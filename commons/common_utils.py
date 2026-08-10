import subprocess
import re
import os

def execute_comand(comand):

	try:
		# Per cada fitxer creat preparem la comanda fent ús d'ExifTool i subprocess 
	    # ja que no és una llibreria nativa de Python
		result = subprocess.run(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)    

	    # Retornem la sortida si el codi és 0 (tot correcte)
		if result.returncode == 0:
			return result.stdout

		# Retornem la sortida si el codi és 2 (cap coincidència)
		elif result.returncode == 2:
			return result.stdout

		# Llançar una excepció genèrica si hi ha qualsevol altre error
		else:	
			raise subprocess.CalledProcessError(result.returncode, comand, output=result.stdout, stderr=result.stderr)

	except subprocess.CalledProcessError as e:
		# Gestionar l'error: mostrar l'error i la sortida stderr
		print(f"Error on the execution (#{result.returncode}): {e.stderr or 'No error message available.'}")
		return ""

	except Exception as e:
		# General exception handling
		print(f"An error occurred: {e}")
		return ""

def extract_int_from_output(output, pattern):

	#Definim les variables necessàries
	num_to_return = 0

	# Obtenim el nombre a partir de la resposta
	match = re.search(rf"(\d+) {pattern}", output)

	if match:
		num_to_return += int(match.group(1))
	else:
		num_to_return += 0

	return num_to_return

import os
from pathlib import Path

