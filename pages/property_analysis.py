import pandas as pd
import streamlit as st

from src.charts import plot_comparable_prices, plot_geographic_map, plot_price_vs_living_area
from src.comparables import build_manual_property, build_valuation_summary, find_comparables
from src.data import load_data
from src.metrics import describe_property_row, format_currency, format_number, format_pct
from src.ui import render_hero


df = load_data()

render_hero(
    title="Evaluer une propriete et la comparer au marche local",
    body=(
        "Selectionnez un bien historique ou saisissez une opportunite en cours d'etude. "
        "L'application calcule un panel de comparables et une lecture de valorisation simple."
    ),
    kicker="Propriete",
)

analysis_mode = st.radio(
    "Mode d'analyse",
    options=["Selectionner une transaction du dataset", "Saisir une propriete manuellement"],
    horizontal=True,
)

if analysis_mode == "Selectionner une transaction du dataset":
    selected_zipcode = st.selectbox("Code postal", sorted(df["zipcode"].unique()))
    zipcode_df = df[df["zipcode"] == selected_zipcode].sort_values("price", ascending=False)
    selected_property_id = st.selectbox("Transaction", zipcode_df["id"].tolist())
    target_row = zipcode_df[zipcode_df["id"] == selected_property_id].iloc[0]
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        asking_price = st.number_input("Prix demande ($)", min_value=50000, value=650000, step=25000)
        bedrooms = st.slider("Chambres", min_value=1, max_value=10, value=3)
        bathrooms = st.slider("Salles de bain", min_value=1.0, max_value=8.0, value=2.5, step=0.25)
        sqft_living = st.number_input("Surface habitable (sqft)", min_value=400, value=2000, step=50)
    with col2:
        sqft_lot = st.number_input("Terrain (sqft)", min_value=500, value=5000, step=100)
        floors = st.slider("Etages", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
        grade = st.slider("Grade", min_value=1, max_value=13, value=7)
        condition = st.slider("Condition", min_value=1, max_value=5, value=3)
    with col3:
        zipcode = st.selectbox("Code postal de reference", sorted(df["zipcode"].unique()))
        waterfront = st.checkbox("Waterfront")
        view = st.slider("Vue", min_value=0, max_value=4, value=1)
        yr_built = st.number_input("Annee de construction", min_value=1900, max_value=2015, value=1995)
        yr_renovated = st.number_input("Annee de renovation", min_value=0, max_value=2015, value=0)

    zipcode_slice = df[df["zipcode"] == zipcode]
    target_row = build_manual_property(
        {
            "asking_price": asking_price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft_living": sqft_living,
            "sqft_lot": sqft_lot,
            "floors": floors,
            "waterfront": int(waterfront),
            "view": view,
            "condition": condition,
            "grade": grade,
            "yr_built": yr_built,
            "yr_renovated": yr_renovated,
            "zipcode": zipcode,
            "lat": float(zipcode_slice["lat"].median()),
            "long": float(zipcode_slice["long"].median()),
        }
    )
    target_row["sale_date"] = pd.Timestamp.today()

comparables = find_comparables(df, target_row, limit=8)
valuation = build_valuation_summary(target_row, comparables)

metric_cols = st.columns(5)
metric_cols[0].metric("Prix cible", format_currency(target_row["price"]))
metric_cols[1].metric("Valeur estimee", format_currency(valuation["estimated_value"]))
metric_cols[2].metric("Ecart", format_currency(valuation["pricing_gap"]))
metric_cols[3].metric("Ecart %", format_pct(valuation["pricing_gap_pct"]))
metric_cols[4].metric("Comparables", format_number(valuation["comp_count"]))

left, right = st.columns([0.95, 1.05])
with left:
    st.subheader("Fiche de la propriete")
    property_snapshot = pd.DataFrame(
        {"Champ": list(describe_property_row(target_row).keys()), "Valeur": list(describe_property_row(target_row).values())}
    )
    st.dataframe(property_snapshot, use_container_width=True, hide_index=True)

    market_position = "correctement valorisee"
    if valuation["pricing_gap_pct"] <= -7:
        market_position = "sous-evaluee"
    elif valuation["pricing_gap_pct"] >= 7:
        market_position = "surevaluee"

    st.subheader("Lecture rapide")
    st.markdown(
        f"""
        - Cette propriete semble **{market_position}** par rapport au panel de comparables.
        - Le panel retient **{format_number(valuation['comp_count'])}** transactions proches.
        - Le **prix median des comparables** ressort a **{format_currency(valuation['median_comp_price'])}**.
        - Le **prix median au pied carre** des comparables est de **{format_currency(valuation['median_comp_ppsf'])}**.
        """
    )

with right:
    st.subheader("Comparables")
    display_comps = comparables.copy()
    display_comps["price"] = display_comps["price"].map(format_currency)
    display_comps["price_per_sqft"] = display_comps["price_per_sqft"].map(format_currency)
    display_comps["sqft_living"] = display_comps["sqft_living"].map(format_number)
    display_comps["bathrooms"] = display_comps["bathrooms"].map(lambda value: format_number(value, 2))
    display_comps["sale_date"] = pd.to_datetime(display_comps["sale_date"]).dt.strftime("%Y-%m-%d")
    st.dataframe(display_comps, use_container_width=True, hide_index=True)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    market_scope = df[df["zipcode"] == str(target_row["zipcode"])]
    st.pyplot(plot_price_vs_living_area(market_scope, highlight_row=target_row), clear_figure=True)
with chart_col2:
    if not comparables.empty:
        st.pyplot(plot_comparable_prices(comparables, float(target_row["price"])), clear_figure=True)

st.subheader("Carte locale")
map_scope = df[df["zipcode"] == str(target_row["zipcode"])]
st.pyplot(plot_geographic_map(map_scope, highlight_row=target_row), clear_figure=True)
