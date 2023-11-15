from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractiveSummaryAction
) 
import pandas as pd
import argparse

parser = argparse.ArgumentParser("summarize Text")
parser.add_argument("--text", type=str, help="Text to be summarized")

args = parser.parse_args()

load_dotenv("env.txt",override=True)

key = os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# Autenticarse
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()


def sample_extractive_summarization(client, documents):
    document = documents

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=3)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("Error: '{}' - Mensaje: '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            sentences_result = [sentence.text for sentence in extract_summary_result.sentences]
            sentences_result = ''.join(sentences_result)
            print(sentences_result)

document = []
document.append(args.text)
sample_extractive_summarization(client,document)