from flask import Flask, request, jsonify
import os
#import pymysql # MySQL
import psycopg2 # PostgreSQL
import datetime as dt
from dotenv import load_dotenv
import requests

load_dotenv()

# To run Flask app on terminal: flask --app webmessage run

app = Flask(__name__) # Create a Flask application instance

# WEB root endpoint
@app.route('/')
def hello_world():
    now = str(dt.datetime.now())
    return 'Hello from Flask! ' + now

@app.route('/core')
def core():
    now = str(dt.datetime.now())
    msg = {"status":"ok",  "now":now, "message":"Vai Corinthians!!"} # dict = JSON

    return msg

@app.route('/cat')
def cat():
    CAT_URL="https://catfact.ninja/fact"
    cat_json = requests.get(CAT_URL).json()
    cat_json["now"] = str(dt.datetime.now())
    cat_json["from"] = "PUC-SP LAB 213"
    return cat_json

@app.route('/db')
def database_info():
    try:
        # Force the correct values (good for debugging)
        host = os.getenv('PGHOST')
        user = os.getenv('PGUSER')
        password = os.getenv('PGPASSWORD')
        db = os.getenv('PGDATABASE')

        print(f"Connecting to: {host}")   # This will help you debug

        # DB connection to Neon PostgreSQL
        connection = psycopg2.connect(
                         dbname=db,
                         user=user,
                         password=password,
                         host=host,
                         # slmode="require",
                         port="5432"
        )
        # Neon uses the default PostgreSQL port, 5432, for both pooled and direct connections

        with connection.cursor() as cursor:
            cursor.execute("select version() as version, now() as now")
            result = cursor.fetchone()

        connection.close()

        return f"""
        <h2>✅ Database Connection Successful</h2>
        <p><strong>Host:</strong> {host}</p>
        <p><strong>PostgreSQL Version:</strong> {result[0]}</p>
        <p><strong>DB Server Time:</strong> {result[1]}</p>
        <p><strong>WEB Server Time:</strong> {dt.datetime.now()}</p>
        """

    except Exception as e:
        return f"""
        <h2>❌ Connection Failed</h2>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Host Being Used:</strong> {host}</p>
        <p><strong>WEB Server Time:</strong> {dt.datetime.now()}</p>
        <hr>
        <p>Make sure your .env file is correctly loaded.</p>
        """, 500

@app.route('/save_message', methods=['POST'])
def save_message():
    try:
        # Force the correct values (good for debugging)
        host = os.getenv('PGHOST')
        user = os.getenv('PGUSER')
        password = os.getenv('PGPASSWORD')
        db = os.getenv('PGDATABASE')

        # Get the message from JSON payload
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field in JSON"}), 400

        message_text = data['message'].strip()
        if not message_text:
            return jsonify({"error": "Message cannot be empty"}), 400

        print(f"Connecting to: {host}")   # This will help you debug

        # DB connection to Neon PostgreSQL
        connection = psycopg2.connect(
                         dbname=db,
                         user=user,
                         password=password,
                         host=host,
                         # slmode="require",
                         port="5432"
        )

        with connection.cursor() as cursor:
            sql = "INSERT INTO web_message (message) VALUES (%s)"
            cursor.execute(sql, (message_text,))
            connection.commit()

            new_id = cursor.lastrowid

        connection.close()

        return jsonify({
            "status": "success",
            "message": "Message saved successfully",
            "id": new_id,
            "saved_message": message_text,
            "now": str(dt.datetime.now())
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "now": str(dt.datetime.now())
        }), 500

@app.route('/message/<int:message_id>')
def get_message(message_id):
    try:
        # Force the correct values (good for debugging)
        host = os.getenv('PGHOST')
        user = os.getenv('PGUSER')
        password = os.getenv('PGPASSWORD')
        db = os.getenv('PGDATABASE')

        print(f"Connecting to: {host}")   # This will help you debug

        # DB connection to Neon PostgreSQL
        connection = psycopg2.connect(
                         dbname=db,
                         user=user,
                         password=password,
                         host=host,
                         # slmode="require",
                         port="5432"
        )

        with connection.cursor() as cursor:
            sql = """
                SELECT id, message, created_date
                FROM web_message
                WHERE id = %s
            """
            cursor.execute(sql, (message_id,))
            message = cursor.fetchone()

        connection.close()

        if message:
            return jsonify({
                "status": "success",
                "data": {
                    "id": message[0],
                    "message": message[1],
                    "created_date": message[2].isoformat() if message[2] else None
                }
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Message with id {message_id} not found",
                "now": str(dt.datetime.now())
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "now": str(dt.datetime.now())
        }), 500