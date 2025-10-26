from dataclasses import dataclass
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'), load_dotenv=True)
