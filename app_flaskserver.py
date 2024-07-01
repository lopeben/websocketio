import time
import random
import logging
from flask_socketio import SocketIO, emit
from flask import Flask, render_template



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.logger.setLevel(logging.INFO)  # or logging.DEBUG for debug level messages
# socketio = SocketIO(app)
# socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")
socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True)



@app.route('/temperature')
def temperature():
    return render_template('temperature.html')



def generate_temperature():
    while True:

        try:
            temp = random.uniform(20.0, 30.0)  # simulated data source
            socketio.emit('temperature', {'data': str(round(temp,2))}) #, broadcast=True)
            app.logger.info("Event emitted")
        
        except Exception as e:
            app.logger.error(f"Error in generate_temperature: {e}")

        socketio.sleep(1)



if __name__ == '__main__':
    print("Staring server")
    socketio.start_background_task(generate_temperature)

    # Development Server Settings
    # socketio.run(app, debug=True, host='0.0.0.0', port=8000)
    # socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
    
    # Production Server Setting
    socketio.run(app, host='0.0.0.0', port=80)
    # socketio.run(app, host='0.0.0.0', port=5000)
    