from flask import Blueprint, request, jsonify, make_response
from returns.result import Success, Failure
import logging
from carify.swagger import api
from carify.exceptions import ProprietarioNaoEncontradoException
from carify.proprietarios.dtos import CreateProprietarioDto
from .repositories import ProprietarioRepositoryInMemory
from .usecases import CreateProprietarioUseCase

logger = logging.getLogger(__name__)

proprietario_bp = Blueprint('proprietario', __name__, url_prefix='/proprietarios')

repository = ProprietarioRepositoryInMemory()


@proprietario_bp.route('', methods=['POST'])
@api.validate(json=CreateProprietarioDto, tags=['Proprietários'])
def create_proprietario():
    """
    Criar um novo proprietário

    Validações automáticas do Pydantic:
    - Nome: 3-100 caracteres
    - Email: formato válido
    - Telefone: 10-15 dígitos
    - CPF: exatamente 11 dígitos (único no sistema)
    """
    logger.info("Iniciando criação de proprietário", extra={
        "endpoint": "POST /proprietarios",
        "method": "POST"
    })

    # Spectree já validou e colocou em request.context.json
    data: CreateProprietarioDto = request.context.json

    usecase = CreateProprietarioUseCase(repository)
    result = usecase.execute(
        nome=data.nome,
        email=data.email,
        telefone=data.telefone,
        cpf=data.cpf
    )

    match result:
        case Failure(error):
            logger.error("Erro ao criar proprietário", extra={
                "error": str(error),
                "cpf": data.cpf,
                "email": data.email
            })
            raise error
        case Success(proprietario):
            logger.info("Proprietário criado com sucesso", extra={
                "proprietario_id": proprietario.id,
                "cpf": proprietario.cpf,
                "email": proprietario.email
            })
            return make_response(jsonify(proprietario.model_dump()), 201)


@proprietario_bp.route('', methods=['GET'])
@api.validate(tags=['Proprietários'])
def list_proprietarios():
    """
    Listar todos os proprietários

    Retorna uma lista com todos os proprietários cadastrados.
    """
    logger.info("Listando proprietários", extra={
        "endpoint": "GET /proprietarios",
        "method": "GET",
        "remote_addr": request.remote_addr
    })

    proprietarios = list(repository.proprietarios.values())

    logger.info("Proprietários listados com sucesso", extra={
        "total_proprietarios": len(proprietarios)
    })

    return jsonify({
        'data': [p.model_dump() for p in proprietarios],
        'total': len(proprietarios)
    })


@proprietario_bp.route('/<int:id>', methods=['GET'])
@api.validate(tags=['Proprietários'])
def get_proprietario(id):
    """
    Buscar um proprietário por ID

    Retorna 404 se o proprietário não for encontrado.
    """
    logger.info("Buscando proprietário por ID", extra={
        "endpoint": f"GET /proprietarios/{id}",
        "method": "GET",
        "proprietario_id": id,
        "remote_addr": request.remote_addr
    })

    proprietario = repository.proprietarios.get(id)

    if not proprietario:
        logger.warning("Proprietário não encontrado", extra={
            "proprietario_id": id
        })
        raise ProprietarioNaoEncontradoException(id)

    logger.info("Proprietário encontrado", extra={
        "proprietario_id": id,
        "cpf": proprietario.cpf
    })

    return jsonify(proprietario.model_dump())
