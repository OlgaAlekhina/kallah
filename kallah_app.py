from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Lock
from kalakh_web1 import Board, Player, BOTTOM_PLAYER


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('test')
def handle_test(data):
    print('Data: ', data)
    well_list = data.get('well_list')
    wells = []
    for well in well_list:
        wells.append(int(well))
    print(wells)
    my_board = Board(wells)
    player = Player(BOTTOM_PLAYER, 2)
    best_move = player.best_move(my_board)
    print(best_move)
    emit('wow', {'data': best_move})

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)