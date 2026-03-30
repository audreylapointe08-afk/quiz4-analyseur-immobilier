import streamlit as st

from src.comparables import build_valuation_summary, find_comparables
from src.data import apply_filters, build_market_snapshot, load_data
from src.llm import build_market_prompt, build_property_prompt, generate_text, llm_available
from src.metrics import describe_property_row
from src.ui import render_hero, render_market_filters


df = load_data()
filters = render_market_filters(df, "ai_market")
filtered_df = apply_filters(df, filters)

render_hero(
    title="Produire une synthese IA pour l'equipe d'investissement",
    body=(
        "Gemini s'appuie sur un resume structure des donnees filtrees ou d'une propriete cible. "
        "Le prompt reste ancre sur les chiffres issus de pandas pour limiter les hallucinations."
    ),
    kicker="Assistant IA",
)

available, message = llm_available()
if not available:
    st.warning(message)
    st.stop()

tab_market, tab_property = st.tabs(["Synthese marche", "Note propriete"])

with tab_market:
    if filtered_df.empty:
        st.info("Ajustez les filtres pour construire un sous-marche analysable.")
    else:
        snapshot = build_market_snapshot(filtered_df)
        st.write("Resume envoye au modele")
        st.json(snapshot)
        if st.button("Generer la synthese marche", type="primary"):
            with st.spinner("Generation en cours..."):
                try:
                    prompt = build_market_prompt(snapshot, filters)
                    st.markdown(generate_text(prompt))
                except Exception as exc:
                    st.error(f"Impossible d'interroger Gemini: {exc}")

with tab_property:
    selected_id = st.selectbox("Selectionner une transaction de reference", df["id"].tolist())
    target_row = df[df["id"] == selected_id].iloc[0]
    comparables = find_comparables(df, target_row, limit=6)
    valuation = build_valuation_summary(target_row, comparables)
    property_payload = describe_property_row(target_row)
    comparable_payload = comparables.fillna("").to_dict(orient="records")

    preview_columns = st.columns(2)
    with preview_columns[0]:
        st.write("Fiche bien")
        st.json(property_payload)
    with preview_columns[1]:
        st.write("Valorisation")
        st.json(valuation)

    if st.button("Generer la note propriete"):
        with st.spinner("Generation en cours..."):
            try:
                prompt = build_property_prompt(property_payload, valuation, comparable_payload)
                st.markdown(generate_text(prompt))
            except Exception as exc:
                st.error(f"Impossible d'interroger Gemini: {exc}")
