import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:

    def __init__(self, nome_db="bookshare.db"):
        try:
            self.conn = sqlite3.connect(nome_db)
            self.cursor = self.conn.cursor()
            logger.info(f"Conexão estabelecida com {nome_db}")
            self.criar_tabelas()
        except sqlite3.Error as e:
            logger.error(f"Erro ao conectar no banco: {e}")
            raise

    def criar_tabelas(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                idade INTEGER,
                email TEXT UNIQUE NOT NULL
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livro (
                id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                paginas INTEGER,
                capa TEXT
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exemplar (
                id_exemplar INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                id_livro INTEGER,
                status TEXT,
                FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
                FOREIGN KEY(id_livro) REFERENCES livro(id_livro)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitacao_emprestimo (
                id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_exemplar INTEGER,
                id_solicitante INTEGER,
                data_solicitacao TEXT,
                status TEXT,
                FOREIGN KEY(id_exemplar) REFERENCES exemplar(id_exemplar),
                FOREIGN KEY(id_solicitante) REFERENCES usuario(id_usuario)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimo (
                id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_exemplar INTEGER,
                id_dono INTEGER,
                id_emprestado INTEGER,
                data_inicio TEXT,
                data_prevista TEXT,
                data_devolucao TEXT,
                FOREIGN KEY(id_exemplar) REFERENCES exemplar(id_exemplar),
                FOREIGN KEY(id_dono) REFERENCES usuario(id_usuario),
                FOREIGN KEY(id_emprestado) REFERENCES usuario(id_usuario)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_emprestimos (
                id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                id_emprestimo INTEGER,
                status_final TEXT,
                FOREIGN KEY(id_emprestimo) REFERENCES emprestimo(id_emprestimo)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacao_usuario (
                id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_avaliador INTEGER,
                id_avaliado INTEGER,
                nota INTEGER,
                comentario TEXT,
                data_avaliacao TEXT,
                FOREIGN KEY(id_avaliador) REFERENCES usuario(id_usuario),
                FOREIGN KEY(id_avaliado) REFERENCES usuario(id_usuario)
            )
            """)

            self.conn.commit()
            logger.info("Tabelas criadas com sucesso")
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            raise

    def limpar_dados(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = OFF")
            
            tabelas = [
                "historico_emprestimos",
                "avaliacao_usuario",
                "emprestimo",
                "solicitacao_emprestimo",
                "exemplar",
                "livro",
                "usuario"
            ]
            
            for tabela in tabelas:
                self.cursor.execute(f"DELETE FROM {tabela}")
            
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
            logger.info("Dados das tabelas limpos com sucesso")
        except sqlite3.Error as e:
            logger.error(f"Erro ao limpar dados: {e}")
            raise

    def fechar(self):
        if self.conn:
            self.conn.close()
            logger.info("Conexão fechada")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()

