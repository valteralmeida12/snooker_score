import os
import json
from flask import Flask, render_template, request, session, redirect, url_for
from flask import jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# Create and env variable with the secret key
app.secret_key = os.getenv('SECRET_KEY')
socketio = SocketIO(app)

# Sample initial scoreboard data
scoreboard_data = {'player1': {'name': 'Player 1', 'games_won': 0, 'score': 0},
                   'player2': {'name': 'Player 2', 'games_won': 0, 'score': 0}}

# Path to the JSON file storing login credentials
credentials_file = 'credentials.json'

def validate_credentials(username, password):
    with open(credentials_file) as f:
        credentials = json.load(f)
    return username in credentials and credentials[username] == password

@app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return render_template('view.html', scoreboard=scoreboard_data)
    return redirect(url_for('edit'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('edit'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        scoreboard_data['player1']['name'] = request.form['player1_name']
        scoreboard_data['player1']['games_won'] = int(request.form['player1_games_won'])
        scoreboard_data['player1']['score'] = int(request.form['player1_score'])

        scoreboard_data['player2']['name'] = request.form['player2_name']
        scoreboard_data['player2']['games_won'] = int(request.form['player2_games_won'])
        scoreboard_data['player2']['score'] = int(request.form['player2_score'])
    return render_template('edit.html', scoreboard=scoreboard_data)

@app.route('/update_info', methods=['POST'])
def update_info():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    scoreboard_data['player1']['name'] = request.form['player1_name']
    scoreboard_data['player1']['games_won'] = int(request.form['player1_games_won'])
    scoreboard_data['player1']['score'] = int(request.form['player1_score'])

    scoreboard_data['player2']['name'] = request.form['player2_name']
    scoreboard_data['player2']['games_won'] = int(request.form['player2_games_won'])
    scoreboard_data['player2']['score'] = int(request.form['player2_score'])

    return redirect(url_for('edit'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@socketio.on('update_info')
def handle_score_update(data):
    if 'logged_in' in session and session['logged_in']:
        scoreboard_data['player1']['games_won'] = data['player1_games_won']
        scoreboard_data['player2']['games_won'] = data['player2_games_won']
        scoreboard_data['player1']['score'] = data['player1_score']
        scoreboard_data['player2']['score'] = data['player2_score']
        emit('scores_updated', scoreboard_data, broadcast=True)

@app.route('/scoreboard_data', methods=['GET'])
def get_scoreboard_data():
    return jsonify(scoreboard_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)




