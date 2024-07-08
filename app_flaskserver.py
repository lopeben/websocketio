import time
import random
import logging
import platform
from flask_socketio import SocketIO, emit
from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.logger.setLevel(logging.INFO)  # or logging.DEBUG for debug level messages

def is_mac():
    return platform.system() == 'Darwin'

if is_mac():
    socketio = SocketIO(app) # Use this when debugging in mac
else:
    socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True)


@app.route('/temperature')
def temperature():
    return render_template('temperature.html')


@socketio.on('request_stored_data')
def handle_get_initial_data():
    try:
        with open('data.txt', 'r') as f:
            temp = f.read()
            humd = temp
    except Exception as e:
        app.logger.error(f"Error in reading data: {e}")
        temp = "No data available"

    data_dict = {"temperature": temp, "humidity": humd}
    socketio.emit('message', data_dict)


@socketio.on('card_click')
def handle_card_click():
    app.logger.info("Card click handler")
    

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
                humd = temp
            data_dict = {"temperature": temp, "humidity": humd}
            socketio.emit('message', data_dict)
            app.logger.info("Event emitted")
        except Exception as e:
            app.logger.error(f"Error in generate_temperature: {e}")
        socketio.sleep(30)



if __name__ == '__main__':
    print("Staring server")
    socketio.start_background_task(generate_random_data)
    socketio.start_background_task(generate_temperature)

    if is_mac():
        # Debug setting WSGI
        socketio.run(app, debug=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    else:
        # Production setting WSGI
        socketio.run(app, debug=False, host='0.0.0.0', port=80)

