
import random

def procesar_trabajar(mensaje):
    return "trabajar" in mensaje.lower().startswith(PREFIJO + "trabajar")

def procesar_crime(mensaje):
    return "crime" in mensaje.lower().startswith(PREFIJO + "crime")

def procesar_daily(mensaje):
    return "daily" in mensaje.lower().startswith(PREFIJO + "daily")

def procesar_despositar(mensaje):
    return "depositar" in mensaje.lower().startswith(PREFIJO + "depositar")

def procesar_retirar(mensaje):
    return "retirar" in mensaje.lower().startswith(PREFIJO + "retirar")

def procesar_banco(mensaje):
    return "banco" in mensaje.lower().startswith(PREFIJO + "banco")