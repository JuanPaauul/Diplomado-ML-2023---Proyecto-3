import subprocess
import json

ruta_script = "content-safety/content-safety.py"
texto_a_analizar = "Quien es messi?"
comando = ["python", ruta_script, "--text", texto_a_analizar]
salida_script = subprocess.check_output(comando, universal_newlines=True)

# Convertir la salida a un diccionario (puedes ajustar esto según el formato de salida de tu script)
#resultado_dict = json.loads(salida_script)

# Utilizar el resultado como desees
print("Resultado del script:", salida_script)