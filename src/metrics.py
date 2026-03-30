from __future__ import annotations

import pandas as pd


def format_currency(value: float | int) -> str:
    return f"${value:,.0f}"


def format_number(value: float | int, digits: int = 0) -> str:
    return f"{value:,.{digits}f}"


def format_pct(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}%"


def describe_property_row(row: pd.Series) -> dict[str, str]:
    return {
        "ID": str(row["id"]),
        "Prix": format_currency(row["price"]),
        "Code postal": str(row["zipcode"]),
        "Chambres": format_number(row["bedrooms"]),
        "Salles de bain": format_number(row["bathrooms"], 2),
        "Surface habitable": f"{format_number(row['sqft_living'])} sqft",
        "Terrain": f"{format_number(row['sqft_lot'])} sqft",
        "Prix / sqft": format_currency(row["price_per_sqft"]),
        "Grade": format_number(row["grade"]),
        "Condition": format_number(row["condition"]),
        "Annee de construction": format_number(row["yr_built"]),
        "Vente": row["sale_date"].strftime("%Y-%m-%d"),
    }
