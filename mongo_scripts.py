from pymongo import MongoClient


def conectar_mongo():
    """
    Conecta ao banco de dados MongoDB e retorna o objeto de conexão com a base 'escola'.
    """
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["escola"]
    return db


def criar_collections_mongo():
    """
    Cria índices necessários nas coleções MongoDB.
    Não cria índices no campo '_id', pois eles são criados automaticamente.
    """
    db = conectar_mongo()

    # Criação de índices em campos frequentemente utilizados para filtros ou associações
    db.aulas.create_index("nome_disciplina")  # Índice no campo "nome_disciplina" da coleção aulas
    db.aluno_aula.create_index("id_aluno")  # Índice no campo "id_aluno" da coleção aluno_aula
    db.checklists.create_index("id_entidade")  # Índice no campo "id_entidade" da coleção checklists
    db.disciplinas.create_index("nome")  # Índice no campo "nome" da coleção disciplinas


def inserir_dados_mongo():
    """
    Insere os dados iniciais no banco de dados MongoDB para as coleções disciplinas, alunos, aulas,
    aluno_aula e checklists.
    """
    db = conectar_mongo()

    # Inserção de dados na coleção disciplinas
    db.disciplinas.insert_one({
        "_id": 1,
        "nome": "Matemática",
        "nome_professor": "Prof. Silva",
        "indice_cobertura": 0.9
    })

    # Inserção de dados na coleção alunos
    db.alunos.insert_one({
        "_id": 1,
        "nome": "João",
        "perfil": "engajado",
        "desempenhos": [
            {
                "id_disciplina": 1,
                "nome_disciplina": "Matemática",
                "nota": 95,
                "tipo": "prova final",
                "explicabilidade": "erros por distração"
            }
        ]
    })

    # Inserção de dados na coleção aulas
    db.aulas.insert_one({
        "_id": 1,
        "id_disciplina": 1,
        "nome_disciplina": "Matemática",
        "nome_professor": "Prof. Silva",
        "indice_cobertura": 0.9,
        "data_hora": "2025-04-06 10:00",
        "nome_turma": "Turma A",
        "resumo": "Introdução ao Álgebra",
        "mindmap_path": "",
        "comentarios": "",
        "transicao_final": ""
    })

    # Inserção de dados na coleção aluno_aula
    db.aluno_aula.insert_one({
        "_id": 1,
        "id_aluno": 1,
        "id_aula": 1,
        "esteve_presente": True,
        "comportamento": "ativo"
    })

    # Inserção de dados na coleção checklists
    db.checklists.insert_one({
        "_id": 1,
        "id_entidade": 1,
        "tipo": "aula",
        "topico": "usou quadro branco",
        "aconteceu": True
    })
