from __future__ import annotations

import pandas as pd


FEATURE_WEIGHTS = {
    "sqft_living": 0.30,
    "bedrooms": 0.10,
    "bathrooms": 0.10,
    "grade": 0.15,
    "condition": 0.10,
    "yr_built": 0.10,
    "sqft_lot": 0.05,
    "view": 0.05,
    "waterfront": 0.05,
}


def build_manual_property(inputs: dict[str, float | int | str]) -> pd.Series:
    return pd.Series(
        {
            "id": "manual-input",
            "price": float(inputs["asking_price"]),
            "bedrooms": float(inputs["bedrooms"]),
            "bathrooms": float(inputs["bathrooms"]),
            "sqft_living": float(inputs["sqft_living"]),
            "sqft_lot": float(inputs["sqft_lot"]),
            "floors": float(inputs["floors"]),
            "waterfront": int(inputs["waterfront"]),
            "view": int(inputs["view"]),
            "condition": int(inputs["condition"]),
            "grade": int(inputs["grade"]),
            "sqft_above": float(inputs["sqft_living"]),
            "sqft_basement": 0.0,
            "yr_built": int(inputs["yr_built"]),
            "yr_renovated": int(inputs["yr_renovated"]),
            "zipcode": str(inputs["zipcode"]),
            "lat": float(inputs["lat"]),
            "long": float(inputs["long"]),
            "sqft_living15": float(inputs["sqft_living"]),
            "sqft_lot15": float(inputs["sqft_lot"]),
            "price_per_sqft": float(inputs["asking_price"]) / max(float(inputs["sqft_living"]), 1.0),
        }
    )


def _score_candidates(candidates: pd.DataFrame, target: pd.Series) -> pd.DataFrame:
    scored = candidates.copy()
    score = pd.Series(0.0, index=scored.index)

    for column, weight in FEATURE_WEIGHTS.items():
        spread = max(scored[column].std(ddof=0), 1.0)
        score += ((scored[column] - float(target[column])).abs() / spread) * weight

    score += (scored["zipcode"] != str(target["zipcode"])).astype(float) * 0.30
    scored["similarity_score"] = score.round(4)
    return scored.sort_values(["similarity_score", "price"])


def find_comparables(df: pd.DataFrame, target: pd.Series, limit: int = 8) -> pd.DataFrame:
    same_zip = df[df["zipcode"] == str(target["zipcode"])].copy()
    same_zip = same_zip[same_zip["id"] != str(target["id"])]

    candidates = same_zip if len(same_zip) >= max(limit, 20) else df[df["id"] != str(target["id"])].copy()
    scored = _score_candidates(candidates, target)

    columns = [
        "id",
        "zipcode",
        "price",
        "price_per_sqft",
        "sqft_living",
        "bedrooms",
        "bathrooms",
        "grade",
        "condition",
        "yr_built",
        "sale_date",
        "similarity_score",
    ]
    return scored[columns].head(limit)


def build_valuation_summary(target: pd.Series, comparables: pd.DataFrame) -> dict[str, float]:
    if comparables.empty:
        return {
            "comp_count": 0,
            "estimated_value": 0.0,
            "median_comp_price": 0.0,
            "median_comp_ppsf": 0.0,
            "pricing_gap": 0.0,
            "pricing_gap_pct": 0.0,
        }

    estimated_value = float(comparables["price"].median())
    median_ppsf = float(comparables["price_per_sqft"].median())
    pricing_gap = float(target["price"]) - estimated_value

    return {
        "comp_count": int(len(comparables)),
        "estimated_value": estimated_value,
        "median_comp_price": estimated_value,
        "median_comp_ppsf": median_ppsf,
        "pricing_gap": pricing_gap,
        "pricing_gap_pct": (pricing_gap / estimated_value * 100) if estimated_value else 0.0,
    }
