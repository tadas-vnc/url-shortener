# app.py
from flask import Flask, request, jsonify, redirect
from database import add_url, get_url, check_password, alias_exists
import random
import string
import sqlite3
from gevent.pywsgi import WSGIServer
app = Flask(__name__)

def generate_random_alias(length=6):
    alias = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    while alias_exists(alias):  
        alias = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return alias

def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    source_url = data.get('source_url')
    alias = data.get('alias', generate_random_alias())
    password = data.get('password', generate_random_password())

    if not source_url:
        return jsonify({'error': 'source_url is required'}), 400

    if alias_exists(alias):
        return jsonify({'error': 'Alias already taken, please choose a different alias'}), 400

    add_url(source_url, alias, password)
    short_url = f"{request.scheme}://{request.host}/{alias}" 
    return jsonify({
        'short_url': short_url,
        'alias': alias,
        'password': password
    }), 201

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    source_url = get_url(short_url)
    if source_url:
        return redirect(source_url)
    return jsonify({'error': 'URL not found'}), 404

@app.route('/update', methods=['POST'])
def update_url():
    data = request.json
    alias = data.get('alias')
    password = data.get('password')
    new_source_url = data.get('new_source_url')
    new_alias = data.get('new_alias')
    new_password = data.get('new_password')

    if not alias or not password:
        return jsonify({'error': 'alias and password are required'}), 400

    if not check_password(alias, password):
        return jsonify({'error': 'Invalid password'}), 403

    if new_alias and alias_exists(new_alias):
        return jsonify({'error': 'New alias already taken, please choose a different alias'}), 400

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if new_alias:
        c.execute('UPDATE urls SET short_url = ? WHERE short_url = ?', (new_alias, alias))
        alias = new_alias 
    if new_source_url:
        c.execute('UPDATE urls SET source_url = ? WHERE short_url = ?', (new_source_url, alias))
    if new_password:
        c.execute('UPDATE urls SET password = ? WHERE short_url = ?', (new_password, alias))
    conn.commit()
    conn.close()

    return jsonify({'success': 'URL updated successfully'})

@app.route('/delete', methods=['DELETE'])
def delete_url():
    data = request.json
    alias = data.get('alias')
    password = data.get('password')

    if not alias or not password:
        return jsonify({'error': 'alias and password are required'}), 400

    if not check_password(alias, password):
        return jsonify({'error': 'Invalid password'}), 403

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM urls WHERE short_url = ?', (alias,))
    conn.commit()
    conn.close()

    return jsonify({'success': 'URL deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port="5000")