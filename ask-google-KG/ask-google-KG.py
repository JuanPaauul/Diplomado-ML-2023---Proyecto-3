from dotenv import load_dotenv
import os
import requests
import argparse
import re

parser = argparse.ArgumentParser("Entities Text")
parser.add_argument('--entities', nargs='+', type=str, help='Una lista de cadenas separadas por espacios')


args = parser.parse_args()

load_dotenv("env.txt")

api_key = os.environ.get('API_GOOGLE_KEY')

def limpiar_caracteres(texto):
    texto_limpio = re.sub(r'\u200b+', ' ', texto)
    return texto_limpio

def consultas(lista_entities):
    results = []
    for entitie in lista_entities:

        query = entitie

        url = "https://kgsearch.googleapis.com/v1/entities:search"

        params = {
            "query": query,
            "key": api_key,
            "limit": 1,
            "languages": "es"
        }

        response = requests.get(url, params=params)
        data = response.json()
        if "itemListElement" in data and len(data["itemListElement"]) > 0:
            result = data["itemListElement"][0]["result"]
            description = result["detailedDescription"]["articleBody"]
            description_limpia = limpiar_caracteres(description)
            results.append(description_limpia)
        else:
            print(f"No se encontraron resultados para la consulta sobre {query}.")

    return results

result = consultas(args.entities)
result = ''.join(result)
print(result)