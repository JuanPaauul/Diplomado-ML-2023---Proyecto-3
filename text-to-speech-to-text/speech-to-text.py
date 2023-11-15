from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import subprocess
import json

content_safety_path = './content-safety/content-safety.py'

print("Cargar variables de entorno desde archivo .env")
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
        comando = ["python", content_safety_path, "--text", text]
        salida_script = subprocess.check_output(comando, universal_newlines=True)
        diccionario = eval(salida_script)
        print("Salida: ", diccionario)
        print("Tipo de salida: ", type(diccionario))

    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        already_called = False
        if called_alessandro(evt.result.text)[0] and not already_called:
            already_called = True
            print("Alessandro esta atendiendo...")

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        called, name = called_alessandro(evt.result.text)
        if called:
            result = evt.result.text.split(name,1)[1]
            print("Lo que se buscara es: ",result)
            check_severity_of_request(result)

        print('RECOGNIZED: {}'.format(evt.result.text))

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
    print('Continuous Recognition is now running, say something.')
    print('type "stop" then enter when done')

    while not done:
        stop = input()
        if (stop.lower() == "stop"):
            print('Stopping async recognition.')
            speech_recognizer.stop_continuous_recognition_async()
            break

    print("recognition stopped, main thread can exit now.")

speech_recognize_continuous_async_from_microphone(speech_config)