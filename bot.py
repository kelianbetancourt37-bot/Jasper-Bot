import sys
import random

PREFIJO = "."

# Simulación rápida de base de datos en memoria
BASE_DATOS_USUARIOS = {}

def obtener_datos(usuario_id):
    if usuario_id not in BASE_DATOS_USUARIOS:
        BASE_DATOS_USUARIOS[usuario_id] = {
            "nombre": "Sin registrar",
            "genero": "No especificado",
            "edad": "Desconocida",
            "nacimiento": "No registrada",
            "descripcion": "Sin biografía.",
            "nivel": 1,
            "xp": 0,
            "nivel_progreso": "[░░░░░░░░░░] 0%",
            "monedas": 500,
            "banco": 0,
            "racha": 0
        }
    return BASE_DATOS_USUARIOS[usuario_id]

# --- Auxiliar RPG para XP y barrita ---
def procesar_expansión_xp(datos, xp_ganada):
    datos["xp"] = datos.get("xp", 0) + xp_ganada
    nivel_actual = datos.get("nivel", 1)
    xp_necesaria = nivel_actual * 100
    
    subio_nivel = False
    while datos["xp"] >= xp_necesaria:
        datos["xp"] -= xp_necesaria
        datos["nivel"] += 1
        nivel_actual = datos["nivel"]
        xp_necesaria = nivel_actual * 100
        subio_nivel = True

    pct = min(100, int((datos["xp"] / xp_necesaria) * 100))
    bloques_llenos = int(pct / 10)
    bloques_vacios = max(0, 10 - bloques_llenos)
    datos["nivel_progreso"] = f"[{'█' * bloques_llenos}{'░' * bloques_vacios}] {pct}%"
    
    return subio_nivel

# --- 1. Handlers de Perfil y Configuración ---
def handler_perfil(args, usuario_id):
    datos = obtener_datos(usuario_id)
    return (
        "╭━━━〔 👤 *TARJETA DE PERFIL* 👤 ━━━╮\n"
        "┃\n"
        f"┃   🏷️ *Nombre:* {datos['nombre']}\n"
        f"┃   🚻 *Género:* {datos['genero']}\n"
        f"┃   🎂 *Edad:* {datos['edad']} años\n"
        f"┃   📅 *Nacimiento:* {datos['nacimiento']}\n\n"
        f"┃   ⭐ *Nivel:* Nivel {datos['nivel']}\n"
        f"┃   📈 *Progreso de nivel:* {datos['nivel_progreso']}\n"
        "┃\n"
        "┣━━ 💰 *ECONOMÍA & RACHA* ━━━\n"
        f"┃   🪙 *Cartera:* {datos['monedas']} monedas\n"
        f"┃   🏦 *Banco:* {datos['banco']} monedas\n"
        f"┃   🔥 *Racha diaria:* {datos['racha']} días\n"
        "┃\n"
        "┣━━ 📝 *BIOGRAFÍA* ━━━\n"
        f"┃   _{datos['descripcion']}_\n"
        "┃\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n"
        "_💡 Usa `.setname`, `.setage`, etc., para editar tus datos._"
    )

def handler_setname(args, usuario_id):
    if not args:
        return "⚠️ Vecino, ¿cómo se va a llamar? Escriba bien. Ejemplo: .setname Don Ramón"
    datos = obtener_datos(usuario_id)
    datos["nombre"] = args
    return f"✅ ¡Vaya! Su nuevo nombre en la vecindad es: *{args}*"

def handler_setdesc(args, usuario_id):
    if not args:
        return "⚠️ Escriba su descripción o chisme de la vecindad. Ejemplo: .setdesc Vendiendo churros"
    datos = obtener_datos(usuario_id)
    datos["descripcion"] = args
    return f"📝 Su recado o descripción quedó registrado en la pared de la vecindad:\n_{args}_"

def handler_setage(args, usuario_id):
    if not str(args).isdigit():
        return "⚠️ Ponga una edad en números, no invente. Ejemplo: .setage 30"
    datos = obtener_datos(usuario_id)
    datos["edad"] = int(args)
    return f"🎂 Con que tiene *{args} años*... ¡Ya está grande para andar jugando con la resortera!"

def handler_setbirth(args, usuario_id):
    if not args:
        return "⚠️ Indique su fecha de nacimiento. Ejemplo: .setbirth 01/01/2000"
    datos = obtener_datos(usuario_id)
    datos["nacimiento"] = args
    return f"📅 Fecha anotada en el calendario de la vecindad: *{args}*"

def handler_setgene(args, usuario_id):
    if not args:
        return "⚠️ Especifique su género. Ejemplo: .setgene Masculino"
    datos = obtener_datos(usuario_id)
    datos["genero"] = args
    return f"🚻 Género registrado correctamente: *{args}*"

def handler_level(args, usuario_id):
    destino = args if args else "Usted"
    datos = obtener_datos(usuario_id)
    return f"📊 *{destino}* se encuentra en el **Nivel {datos['nivel']}** de la vecindad (¡Con experiencia barriendo el patio!)."

def handler_levelup(args, usuario_id):
    destino = args if args else "Vecino"
    datos = obtener_datos(usuario_id)
    datos["nivel"] += 1
    return f"🎉 ¡Felicidades {destino}! Ha ascendido al **Nivel {datos['nivel']}** de la vecindad. ¡Se ganó una torta de jamón! 🥪🚀"

