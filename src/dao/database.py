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
                username VARCHAR(50) UNIQUE NOT NULL,
                senha VARCHAR(50) NOT NULL,
                data_nascimento VARCHAR(10) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livro (
                id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(255) NOT NULL,
                autor VARCHAR(255) NOT NULL,
                paginas INTEGER NOT NULL,
                isbn VARCHAR(20) UNIQUE NOT NULL
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exemplar (
                id_exemplar INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                id_livro INTEGER,
                status VARCHAR(50) NOT NULL CHECK(status IN ('disponivel', 'emprestado', 'reservado')),
                FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
                FOREIGN KEY(id_livro) REFERENCES livro(id_livro)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitacao_emprestimo (
                id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
                data_solicitacao TEXT,
                status TEXT NOT NULL CHECK(status IN ('pendente', 'aceita', 'recusada', 'cancelada')),
                dias_emprestimo INTEGER,
                id_exemplar INTEGER,
                id_solicitante INTEGER,
                FOREIGN KEY(id_exemplar) REFERENCES exemplar(id_exemplar),
                FOREIGN KEY(id_solicitante) REFERENCES usuario(id_usuario)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimo (
                id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_solicitacao INTEGER,
                data_inicio TEXT,
                data_prevista TEXT,
                data_devolucao TEXT,
                FOREIGN KEY(id_solicitacao) REFERENCES solicitacao_emprestimo(id_solicitacao)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacao_usuario (
                id_avaliador INTEGER NOT NULL,
                tipo_avaliador INT NOT NULL,
                nota INTEGER CHECK(nota >= 1 AND nota <= 5) NOT NULL,
                comentario TEXT,
                id_emprestimo INTEGER NOT NULL,
                data_avaliacao TEXT NOT NULL,
                PRIMARY KEY (id_avaliador, id_emprestimo),
                FOREIGN KEY(id_avaliador) REFERENCES usuario(id_usuario),
                FOREIGN KEY(id_emprestimo) REFERENCES emprestimo(id_emprestimo)
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

    def _executar_query(self, query, params=None, fetch=False, fetch_one=False):
        """Executa uma query SQL com parâmetros opcionais"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch_one:
                return self.cursor.fetchone()
            elif fetch:
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Erro ao executar query: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()