import time
import random
import logging
from flask_socketio import SocketIO, emit
from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.logger.setLevel(logging.INFO)  # or logging.DEBUG for debug level messages
socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True)


@app.route('/temperature')
def temperature():
    return render_template('temperature.html')


@socketio.on('request_stored_data')
def handle_get_initial_data():
    try:
        with open('data.txt', 'r') as f:
            temp = f.read()
    except Exception as e:
        app.logger.error(f"Error in reading data: {e}")
        temp = "No data available"
    socketio.emit('temperature', {'data': temp})


def generate_random_data():
    while True:
        try:
            temp = random.uniform(20.0, 30.0)  # simulated data source
            with open('data.txt', 'w') as f:
                f.write(str(round(temp,2)))
            app.logger.info("Data written to file")
        except Exception as e:
            app.logger.error(f"Error in write_random_data: {e}")
        socketio.sleep(60)


def generate_temperature():
    while True:
        try:
            with open('data.txt', 'r') as f:
                temp = f.read()
            socketio.emit('temperature', {'data': temp}) #, broadcast=True)
            app.logger.info("Event emitted")
        except Exception as e:
            app.logger.error(f"Error in generate_temperature: {e}")
        socketio.sleep(30)



if __name__ == '__main__':
    print("Staring server")
    socketio.start_background_task(generate_random_data)
    socketio.start_background_task(generate_temperature)
    
    # Development Server Settings
    # socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)

    socketio.run(app, host='0.0.0.0', port=80)
    