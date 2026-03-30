from __future__ import annotations

import pandas as pd
import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --sand: #f6f1e9;
            --paper: #fffdf9;
            --ink: #1d2433;
            --teal: #0f5257;
            --copper: #b85c38;
            --gold: #d8a25e;
            --line: #d7cab9;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(216,162,94,0.15), transparent 28%),
                radial-gradient(circle at top left, rgba(15,82,87,0.09), transparent 30%),
                linear-gradient(180deg, #f8f3eb 0%, #f4ede2 100%);
            color: var(--ink);
        }

        h1, h2, h3 {
            font-family: Georgia, "Times New Roman", serif;
            letter-spacing: 0.02em;
        }

        html, body, [class*="css"] {
            font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        }

        .hero-card {
            padding: 1.5rem 1.6rem;
            border: 1px solid rgba(215, 202, 185, 0.9);
            background: linear-gradient(135deg, rgba(255,253,249,0.94), rgba(241,234,223,0.95));
            border-radius: 20px;
            box-shadow: 0 18px 45px rgba(29,36,51,0.08);
            margin-bottom: 1rem;
        }

        .hero-kicker {
            color: var(--teal);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .hero-title {
            color: var(--ink);
            font-size: 2.4rem;
            line-height: 1.05;
            margin-top: 0.35rem;
            margin-bottom: 0.5rem;
        }

        .hero-copy {
            color: rgba(29,36,51,0.84);
            font-size: 1.05rem;
            max-width: 56rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,253,249,0.86);
            border: 1px solid rgba(215, 202, 185, 0.85);
            border-radius: 16px;
            padding: 0.65rem 0.8rem;
        }

        div[data-testid="stMetricLabel"] {
            color: #5f6471;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(215, 202, 185, 0.85);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, body: str, kicker: str = "King County Real Estate Lab") -> None:
    st.markdown(
        f"""
        <section class="hero-card">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{body}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_market_filters(df: pd.DataFrame, prefix: str) -> dict[str, object]:
    st.sidebar.subheader("Filtres")
    zipcode_options = sorted(df["zipcode"].unique().tolist())
    price_min = int(df["price"].min())
    price_max = int(df["price"].max())
    sqft_min = int(df["sqft_living"].min())
    sqft_max = int(df["sqft_living"].max())
    year_min = int(df["yr_built"].min())
    year_max = int(df["yr_built"].max())

    zipcodes = st.sidebar.multiselect(
        "Codes postaux",
        zipcode_options,
        default=[],
        key=f"{prefix}_zipcodes",
        help="Laissez vide pour afficher l'ensemble du comte.",
    )
    price_range = st.sidebar.slider(
        "Prix",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
        step=25000,
        key=f"{prefix}_price_range",
    )
    sqft_range = st.sidebar.slider(
        "Surface habitable (sqft)",
        min_value=sqft_min,
        max_value=sqft_max,
        value=(sqft_min, sqft_max),
        step=50,
        key=f"{prefix}_sqft_range",
    )
    min_bedrooms = st.sidebar.slider(
        "Chambres minimum",
        min_value=int(df["bedrooms"].min()),
        max_value=int(df["bedrooms"].max()),
        value=int(df["bedrooms"].min()),
        key=f"{prefix}_min_bedrooms",
    )
    min_bathrooms = st.sidebar.slider(
        "Salles de bain minimum",
        min_value=float(df["bathrooms"].min()),
        max_value=float(df["bathrooms"].max()),
        value=float(df["bathrooms"].min()),
        step=0.25,
        key=f"{prefix}_min_bathrooms",
    )
    grade_range = st.sidebar.slider(
        "Grade",
        min_value=int(df["grade"].min()),
        max_value=int(df["grade"].max()),
        value=(int(df["grade"].min()), int(df["grade"].max())),
        key=f"{prefix}_grade_range",
    )
    condition_range = st.sidebar.slider(
        "Condition",
        min_value=int(df["condition"].min()),
        max_value=int(df["condition"].max()),
        value=(int(df["condition"].min()), int(df["condition"].max())),
        key=f"{prefix}_condition_range",
    )
    year_range = st.sidebar.slider(
        "Annee de construction",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        key=f"{prefix}_year_range",
    )
    waterfront_only = st.sidebar.checkbox("Seulement waterfront", key=f"{prefix}_waterfront_only")
    renovated_only = st.sidebar.radio(
        "Renovation",
        options=["Toutes", "Renovees", "Non renovees"],
        index=0,
        key=f"{prefix}_renovation",
    )

    return {
        "zipcodes": zipcodes,
        "price_range": price_range,
        "sqft_range": sqft_range,
        "min_bedrooms": min_bedrooms,
        "min_bathrooms": min_bathrooms,
        "grade_range": grade_range,
        "condition_range": condition_range,
        "year_range": year_range,
        "waterfront_only": waterfront_only,
        "renovated_only": renovated_only,
    }
