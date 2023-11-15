from dotenv import load_dotenv
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import argparse
import sys

parser = argparse.ArgumentParser("Analize Text")
parser.add_argument("--text", type=str, help="Text to be analized")

args = parser.parse_args()

print("Cargar variables de entorno desde archivo .env")
load_dotenv("env.txt",override=True)

def analyze_text(text_input: str):
    # analyze text
    key = os.environ.get("CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("CONTENT_SAFETY_ENDPOINT")

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=text_input)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    
    severity = {
        "hate":response.hate_result.severity,
        "self_harm":response.hate_result.severity,
        "sexual":response.hate_result.severity,
        "violence":response.hate_result.severity,
    }

    return severity

if __name__ == "__main__":
    # Obtén argumentos de la línea de comandos si es necesario
    # ...

    # Llama a la función y almacena el resultado
    resultado_funcion = analyze_text(args.text)

    # Imprime o utiliza el resultado
    print("El resultado es:", resultado_funcion)

    # Devuelve el resultado como código de salida
    sys.exit(0)