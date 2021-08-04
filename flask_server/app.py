import socket

from flask import Flask
from main.main import main

app = Flask(__name__)

app.register_blueprint(main)


if __name__ == "__main__":
    for port in range(5000, 6000):
        try:
            app.run(host='0.0.0.0', port=port, debug=True)
            break
        except socket.error:
            pass
