import socketio


sio = socketio.Client()


@sio.event
def connect():
    print("Connected to the server")


@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.on('new_json')
def on_new_json(data):
    print(f"Received data: {data}")

sio.connect('http://localhost:7777')

# Wait for events
sio.wait()
