from flask import Flask, render_template, jsonify, request
import urllib.request
import urllib.parse
import json
import os

app = Flask(__name__, template_folder='templates')

# CONFIGURACIÓN DE TELEGRAM
TELEGRAM_TOKEN = "8896103095:AAHQP6eONVkdkxdMgE4X1sccMomRrnbGh2s"
CHAT_ID = "61814697148"
ARCHIVO_DATOS = "eventos.json"

def enviar_aviso_telegram(mensaje):
    try:
        mensaje_seguro = urllib.parse.quote(mensaje)
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje_seguro}"
        urllib.request.urlopen(url)
    except:
        pass

@app.route('/')
def home():
    # 🚀 Esta línea es la que le ordena al bot avisarte de inmediato
    enviar_aviso_telegram("🚀 ¡Alguien acaba de entrar a visitar tu Calendario Escolar!")
    return render_template('index.html')

@app.route('/api/events', methods=['GET'])
def obtener_eventos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
            try:
                return jsonify(json.load(f)), 200
            except:
                return jsonify([]), 200
    return jsonify([]), 200

@app.route('/api/events', methods=['POST'])
def guardar_evento():
    try:
        datos = request.get_json()
        eventos = []
        if os.path.exists(ARCHIVO_DATOS):
            with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                try:
                    eventos = json.load(f)
                except:
                    eventos = []
        
        eventos.append(datos)
        
        with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
            json.dump(eventos, f, ensure_ascii=False, indent=4)
            
        titulo = datos.get('title', 'Sin título')
        enviar_aviso_telegram(f"📢 ¡Nuevo evento guardado!: {titulo}")
        return jsonify({"status": "success", "message": "Evento guardado con éxito"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
