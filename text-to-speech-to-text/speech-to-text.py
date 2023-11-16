from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import subprocess
import json

content_safety_path = './content-safety/content-safety.py'
text_to_speech_path = './text-to-speech-to-text/text-to-speech.py'
summarize_text_path = './summarize-text/summarize.py'
entity_recognition_path = './summarize-text/entity-recognition.py'
google_knowledge_graph_path = './ask-google-KG/ask-google-KG.py'

load_dotenv("./text-to-speech-to-text/env.txt")

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

def speech_recognize_continuous_async_from_microphone(speech_config):
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="es-BO")

    done = False
    stop = ''
    
    def called_alessandro(speach):
        names = ['alessandro','alexandro']
        found = False
        name_found = ''
        for name in names:
            if speach.find(name) > -1:
                found = True
                name_found = name
                break
        return found, name_found
    
    def check_severity_of_request(text):
        command = ["python", content_safety_path, "--text", text]
        script_output = subprocess.check_output(command, universal_newlines=True)
        output_dict = eval(script_output)
        offensive_content = False
        for severity in output_dict.values():
            if(severity > 3):
                offensive_content = True
        return offensive_content

    def summarize_text(text):
        if len(text) > 150:
            command = ["python", summarize_text_path, "--text", text]
            text = subprocess.check_output(command, universal_newlines=True)
        return text
    
    def get_entities(text):
        command = ["python", entity_recognition_path, "--text", text]
        script_output = subprocess.check_output(command, universal_newlines=True)
        output_dict = eval(script_output)
        return output_dict
    
    def get_knowledge_graph(entities):
        command = ["python", google_knowledge_graph_path, "--entities"]
        for entity in entities:
            command.append(entity)
        script_output = subprocess.check_output(command, universal_newlines=True)
        return script_output

    def read_answer(answer, show_text = True):
        if show_text:
            print('Alessandro esta respondiendo...')
        command = ["python", text_to_speech_path, "--text", answer]
        _ = subprocess.check_output(command, universal_newlines=True)

    def ask_alessandro(question, name):
        print("Alessandro esta pensando...")
        result = question.split(name,1)[1]
        if check_severity_of_request(result):
            read_answer("Lo siento, no puedo ayudarte porque he detectado contenido ofensivo en tu pregunta")
        else:
            result = summarize_text(result)
            entities = get_entities(result)
            if len(entities) > 0:
                information = get_knowledge_graph(entities)
                read_answer(f'¡Claro! {information}. ¿Tienes alguna otra pregunta?')
            else:
                read_answer("Lo siento, soy un asistente únicamente orientado a darte información sobre figuras públicas.")
        print('Alessandro termino de responder. \n')

    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        if called_alessandro(evt.result.text.lower())[0]:
            print("Alessandro esta atendiendo...")

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        called, name = called_alessandro(evt.result.text.lower())
        if called:
            ask_alessandro(evt.result.text, name)

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition"""
        print('CLOSING on {}'.format(evt.result.text))
        nonlocal done
        done = True

    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    result_future = speech_recognizer.start_continuous_recognition_async()

    result_future.get()  # wait for voidfuture, so we know engine initialization is done.
    print('¡Hola! soy Alessandro tu asistente virtual, para que te responda no olvides llamarme por mi nombre. \n')
    read_answer('¡Hola! soy Alessandro tu asistente virtual, para que te responda no olvides llamarme por mi nombre.', False)

    while not done:
        stop = input()
        if (stop.lower() == "stop"):
            print('Apagando a Alessandro.')
            speech_recognizer.stop_continuous_recognition_async()
            break

    print("Alessandro fue apagado.")

speech_recognize_continuous_async_from_microphone(speech_config)