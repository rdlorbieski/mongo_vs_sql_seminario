import streamlit as st
import sqlite3
from pymongo import MongoClient
from datetime import datetime

# --- Conexões ---
def conectar_sqlite():
    return sqlite3.connect("escola.db")

def conectar_mongo():
    cliente = MongoClient("mongodb://localhost:27017/")
    return cliente["escola"]

def listar_disciplinas_sqlite():
    conn = conectar_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT id_disciplina, nome FROM Disciplina")
    disciplinas = [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    conn.close()
    return disciplinas

def listar_disciplinas_mongo():
    db = conectar_mongo()
    return [{"id": doc["_id"], "nome": doc.get("nome", "")} for doc in db.disciplinas.find({}, {"_id": 1, "nome": 1})]

def obter_disciplina_mongo(id_disciplina):
    db = conectar_mongo()
    return db.disciplinas.find_one({"_id": id_disciplina})

def get_next_id(collection, field="_id"):
    db = conectar_mongo()
    doc = db[collection].find_one(sort=[(field, -1)])
    return (doc[field] + 1) if doc and field in doc else 1

# --- Streamlit App ---
st.title("Cadastro de Aula")
banco = st.selectbox("Escolha o banco de dados:", ["SQLite", "MongoDB"])
aba = st.radio("O que deseja cadastrar?", ["Nova Aula", "Novo Desempenho"])

# --- Cadastro de Aula ---
if aba == "Nova Aula":
    if banco == "SQLite":
        conn = conectar_sqlite()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id_aula) FROM Aula")
        result = cursor.fetchone()
        id_aula = (result[0] or 0) + 1
        conn.close()
        st.markdown(f"**ID da Aula (auto):** {id_aula}")
    else:
        id_aula = get_next_id("aulas")
        st.markdown(f"**ID da Aula (auto):** {id_aula}")

    disciplinas = listar_disciplinas_sqlite() if banco == "SQLite" else listar_disciplinas_mongo()

    if disciplinas:
        disciplina_selecionada = st.selectbox(
            "Selecione a Disciplina",
            options=disciplinas,
            format_func=lambda d: f"{d['id']} - {d['nome']}"
        )
        id_disciplina = disciplina_selecionada["id"]
    else:
        st.warning("Nenhuma disciplina encontrada no banco de dados.")
        id_disciplina = None

    data_hora = st.text_input("Data e Hora da Aula", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
    nome_turma = st.text_input("Nome da Turma")
    resumo = st.text_area("Resumo da Aula")

    if st.button("Salvar Aula"):
        if banco == "SQLite":
            conn = conectar_sqlite()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Aula VALUES (?, ?, ?, ?, ?, '', '', '')", (id_aula, id_disciplina, data_hora, nome_turma, resumo))
            conn.commit()
            conn.close()
            st.success("Aula salva no SQLite com sucesso!")
        else:
            db = conectar_mongo()
            disciplina = obter_disciplina_mongo(id_disciplina)
            db.aulas.insert_one({
                "_id": id_aula,
                "id_disciplina": id_disciplina,
                "nome_disciplina": disciplina["nome"] if disciplina else "",
                "nome_professor": disciplina["nome_professor"] if disciplina else "",
                "indice_cobertura": disciplina["indice_cobertura"] if disciplina else 0.0,
                "data_hora": data_hora,
                "nome_turma": nome_turma,
                "resumo": resumo,
                "mindmap_path": "",
                "comentarios": "",
                "qualidade_aula": "maxima",
                "transicao_final": ""
            })
            st.success("Aula salva no MongoDB com sucesso!")

# --- Cadastro de Desempenho ---
def listar_ids_alunos_sqlite():
    conn = conectar_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT id_aluno, nome FROM Aluno")
    alunos = [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    conn.close()
    return alunos

def listar_ids_alunos_mongo():
    db = conectar_mongo()
    alunos = [{"id": aluno["_id"], "nome": aluno["nome"]} for aluno in db.alunos.find({}, {"_id": 1, "nome": 1})]
    return alunos

if aba == "Novo Desempenho":
    if banco == "SQLite":
        conn = conectar_sqlite()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id_desempenho) FROM Desempenho")
        result = cursor.fetchone()
        id_desempenho = (result[0] or 0) + 1
        conn.close()
    else:
        id_desempenho = get_next_id("alunos", field="desempenhos.id_desempenho")

    st.markdown(f"**ID do Desempenho (auto):** {id_desempenho}")

    alunos = listar_ids_alunos_sqlite() if banco == "SQLite" else listar_ids_alunos_mongo()

    if alunos:
        aluno_selecionado = st.selectbox(
            "Selecione o Aluno",
            options=alunos,
            format_func=lambda aluno: f"{aluno['id']} - {aluno['nome']}"
        )
        id_aluno = aluno_selecionado["id"]
    else:
        st.warning("Nenhum aluno encontrado no banco de dados.")
        id_aluno = None

    disciplinas = listar_disciplinas_sqlite() if banco == "SQLite" else listar_disciplinas_mongo()

    if disciplinas:
        disciplina_selecionada = st.selectbox(
            "Selecione a Disciplina",
            options=disciplinas,
            format_func=lambda d: f"{d['id']} - {d['nome']}"
        )
        id_disciplina = disciplina_selecionada["id"]
        nome_disciplina = disciplina_selecionada["nome"]
    else:
        st.warning("Nenhuma disciplina encontrada no banco de dados.")
        id_disciplina = None
        nome_disciplina = ""

    nota = st.number_input("Nota", 0, 100)
    tipo = st.text_input("Tipo da Avaliação")
    explicabilidade = st.text_area("Explicabilidade da Nota")

    if st.button("Salvar Desempenho"):
        if not id_aluno:
            st.error("Erro: Nenhum aluno foi selecionado.")
        elif not id_disciplina:
            st.error("Erro: Nenhuma disciplina foi selecionada.")
        else:
            if banco == "SQLite":
                conn = conectar_sqlite()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Desempenho VALUES (?, ?, ?, ?, ?, ?)",
                               (id_desempenho, id_aluno, id_disciplina, nota, tipo, explicabilidade))
                conn.commit()
                conn.close()
                st.success("Desempenho salvo no SQLite com sucesso!")
            else:
                db = conectar_mongo()
                db.alunos.update_one(
                    {"_id": id_aluno},
                    {"$push": {
                        "desempenhos": {
                            "id_desempenho": id_desempenho,
                            "id_disciplina": id_disciplina,
                            "nome_disciplina": nome_disciplina,
                            "nota": nota,
                            "tipo": tipo,
                            "explicabilidade": explicabilidade
                        }
                    }},
                    upsert=True
                )
                st.success("Desempenho salvo no MongoDB com sucesso!")
