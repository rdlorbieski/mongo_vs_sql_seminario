# main.py
from sqlite_scripts import criar_tabelas_sqlite, inserir_dados_sqlite
from mongo_scripts import criar_collections_mongo, inserir_dados_mongo

if __name__ == "__main__":
    # Escolha entre SQLite ou MongoDB
    usar_sqlite = True

    if usar_sqlite:
        criar_tabelas_sqlite()
        inserir_dados_sqlite()
        print("Banco SQLite criado e populado com sucesso!")
    else:
        criar_collections_mongo()
        inserir_dados_mongo()
        print("Banco MongoDB criado e populado com sucesso!")