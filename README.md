# WebSocketIO
Socket.IO assisted WebSockets for real-time communication between client and server.

This code demonstrates the use of the Socket.IO library in WebSockets to show real-time communication between the client and the server. The server pushes temperature updates (in this case, simulated temperature data) to the client as soon as they are available. This is different from the traditional request-response model where the client has to request data from the server.

## Client Side (HTML Page)
1. `document.addEventListener('DOMContentLoaded', (event) => {...})`: This is an event listener that waits for the HTML document to be fully loaded and parsed, without waiting for stylesheets, images, and subframes to finish loading.
2. `var socket = io.connect('http://' + document.domain + ':' + location.port)`: This line establishes a WebSocket connection to the server using Socket.IO. The connection is made to the current domain and port.
3. `socket.on('temperature', function(msg) {...})`: This is an event listener for the ‘temperature’ event. When the server emits a ‘temperature’ event, the callback function is executed.
4. `document.getElementById('temperature').innerHTML = msg.data`: This line updates the HTML content of the element with the id ‘temperature’ with the data received from the server.

## Server Side (Flask Application)
This is a simple Flask application that uses the Flask-SocketIO extension to emit temperature data to connected clients. The script acts as a server that emits a random temperature value to all connected clients every second. Clients can view this data by navigating to the /temperature route. The temperature data is generated in a background task, so it doesn’t interfere with the handling of client requests. The server runs on host ‘0.0.0.0’ and port 5000.

1. `app = Flask(__name__)` and `socketio = SocketIO(app)`: Creates new instances of the Flask web server and initializes a new instance of Flask-SocketIO. It allows the Flask application to use WebSockets, which provide a persistent connection between the client and the server.
2. `@app.route('/temperature')`: This decorator creates a new route on the web server. When a client navigates to `<your-server-url>/temperature`, the function below this decorator will be executed.
3. `def temperature(): return render_template('temperature.html')`: This function renders the `temperature.html` template when the `/temperature` route is accessed.
4. `def generate_temperature()`: This function generates a random temperature value between 20.0 and 30.0 every second. `socketio.emit('temperature', {'data': str(round(temp,2))})`: This line emits the generated temperature value to all connected clients on the ‘temperature’ channel.
5. `socketio.start_background_task(generate_temperature)`: This line starts the `generate_temperature` function as a background task. This means that the function will run independently of any client requests.
6. `socketio.run(app, debug=True, host='0.0.0.0', port=5000)`: This line runs the Flask web server on host ‘0.0.0.0’ and port 5000. The `debug=True` argument means that the server will provide more detailed error messages if something goes wrong.

## Dependencies (Install via Pip)
1. **flask-socketio**

### Install the following to improve performance
2. **eventlet=0.36.1** -- If this does not work due to `socket.on()` not receiving an event, try the following alternatives:
    - **gevent=24.2.1**
    - **gevent-websocket=0.10.1**
## Launch the server
**python flaskserver.py**

## Viewing at the browser
**http://localhost:5000/temperature**

