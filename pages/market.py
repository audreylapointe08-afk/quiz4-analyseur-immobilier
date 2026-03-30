import streamlit as st

from src.charts import (
    plot_geographic_map,
    plot_median_price_by_zipcode,
    plot_ppsf_distribution,
    plot_price_distribution,
    plot_price_vs_living_area,
    plot_quality_drivers,
    plot_transactions_over_time,
)
from src.data import apply_filters, build_market_snapshot, load_data, summarize_zipcodes
from src.metrics import format_currency, format_number, format_pct
from src.ui import render_hero, render_market_filters


df = load_data()
filters = render_market_filters(df, "market")
filtered_df = apply_filters(df, filters)
snapshot = build_market_snapshot(filtered_df)

render_hero(
    title="Explorer le marche, trouver les poches de valeur",
    body=(
        "Filtrez le comte de King selon vos hypotheses d'investissement, visualisez les regimes de prix "
        "et reperez les micro-marches a plus forte liquidite."
    ),
    kicker="Marche",
)

if filtered_df.empty:
    st.warning("Aucune transaction ne correspond aux filtres actuels.")
    st.stop()

metric_columns = st.columns(5)
metric_columns[0].metric("Transactions", format_number(snapshot["transactions"]))
metric_columns[1].metric("Prix median", format_currency(snapshot["median_price"]))
metric_columns[2].metric("Prix moyen", format_currency(snapshot["average_price"]))
metric_columns[3].metric("Prix / sqft", format_currency(snapshot["median_ppsf"]))
metric_columns[4].metric("Waterfront", format_pct(snapshot["waterfront_share"]))

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.pyplot(plot_price_distribution(filtered_df), clear_figure=True)
with chart_col2:
    st.pyplot(plot_ppsf_distribution(filtered_df), clear_figure=True)

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    st.pyplot(plot_transactions_over_time(filtered_df), clear_figure=True)
with chart_col4:
    st.pyplot(plot_price_vs_living_area(filtered_df), clear_figure=True)

chart_col5, chart_col6 = st.columns(2)
with chart_col5:
    st.pyplot(plot_median_price_by_zipcode(filtered_df), clear_figure=True)
with chart_col6:
    st.pyplot(plot_quality_drivers(filtered_df), clear_figure=True)

st.subheader("Carte des transactions filtrees")
sample_df = filtered_df.sample(min(len(filtered_df), 5000), random_state=42)
st.pyplot(plot_geographic_map(sample_df), clear_figure=True)

left, right = st.columns([1.05, 0.95])
with left:
    st.subheader("Top codes postaux")
    zipcode_summary = summarize_zipcodes(filtered_df, top_n=12).copy()
    zipcode_summary["median_price"] = zipcode_summary["median_price"].map(format_currency)
    zipcode_summary["median_ppsf"] = zipcode_summary["median_ppsf"].map(format_currency)
    zipcode_summary["avg_grade"] = zipcode_summary["avg_grade"].map(lambda value: format_number(value, 2))
    st.dataframe(zipcode_summary, use_container_width=True, hide_index=True)

with right:
    st.subheader("Lecture investisseur")
    most_liquid = summarize_zipcodes(filtered_df, top_n=1)
    best_grade = (
        filtered_df.groupby("zipcode", as_index=False)
        .agg(avg_grade=("grade", "mean"), median_price=("price", "median"))
        .sort_values(["avg_grade", "median_price"], ascending=[False, False])
        .head(1)
    )
    st.markdown(
        f"""
        - Le filtre actuel couvre **{format_number(snapshot['transactions'])}** ventes.
        - Le **prix median** ressort a **{format_currency(snapshot['median_price'])}**.
        - Le **prix au pied carre median** est de **{format_currency(snapshot['median_ppsf'])}**.
        - Le marche le plus liquide dans ce sous-ensemble est **{most_liquid.iloc[0]['zipcode']}**.
        - Le meilleur mix qualite/prix ressort actuellement sur **{best_grade.iloc[0]['zipcode']}**.
        """
    )

st.subheader("Donnees filtrees")
st.dataframe(
    filtered_df[
        [
            "id",
            "sale_date",
            "price",
            "zipcode",
            "bedrooms",
            "bathrooms",
            "sqft_living",
            "price_per_sqft",
            "grade",
            "condition",
            "waterfront_label",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
