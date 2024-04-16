import time
import random
from flask_socketio import SocketIO
from flask import Flask, render_template



app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/temperature')
def temperature():
    return render_template('temperature.html')


def generate_temperature():
    while True:
        
        temp = random.uniform(20.0, 30.0)  # simulated data source
        
        socketio.emit('temperature', {'data': str(round(temp,2))})
        
        time.sleep(1)


if __name__ == '__main__':
    socketio.start_background_task(generate_temperature)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
