Simple game client
------------------

This client is meant to be a quick and easy prototyping tool to test out the core game logic, which should all live on the server.

The client:

- registers a connection with server
- shares the /data/schema with the server, so it can natively access all the game objects and game commands streamed in
- processes user actions and converts them to server commands
- parses the servers responses to update the world view, using interpolation where appropriate
- is very dumb

Requirements
------------

- python2.7
- kivy
- protobuf2
- grpc

Python/kivy combination was chosen because it was cheap and easy to setup, available on most systems, and doesn't require a lot of code to get a lot done. It's also very easy to read and follow, even when you're unfamiliar with the language/toolkit.

For this test client, game performance is not critical. So I prioritised setup and speed of development over raw performance.

Installation
------------

# install core dependencies
apt install python-kivy python protobuf-python

# install gRPC
python -m pip install --upgrade pip
python -m pip install grpcio
python -m pip install grpcio-tools
