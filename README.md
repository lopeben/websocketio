# websocketio
Socket.IO assisted WebSockets for real-time communication between client and server.

This code demonstrates the use of Socket.IO library in WebSockets to show real-time communication between the client and the server. 
The server pushes temperature updates (in this case, simulated temperature data) to the client as soon as they are available. 
This is different from the traditional request-response model where the client has to request data from the server.

## Client side (HTML Page)

1. document.addEventListener('DOMContentLoaded', (event) => {...}): This is an event listener that waits for the HTML document to be fully loaded and parsed, without waiting for stylesheets, images, and subframes to finish loading.

2. var socket = io.connect('http://' + document.domain + ':' + location.port): This line establishes a WebSocket connection to the server using Socket.IO. The connection is made to the current domain and port.

3. socket.on('temperature', function(msg) {...}): This is an event listener for the ‘temperature’ event. When the server emits a ‘temperature’ event, the callback function is executed.

4. document.getElementById('temperature').innerHTML = msg.data: This line updates the HTML content of the element with the id ‘temperature’ with the data received from the server.



