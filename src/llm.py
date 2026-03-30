from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def llm_available() -> tuple[bool, str]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False, "La variable GOOGLE_API_KEY est absente du fichier .env."
    return True, ""


def build_market_prompt(snapshot: dict[str, float | int | str], filters: dict[str, object]) -> str:
    selected_zipcodes = filters["zipcodes"]
    zipcode_scope = ", ".join(selected_zipcodes[:8]) if selected_zipcodes else "tous les zipcodes"
    return f"""
Tu es analyste junior dans un fonds immobilier.
Redige une synthese concise, professionnelle et factuelle en francais.

Contexte:
- Zone analysee: {zipcode_scope}
- Transactions: {snapshot["transactions"]}
- Prix median: {snapshot["median_price"]:.0f} $
- Prix moyen: {snapshot["average_price"]:.0f} $
- Prix median au pied carre: {snapshot["median_ppsf"]:.0f} $
- Surface mediane: {snapshot["median_living_area"]:.0f} sqft
- Part de biens waterfront: {snapshot["waterfront_share"]:.1f} %
- Part de biens renoves: {snapshot["renovated_share"]:.1f} %
- Grade moyen: {snapshot["avg_grade"]:.2f}
- Fenetre temporelle: {snapshot["date_min"]} a {snapshot["date_max"]}

Attendu:
- 1 paragraphe sur le marche
- 3 points cles
- 1 angle d'investissement a surveiller
Ne jamais inventer de chiffres.
""".strip()


def build_property_prompt(
    property_payload: dict[str, str],
    valuation_payload: dict[str, float],
    comparable_payload: list[dict[str, object]],
) -> str:
    return f"""
Tu rediges une note d'investissement courte et factuelle en francais.

Bien cible:
{property_payload}

Valorisation:
{valuation_payload}

Comparables:
{comparable_payload}

Attendu:
- 1 resume de la propriete
- 3 forces
- 3 points de vigilance
- 1 conclusion: sous-evaluee, correctement valorisee ou surevaluee
Ne jamais inventer de donnees absentes.
""".strip()


def generate_text(prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text
