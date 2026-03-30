import streamlit as st

from src.charts import plot_geographic_map, plot_price_distribution, plot_transactions_over_time
from src.data import build_market_snapshot, load_data, summarize_zipcodes
from src.metrics import format_currency, format_number, format_pct
from src.ui import render_hero


df = load_data()
snapshot = build_market_snapshot(df)
top_zipcodes = summarize_zipcodes(df, top_n=8)

render_hero(
    title="Analyse interactive du marche immobilier du comte de King",
    body=(
        "Explorez 21 613 transactions, identifiez des poches de valeur et produisez une note "
        "d'investissement avec l'assistant Gemini. Cette version est pensée pour un usage d'equipe "
        "rapide en screening et en valorisation."
    ),
)

metric_columns = st.columns(4)
metric_columns[0].metric("Transactions", format_number(snapshot["transactions"]))
metric_columns[1].metric("Prix median", format_currency(snapshot["median_price"]))
metric_columns[2].metric("Prix median / sqft", format_currency(snapshot["median_ppsf"]))
metric_columns[3].metric("Biens renoves", format_pct(snapshot["renovated_share"]))

metric_columns_2 = st.columns(4)
metric_columns_2[0].metric("Prix moyen", format_currency(snapshot["average_price"]))
metric_columns_2[1].metric("Surface mediane", f"{format_number(snapshot['median_living_area'])} sqft")
metric_columns_2[2].metric("Waterfront", format_pct(snapshot["waterfront_share"]))
metric_columns_2[3].metric("Grade moyen", format_number(snapshot["avg_grade"], 2))

left, right = st.columns([1.1, 0.9])
with left:
    st.subheader("Ce que fait l'application")
    st.markdown(
        """
        - Explorer le marche avec des filtres operationnels.
        - Comparer les prix, surfaces et dynamiques par code postal.
        - Evaluer une propriete existante ou un bien saisi manuellement.
        - Generer une synthese IA exploitable en comite d'investissement.
        """
    )
    st.subheader("Couverture du dataset")
    st.markdown(
        f"""
        Les ventes s'etendent du **{snapshot['date_min']}** au **{snapshot['date_max']}**.
        Le fichier contient les caracteristiques de prix, qualite, taille, localisation
        et historique de renovation pour chaque transaction.
        """
    )
    st.dataframe(top_zipcodes, use_container_width=True, hide_index=True)

with right:
    st.subheader("Empreinte geographique")
    sample_size = min(len(df), 4000)
    st.pyplot(plot_geographic_map(df.sample(sample_size, random_state=42)), clear_figure=True)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.pyplot(plot_price_distribution(df), clear_figure=True)
with chart_col2:
    st.pyplot(plot_transactions_over_time(df), clear_figure=True)

st.subheader("Apercu des donnees")
st.dataframe(
    df[
        [
            "id",
            "sale_date",
            "price",
            "zipcode",
            "bedrooms",
            "bathrooms",
            "sqft_living",
            "grade",
            "condition",
        ]
    ].head(15),
    use_container_width=True,
    hide_index=True,
)
