import time
import requests
import waitress
from flask import Flask, request

app = Flask('PingPong')

games = {}
time_out = 5000
ms = 1 / 1000


@app.route('/create', methods=['POST'])
def create():
    data = request.json

    reply = 'No one want to play with you', 400

    try:
        if data['server_name']:
            games[data['server_name']] = {
                'ping': True,
                'pong': False
            }
            print(f'Creating Game {data["server_name"]}')

            cpt = 0

            while cpt < time_out * 2:
                if games[data['server_name']]['pong']:
                    return 'Someone want to play with you!', 200

    except KeyError as e:
        reply = f'Bad Json... {e}', 422
    except Exception as e:
        reply = f'Not OK... {e}', 400

    return reply


@app.route('/ping/<server>', methods=['PUT'])
def ping(server):
    error = ''
    try:
        games[server]['ping'] = True
        games[server]['pong'] = False

        cpt = 0

        while cpt < time_out:
            if games[server]['pong']:
                return 'pong', 200

            cpt += 1
            time.sleep(ms)

    except Exception as e:
        error = e

    return f'ping? {error}', 400


@app.route('/pong/<server>', methods=['PUT'])
def pong(server):
    error = ''
    try:
        games[server]['pong'] = True
        games[server]['ping'] = False
        cpt = 0

        while cpt < time_out:
            if games[server]['ping']:
                return 'ping', 200

            cpt += 1
            time.sleep(ms)
    except Exception as e:
        error = e

    return f'ping? {error}', 400


if __name__ == '__main__':
    import socket

    print(f'Server Local IP : {socket.gethostbyname(socket.gethostname())}')
    print(f'Server External IP : {requests.get("http://ip.42.pl/raw").text}')
    waitress.serve(app, host='0.0.0.0', port=80)
