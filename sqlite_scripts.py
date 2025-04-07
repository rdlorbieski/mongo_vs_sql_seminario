import sqlite3


def conectar_sqlite(nome_banco="escola.db"):
    """
    Conecta ao banco de dados SQLite.
    """
    return sqlite3.connect(nome_banco)


def criar_tabelas_sqlite():
    """
    Cria todas as tabelas do banco de dados SQLite.
    """
    try:
        with conectar_sqlite() as conn:
            cursor = conn.cursor()

            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Disciplina (
                id_disciplina INTEGER PRIMARY KEY,
                nome TEXT,
                nome_professor TEXT,
                indice_cobertura REAL
            );

            CREATE TABLE IF NOT EXISTS Aula (
                id_aula INTEGER PRIMARY KEY,
                id_disciplina INTEGER,
                data_hora TEXT,
                nome_turma TEXT,
                resumo TEXT,
                mindmap_path TEXT,
                comentarios TEXT,
                transicao_final TEXT,
                FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina)
            );

            CREATE TABLE IF NOT EXISTS Aluno (
                id_aluno INTEGER PRIMARY KEY,
                nome TEXT,
                perfil TEXT
            );

            CREATE TABLE IF NOT EXISTS AlunoAula (
                id_aula INTEGER,
                id_aluno INTEGER,
                esteve_presente BOOLEAN,
                comportamento TEXT,
                PRIMARY KEY (id_aula, id_aluno),
                FOREIGN KEY (id_aula) REFERENCES Aula(id_aula),
                FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
            );

            CREATE TABLE IF NOT EXISTS Desempenho (
                id_desempenho INTEGER PRIMARY KEY,
                id_aluno INTEGER,
                id_disciplina INTEGER,
                nota INTEGER,
                tipo TEXT,
                explicabilidade TEXT,
                FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
                FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina)
            );

            CREATE TABLE IF NOT EXISTS Checklist (
                id_checklist INTEGER PRIMARY KEY,
                id_entidade INTEGER,
                tipo TEXT,
                topico TEXT,
                aconteceu BOOLEAN
            );
            """)
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


def inserir_dados_sqlite():
    """
    Insere dados nas tabelas do banco SQLite.
    Evita duplicidades ao verificar se os registros já existem.
    """
    try:
        with conectar_sqlite() as conn:
            cursor = conn.cursor()

            # Inserir na tabela Disciplina
            cursor.execute("INSERT OR IGNORE INTO Disciplina VALUES (?, ?, ?, ?)",
                           (1, 'Matemática', 'Prof. Silva', 0.9))

            # Inserir na tabela Aluno
            cursor.execute("INSERT OR IGNORE INTO Aluno VALUES (?, ?, ?)",
                           (1, 'João', 'engajado'))

            # Inserir na tabela Aula
            cursor.execute("INSERT OR IGNORE INTO Aula VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (1, 1, '2025-04-06 10:00', 'Turma A', 'Introdução ao Álgebra', '', '', ''))

            # Inserir na tabela AlunoAula
            cursor.execute("INSERT OR IGNORE INTO AlunoAula VALUES (?, ?, ?, ?)",
                           (1, 1, 1, 'ativo'))

            # Inserir na tabela Desempenho
            cursor.execute("INSERT OR IGNORE INTO Desempenho VALUES (?, ?, ?, ?, ?, ?)",
                           (1, 1, 1, 95, 'prova final', 'erros por distração'))
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
