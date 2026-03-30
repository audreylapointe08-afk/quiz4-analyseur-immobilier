from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "kc_house_data.csv"


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, dtype={"id": str, "zipcode": str})
    sale_dates = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S", errors="coerce")

    df["sale_date"] = sale_dates
    df["sale_year"] = sale_dates.dt.year
    df["sale_month"] = sale_dates.dt.to_period("M").astype(str)
    df["price_per_sqft"] = (df["price"] / df["sqft_living"]).round(2)
    df["lot_ratio"] = (df["sqft_living"] / df["sqft_lot"]).replace([pd.NA], 0).fillna(0)
    df["property_age"] = (df["sale_year"] - df["yr_built"]).clip(lower=0)
    df["is_renovated"] = df["yr_renovated"].fillna(0).gt(0)
    df["renovation_year"] = df["yr_renovated"].replace(0, pd.NA)
    df["waterfront_label"] = df["waterfront"].map({0: "Non", 1: "Oui"}).fillna("Non")
    df["view_label"] = df["view"].map(
        {
            0: "Aucune",
            1: "Legere",
            2: "Correcte",
            3: "Belle",
            4: "Exceptionnelle",
        }
    )
    return df


def apply_filters(df: pd.DataFrame, filters: dict[str, object]) -> pd.DataFrame:
    filtered = df.copy()

    zipcodes = filters.get("zipcodes")
    if zipcodes:
        filtered = filtered[filtered["zipcode"].isin(zipcodes)]

    min_price, max_price = filters["price_range"]
    filtered = filtered[filtered["price"].between(min_price, max_price)]

    min_sqft, max_sqft = filters["sqft_range"]
    filtered = filtered[filtered["sqft_living"].between(min_sqft, max_sqft)]

    filtered = filtered[filtered["bedrooms"] >= filters["min_bedrooms"]]
    filtered = filtered[filtered["bathrooms"] >= filters["min_bathrooms"]]

    min_grade, max_grade = filters["grade_range"]
    filtered = filtered[filtered["grade"].between(min_grade, max_grade)]

    min_condition, max_condition = filters["condition_range"]
    filtered = filtered[filtered["condition"].between(min_condition, max_condition)]

    min_year, max_year = filters["year_range"]
    filtered = filtered[filtered["yr_built"].between(min_year, max_year)]

    if filters["waterfront_only"]:
        filtered = filtered[filtered["waterfront"] == 1]

    renovated_option = filters["renovated_only"]
    if renovated_option == "Renovees":
        filtered = filtered[filtered["is_renovated"]]
    elif renovated_option == "Non renovees":
        filtered = filtered[~filtered["is_renovated"]]

    return filtered


def build_market_snapshot(df: pd.DataFrame) -> dict[str, float | int | str]:
    if df.empty:
        return {
            "transactions": 0,
            "median_price": 0,
            "average_price": 0,
            "median_ppsf": 0,
            "median_living_area": 0,
            "waterfront_share": 0.0,
            "renovated_share": 0.0,
            "avg_grade": 0.0,
            "date_min": "n/a",
            "date_max": "n/a",
        }

    return {
        "transactions": int(len(df)),
        "median_price": float(df["price"].median()),
        "average_price": float(df["price"].mean()),
        "median_ppsf": float(df["price_per_sqft"].median()),
        "median_living_area": float(df["sqft_living"].median()),
        "waterfront_share": float(df["waterfront"].mean() * 100),
        "renovated_share": float(df["is_renovated"].mean() * 100),
        "avg_grade": float(df["grade"].mean()),
        "date_min": df["sale_date"].min().strftime("%Y-%m-%d"),
        "date_max": df["sale_date"].max().strftime("%Y-%m-%d"),
    }


def summarize_zipcodes(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["zipcode", "transactions", "median_price", "median_ppsf"])

    return (
        df.groupby("zipcode", as_index=False)
        .agg(
            transactions=("id", "count"),
            median_price=("price", "median"),
            median_ppsf=("price_per_sqft", "median"),
            avg_grade=("grade", "mean"),
        )
        .sort_values(["transactions", "median_price"], ascending=[False, False])
        .head(top_n)
    )
