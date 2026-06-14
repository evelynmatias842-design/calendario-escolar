from flask import Flask, render_template
import urllib.request
import urllib.parse

app = Flask(__name__)

# 🔴 PEGA TUS DATOS DE TELEGRAM AQUÍ EN MEDIO DE LAS COMILLAS
TELEGRAM_TOKEN = "AQUÍ_PEGA_TU_TOKEN_DE_TELEGRAM"
CHAT_ID = "AQUÍ_PEGA_TU_CHAT_ID"

def enviar_aviso_telegram():
    """Función para enviar un mensaje automático a Telegram"""
    try:
        mensaje = "🚀 ¡Alguien acaba de entrar a visitar tu Calendario Escolar!"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        # Preparamos los datos para enviar
        valores = {"chat_id": CHAT_ID, "text": mensaje}
        datos = urllib.parse.urlencode(valores).encode("utf-8")
        
        # Hacemos la petición segura a Telegram
        req = urllib.request.Request(url, data=datos)
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")

@app.route('/')
def index():
    # Cada vez que alguien entra a la ruta principal, se activa el aviso
    enviar_aviso_telegram()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
