from __future__ import annotations

from src.runtime import configure_matplotlib_cache

configure_matplotlib_cache()

import matplotlib.pyplot as plt
import pandas as pd


PRIMARY = "#0F5257"
SECONDARY = "#B85C38"
TERTIARY = "#E7A977"
BACKGROUND = "#F6F1E9"
GRID = "#D6C7B8"
TEXT = "#1D2433"


def _base_figure(figsize: tuple[int, int] = (8, 4.5)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor("#FFFDFC")
    ax.grid(axis="y", color=GRID, alpha=0.65, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=TEXT)
    ax.title.set_color(TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    return fig, ax


def plot_price_distribution(df: pd.DataFrame):
    fig, ax = _base_figure()
    ax.hist(df["price"], bins=30, color=PRIMARY, edgecolor="#FFFDFC", alpha=0.9)
    ax.set_title("Distribution des prix")
    ax.set_xlabel("Prix de vente ($)")
    ax.set_ylabel("Nombre de transactions")
    return fig


def plot_ppsf_distribution(df: pd.DataFrame):
    fig, ax = _base_figure()
    ax.hist(df["price_per_sqft"], bins=30, color=SECONDARY, edgecolor="#FFFDFC", alpha=0.85)
    ax.set_title("Distribution du prix au pied carre")
    ax.set_xlabel("Prix / sqft ($)")
    ax.set_ylabel("Nombre de transactions")
    return fig


def plot_price_vs_living_area(df: pd.DataFrame, highlight_row: pd.Series | None = None):
    fig, ax = _base_figure(figsize=(8, 5))
    ax.scatter(df["sqft_living"], df["price"], s=18, alpha=0.35, color=PRIMARY)
    if highlight_row is not None:
        ax.scatter(
            float(highlight_row["sqft_living"]),
            float(highlight_row["price"]),
            s=140,
            color=SECONDARY,
            edgecolor="#FFFDFC",
            linewidth=1.2,
            zorder=5,
        )
    ax.set_title("Prix vs surface habitable")
    ax.set_xlabel("Surface habitable (sqft)")
    ax.set_ylabel("Prix de vente ($)")
    return fig


def plot_transactions_over_time(df: pd.DataFrame):
    monthly = df.groupby("sale_month", as_index=False).agg(
        transactions=("id", "count"),
        median_price=("price", "median"),
    )
    fig, ax = _base_figure(figsize=(8, 4.8))
    ax.plot(monthly["sale_month"], monthly["transactions"], color=PRIMARY, linewidth=2.4)
    ax.fill_between(monthly["sale_month"], monthly["transactions"], color=TERTIARY, alpha=0.2)
    ax.set_title("Transactions mensuelles")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Nombre de ventes")
    ax.tick_params(axis="x", rotation=45)
    return fig


def plot_median_price_by_zipcode(df: pd.DataFrame, limit: int = 12):
    zipcode_summary = (
        df.groupby("zipcode", as_index=False)
        .agg(median_price=("price", "median"), transactions=("id", "count"))
        .sort_values("median_price", ascending=False)
        .head(limit)
        .sort_values("median_price")
    )

    fig, ax = _base_figure(figsize=(8, 5))
    ax.barh(zipcode_summary["zipcode"], zipcode_summary["median_price"], color=PRIMARY, alpha=0.9)
    ax.set_title("Prix median par code postal")
    ax.set_xlabel("Prix median ($)")
    ax.set_ylabel("Code postal")
    return fig


def plot_quality_drivers(df: pd.DataFrame):
    quality = (
        df.groupby("grade", as_index=False)
        .agg(median_price=("price", "median"), median_ppsf=("price_per_sqft", "median"))
        .sort_values("grade")
    )
    fig, ax = _base_figure(figsize=(8, 4.8))
    ax.plot(quality["grade"], quality["median_price"], color=PRIMARY, linewidth=2.5, marker="o")
    ax.set_title("Impact du grade sur le prix median")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Prix median ($)")
    return fig


def plot_geographic_map(df: pd.DataFrame, highlight_row: pd.Series | None = None):
    fig, ax = _base_figure(figsize=(8, 5.6))
    scatter = ax.scatter(
        df["long"],
        df["lat"],
        c=df["price_per_sqft"],
        cmap="YlGnBu",
        s=16,
        alpha=0.5,
    )
    if highlight_row is not None:
        ax.scatter(
            float(highlight_row["long"]),
            float(highlight_row["lat"]),
            color=SECONDARY,
            s=150,
            edgecolor="#FFFDFC",
            linewidth=1.2,
            zorder=6,
        )
    ax.set_title("Carte des transactions")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.colorbar(scatter, ax=ax, label="Prix / sqft ($)")
    return fig


def plot_comparable_prices(comparables: pd.DataFrame, target_price: float):
    fig, ax = _base_figure(figsize=(8, 4.8))
    ax.bar(comparables["id"].astype(str), comparables["price"], color=PRIMARY, alpha=0.85)
    ax.axhline(target_price, color=SECONDARY, linewidth=2.2, linestyle="--")
    ax.set_title("Prix des comparables vs cible")
    ax.set_xlabel("Comparable")
    ax.set_ylabel("Prix ($)")
    ax.tick_params(axis="x", rotation=45)
    return fig