# --- 2. Handlers económicos anteriores ---
def handler_trabajar(args, usuario_id):
    datos = obtener_datos(usuario_id)
    ganancia = random.randint(50, 200)
    xp_ganada = random.randint(25, 60)
    
    datos["monedas"] += ganancia
    subio = procesar_expansión_xp(datos, xp_ganada)
    
    mensaje = f"🛠️ Has trabajado duro y ganaste 🪙 *{ganancia}* monedas y ⭐ *{xp_ganada} XP*."
    if subio:
        mensaje += f"\n🎉 ¡Felicidades! Subiste al **Nivel {datos['nivel']}** de la vecindad. ¡Torta de jamón desbloqueada! 🥪"
    return mensaje

def handler_crime(args, usuario_id):
    datos = obtener_datos(usuario_id)
    exito = random.choice([True, False])
    if exito:
        botin = random.randint(100, 500)
        datos["monedas"] += botin
        return f"🥷 ¡Robo exitoso! Botín conseguido: {botin} monedas."
    else:
        multa = random.randint(50, 150)
        datos["monedas"] = max(0, datos["monedas"] - multa)
        return f"🚨 ¡Te atrapó la policía! Perdiste {multa} monedas."

def handler_daily(args, usuario_id):
    datos = obtener_datos(usuario_id)
    datos["monedas"] += 500
    datos["racha"] += 1
    return "🎁 ¡Reclamaste tu recompensa diaria de 500 monedas!"

def handler_depositar(args, usuario_id):
    if not args or not str(args).isdigit():
        return "⚠️ Debes especificar cuánto depositar en números. Ej: `.dp 100`"
    cantidad = int(args)
    datos = obtener_datos(usuario_id)
    if cantidad > datos["monedas"]:
        return "⚠️ No tienes tantas monedas en la cartera, vecino."
    datos["monedas"] -= cantidad
    datos["banco"] += cantidad
    return f"🏦 Depositaste {cantidad} monedas en el banco de la vecindad."

def handler_retirar(args, usuario_id):
    if not args or not str(args).isdigit():
        return "⚠️ Debes especificar cuánto retirar en números. Ej: `.r 100`"
    cantidad = int(args)
    datos = obtener_datos(usuario_id)
    if cantidad > datos["banco"]:
        return "⚠️ No tienes tanto guardado en el banco."
    datos["banco"] -= cantidad
    datos["monedas"] += cantidad
    return f"💵 Retiraste {cantidad} monedas del banco."

def handler_banco(args, usuario_id):
    datos = obtener_datos(usuario_id)
    return f"💳 Estado de cuenta para la vecindad: Tienes 🪙 {datos['monedas']} en mano y 🏦 {datos['banco']} en el banco."

def handler_menu(args, usuario_id):
    return (
        "╭━━━〔 🤖 *BOT JASPER* 🤖 〕━━━╮\n"
        "┃\n"
        "┃   👤 Perfil y Registro\n"
        "┃   ┃\n"
        "┃ `.perfil`\n"
        "┃ `.setname <nombre>`\n"
        "┃ `.setage <edad>`\n"
        "┃ `.setbirth <fecha>`\n"
        "┃ `.setgene <genero>`\n"
        "┃ `.setdesc <descripción>`\n"
        "┃ `.level / .levelup`\n"
        "┃\n"
        "┃   💰 Economía\n"
        "┃   ┃\n"
        "┃ `.trabajar / .w`\n"
        "┃ `.crime / .c`\n"
        "┃ `.daily / .d`\n"
        "┃ `.depositar / .dp`\n"
        "┃ `.retirar / .r`\n"
        "┃ `.banco / .b`\n"
        "┃\n"
        "┃   📝 Información\n"
        "┃   ┃\n"
        "┃ `.ping / .p`\n"
        "┃\n"
        "┃   👤 Perfil y Registro\n"
        "┃   ┃\n"
        "┃ `.perfil`\n"
        "┃ `.setname <nombre>`\n"
        "┃ `.setage <edad>`\n"
        "┃ `.setbirth <fecha>`\n"
        "┃ `.setgene <genero>`\n"
        "┃ `.setdesc <descripción>`\n"        
        "┃ `.level / .levelup`\n" 
        "╰━━━━━━━━━━━━━━━━━━╯"
    )

# --- 3. Diccionario maestro actualizado ---
ENRUTADOR_COMANDOS = {
    "menu": handler_menu, "help": handler_menu,
    "perfil": handler_perfil, "profile": handler_perfil,
    "setname": handler_setname,
    "setdesc": handler_setdesc,
    "setage": handler_setage,
    "setbirth": handler_setbirth,
    "setgene": handler_setgene,
    "level": handler_level,
    "levelup": handler_levelup, "sublevel": handler_levelup,
    "trabajar": handler_trabajar, "w": handler_trabajar,
    "crime": handler_crime, "c": handler_crime,
    "daily": handler_daily, "d": handler_daily,
    "depositar": handler_depositar, "dp": handler_depositar,
    "retirar": handler_retirar, "r": handler_retirar,
    "banco": handler_banco, "b": handler_banco,
}

# --- 4. Procesamiento principal ---
def procesar_entrada(mensaje_completo, usuario_id):
    mensaje = mensaje_completo.strip()
    if not mensaje.lower().startswith(PREFIJO):
        return None

    partes = mensaje[len(PREFIJO):].split(maxsplit=1)
    comando = partes[0].lower()
    args = partes if len(partes) > 1 else ""

    if comando in ENRUTADOR_COMANDOS:
        return ENRUTADOR_COMANDOS[comando](args, usuario_id)
    
    return f"❓ Comando no reconocido en la vecindad. Escribe {PREFIJO}menu."

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        msg_test = sys.argv[1]  # <--- Corregido índice [1]
        usr_test = sys.argv[2]  # <--- Corregido índice [2]
        res = procesar_entrada(msg_test, usr_test)
        if res:
            print(res)
    else:
        print("--- PRUEBA RÁPIDA ---")
        print(procesar_entrada(".perfil", "vecino_123"))
