from flask import Flask, render_template, request, jsonify
import json
import os
import uuid

app = Flask(__name__)
DATA_FILE = 'events.json'

# Función para leer los eventos guardados
def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Función para guardar los eventos
def save_events(events):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener los eventos en el calendario
@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(load_events())

# Ruta para añadir un nuevo evento
@app.route('/api/events', methods=['POST'])
def add_event():
    data = request.json
    events = load_events()
    
    # Código de colores personalizado
    colors = {
        'tarea': '#3b82f6',     # Azul
        'examen': '#ef4444',    # Rojo
        'personal': '#10b981'   # Verde
    }
    
    new_event = {
        'id': str(uuid.uuid4()),
        'title': data.get('title'),
        'start': data.get('start'),  # Formato YYYY-MM-DD
        'category': data.get('category'),
        'color': colors.get(data.get('category'), '#6b7280'),
        'urgent': data.get('urgent', False)
    }
    
    events.append(new_event)
    save_events(events)
    return jsonify(new_event), 201

# Ruta para eliminar un evento si haces clic en él
@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events = load_events()
    events = [e for e in events if e['id'] != event_id]
    save_events(events)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
