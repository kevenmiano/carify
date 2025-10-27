# Suprimir warning do pkg_resources antes de importar OpenTelemetry
import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from pydantic import ValidationError
import os
import logging
from dotenv import load_dotenv
from carify.swagger import api
from carify.exceptions import BaseError
from carify.proprietarios.routes import proprietario_bp
from carify.observability import init_telemetry, trace_exception

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


load_dotenv()

app = Flask(__name__)
cors = CORS(app)

tracer = init_telemetry(app)

@app.errorhandler(BaseError)
def handle_base_error(error: BaseError):
    context = {
        'endpoint': request.endpoint,
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr
    }

    trace_exception(tracer, error, context)

    return make_response(
        jsonify({'error': error.message}),
        error.status_code
    )

@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    context = {
        'endpoint': request.endpoint,
        'method': request.method,
        'path': request.path,
        'validation_errors': len(error.errors())
    }

    trace_exception(tracer, error, context)

    return make_response(
        jsonify({
            'error': 'Dados inválidos',
            'details': error.errors()
        }),
        400
    )

@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    context = {
        'endpoint': request.endpoint,
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr
    }

    trace_exception(tracer, error, context)

    return make_response(
        jsonify({'error': 'Erro interno do servidor'}),
        500
    )

api.register(app)

app.register_blueprint(proprietario_bp)

@app.route('/')
def index():
    logger.info("Root endpoint accessed", extra={
        'endpoint': '/',
        'method': 'GET',
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'remote_addr': request.remote_addr
    })
    return jsonify({
        'message': 'Carify API',
        'version': '0.1.0',
        'endpoints': {
            'proprietarios': '/proprietarios',
            'health': '/health'
        },
        'docs': {
            'scalar': '/docs/scalar/'
        }
    })

@app.route('/health')
def health():
    logger.info("Health check endpoint accessed", extra={
        'endpoint': '/health',
        'method': 'GET',
        'status': 'ok',
        'remote_addr': request.remote_addr
    })
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    logger.info("Starting Carify API server", extra={
        'host': '0.0.0.0',
        'port': int(os.getenv('PORT', 3000)),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'service': 'carify-api'
    })

    app.run(
        host="0.0.0.0",
        port=int(os.getenv('PORT', 3000)),
        debug=True
    )
