from dotenv import load_dotenv
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import argparse
import sys
import json

parser = argparse.ArgumentParser("Analize Text")
parser.add_argument("--text", type=str, help="Text to be analized")

args = parser.parse_args()
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
        "self_harm":response.self_harm_result.severity,
        "sexual":response.sexual_result.severity,
        "violence":response.violence_result.severity,
    }

    return severity

if __name__ == "__main__":
    resultado_funcion = analyze_text(args.text)
    resultado_json = json.dumps(resultado_funcion)
    print(resultado_json)
    sys.exit(0)