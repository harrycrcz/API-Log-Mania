from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)


conn = psycopg2.connect(
    dbname="logs",
    user="postgres",
    password="password",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        client VARCHAR(50),
        event VARCHAR(50),
        description TEXT,
        timestamp TIMESTAMP
    )
''')
conn.commit()

# pa recibir la variable de entorno:
API_KEY = os.getenv("API_KEY")


@app.route('/logs', methods=['POST'])
def receive_logs():
    api_key = request.headers.get('API-Key')
    if api_key != API_KEY:
        return jsonify({'error': 'Invalid API key'}), 403

    data = request.json
    client = data['client']
    event = data['event']
    description = data['description']
    timestamp = data['timestamp']

    cur.execute('''
        INSERT INTO logs (client, event, description, timestamp)
        VALUES (%s, %s, %s, %s)
    ''', (client, event, description, timestamp))
    conn.commit()

    return jsonify({'message': 'Log received'}), 201


@app.route('/logs', methods=['GET'])
def get_logs():
    event_type = request.args.get('event')
    timestamp = request.args.get('timestamp')

    query = 'SELECT * FROM logs WHERE 1=1'
    params = []

    if event_type:
        query += ' AND event=%s'
        params.append(event_type)
    if timestamp:
        query += ' AND timestamp=%s'
        params.append(timestamp)

    cur.execute(query, tuple(params))
    logs = cur.fetchall()

    return jsonify(logs), 200


if __name__ == '__main__':
    app.run(debug=True)
