from flask import Flask, request, redirect, jsonify, url_for
import hashlib
import threading
import asyncio

app = Flask(__name__)

# Внутреннее хранилище для URL
url_mapping = {}

# Функция для генерации короткой части URL
def generate_short_id(url):
    return hashlib.sha256(url.encode()).hexdigest()[:6]


@app.route('/', methods=['POST'])
def shorten_url():
    data = request.get_data(as_text=True)
    original_url = data.strip()
    short_id = generate_short_id(original_url)
    url_mapping[short_id] = original_url
    return jsonify({'short_url': short_id}), 201


@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        response = redirect(original_url, code=307)
        return response
    else:
        return jsonify({'error': 'URL not found'}), 404

# Асинхронный вызов
@app.route('/async-call', methods=['GET'])
def async_call():
    result = asyncio.run(async_task())
    return jsonify({'async_result': result})

async def async_task():
    # Имитация асинхронной операции
    await asyncio.sleep(1)
    return 'Асинхронный вызов завершен'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)