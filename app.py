import os
import Flask  # (o las librerías que ya tengas arriba)
import urllib.request
import urllib.parse
from flask import Flask, render_template, jsonify, request
import urllib.request
import urllib.parse
import json
import os

# Configuración de Flask
app = Flask(__name__, template_folder='templates')

# 🔴 CONFIGURACIÓN DE TELEGRAM (Pon tu Token dentro de las comillas)
TELEGRAM_TOKEN = "8896103095:AAHQP6eONVkdkxdMgE4X1sccMomRrnbGh2s"
CHAT_ID = "6814697148"
ARCHIVO_DATOS = "eventos.json"
def enviar_aviso_telegram(mensaje):
    try:
        mensaje_seguro = urllib.parse.quote(mensaje)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje_seguro}"
        urllib.request.urlopen(url)
       @app.route('/api/events', methods=['POST'])
        # <-- Mira cómo está escrito aquí
def guardar_evento():
    # ... tu código para guardar el json ...
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")
        # ARMA LA URL USANDO EL MENSAJE SEGURO
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje_seguro}"
        
        # ENVÍA EL MENSAJE
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")
        # CONVIERTE LOS ESPACIOS Y ACENTOS EN TEXTO SEGURO PARA URL
        mensaje_seguro = urllib.parse.quote(mensaje)
        
        # ARMA LA URL USANDO EL MENSAJE SEGURO
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje_seguro}"
        
        # ENVÍA EL MENSAJE
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")
        if "AQUÍ_PEGA" in TELEGRAM_TOKEN or not TELEGRAM_TOKEN:
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        valores = {"chat_id": CHAT_ID, "text": mensaje}
        datos = urllib.parse.urlencode(valores).encode("utf-8")
        req = urllib.request.Request(url, data=datos)
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error de Telegram: {e}")

def cargar_eventos_guardados():
    """Lee las tareas guardadas en el archivo JSON"""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_eventos_en_archivo(eventos):
    """Escribe las tareas en el archivo JSON"""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    enviar_aviso_telegram("🚀 ¡Alguien acaba de entrar a visitar tu Calendario Escolar!")
    return render_template('index.html')

# 📡 RUTA 1: Enviar los eventos guardados al calendario de la pantalla
@app.route('/api/eventos', methods=['GET'])
def obtener_eventos():
    return jsonify(cargar_eventos_guardados())

# 📡 RUTA 2: Recibir un nuevo evento desde la pantalla y guardarlo
@app.route('/api/eventos', methods=['POST'])
def guardar_evento():
    nuevo_evento = request.get_json()
    eventos = cargar_eventos_guardados()
    eventos.append(nuevo_evento)
    guardar_eventos_en_archivo(eventos)
    
    # Te avisa a tu Telegram qué tarea o examen acaban de anotar
    enviar_aviso_telegram(f"📅 ¡Nuevo evento agregado!: '{nuevo_evento.get('title')}' para el día {nuevo_evento.get('start')}")
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
