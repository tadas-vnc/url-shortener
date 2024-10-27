# app.py
from flask import Flask, request, jsonify, redirect
from database import add_url, get_url, check_password, alias_exists
import random
import string
import sqlite3
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app)
def is_valid_link(link):
    if(link is None):
        return False
    link_regex = r"^(https?://.{1,995})$"
    return bool(re.match(link_regex, link))

def is_valid_string(s):
    if(s is None):
        return False
    string_regex = r"^[a-zA-Z0-9_]{2,16}$"
    return bool(re.match(string_regex, s))

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
    alias = alias.lower()
    password = data.get('password', generate_random_password())
    if(not is_valid_string(alias)):
        return jsonify({'error': 'Custom alias is not a valid, only lating letters, numbers and underscore is allowed.'}), 400
    if(not is_valid_string(password)):
        return jsonify({'error': 'Custom password is not a valid, only lating letters, numbers and underscore is allowed.'}), 400
    if not source_url:
        return jsonify({'error': 'source_url is required'}), 400

    if not is_valid_link(source_url):
        return jsonify({'error': 'Source URL is not valid, source URL must start with "http" and not exceed 1000 character limit.'}), 400

    if alias_exists(alias):
        return jsonify({'error': 'Alias already taken, please choose a different alias'}), 400

    add_url(source_url, alias, password)
    short_url = f"{request.scheme}://{request.host}/{alias}" 
    return jsonify({
        'short_url': short_url,
        'alias': alias,
        'password': password,
        'success': 'Short url created successfully.'
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
    alias = alias.lower()
    password = data.get('password')
    new_source_url = data.get('new_source_url')
    print(new_source_url)
    new_alias = data.get('new_alias')
    new_password = data.get('new_password')
    if new_source_url and not is_valid_link(new_source_url):
        return jsonify({'error': 'Source URL is not valid, source URL must start with "http" and not exceed 1000 character limit.'}), 400
    if not alias or not password:
        return jsonify({'error': 'alias and password are required'}), 400

    if not check_password(alias, password):
        return jsonify({'error': 'Invalid password or alias'}), 403

    if new_alias and alias_exists(new_alias) and new_alias != alias:
        new_alias = new_alias.lower()
        return jsonify({'error': 'New alias already taken, please choose a different alias'}), 400
    if new_alias:
        if(not is_valid_string(new_alias)):
            return jsonify({'error': 'Custom alias is not a valid, only lating letters, numbers and underscore is allowed.'}), 400
    
    if(new_password and not is_valid_string(new_password)):
        return jsonify({'error': 'Custom password is not a valid, only lating letters, numbers and underscore is allowed.'}), 400
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
        return jsonify({'error': 'Invalid password or alias'}), 403

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM urls WHERE short_url = ?', (alias,))
    conn.commit()
    conn.close()

    return jsonify({'success': 'URL deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port="5000")