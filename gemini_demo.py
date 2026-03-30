import os
import sys

sys.dont_write_bytecode = True

from dotenv import load_dotenv
from google import genai

from src.runtime import get_secret


REQUESTED_MODEL = "gemini-3.1-flash-lite-preview"
FALLBACK_MODELS = ("gemini-3-flash-preview", "gemini-2.5-flash-lite")


def main() -> None:
    load_dotenv()

    api_key = get_secret("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY est introuvable dans les secrets Streamlit ou le fichier .env.")

    model_name = get_secret("GEMINI_MODEL", REQUESTED_MODEL)
    prompt = os.getenv("GEMINI_PROMPT", "Explique brievement la finance de marche.")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
    except Exception as exc:
        print(f"Echec avec le modele '{model_name}': {exc}")
        print("Modeles officiels proches a essayer si celui-ci n'est pas disponible :")
        for fallback_model in FALLBACK_MODELS:
            print(f"- {fallback_model}")
        return

    print(response.text)


if __name__ == "__main__":
    main()
