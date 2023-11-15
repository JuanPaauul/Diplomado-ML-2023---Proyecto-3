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

parser = argparse.ArgumentParser("Entities Text")
parser.add_argument("--text", type=str, help="Text contaiing the entities")

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

# Example function for recognizing entities from text
def entity_recognition_example(client, documents):
    try:
        result = client.recognize_entities(documents = documents)[0]
        return result.entities
    
    except Exception as err:
        print("Encountered exception. {}".format(err))

doc_input = []
doc_input.append(args.text)

entities = entity_recognition_example(client,doc_input)

data_list = []

for entity in entities:
    data_list.append([entity.text, entity.category, entity.confidence_score])
    
columns = ['Name','Category','Confidence Score']
df = pd.DataFrame(data_list, columns=columns)


print(list(df[df['Category'] == 'Person'].Name))