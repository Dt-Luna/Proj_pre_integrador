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
            # Tabela de usuários
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                idade INTEGER,
                email TEXT UNIQUE NOT NULL
            )
            """)

            # Tabela de livros
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livro (
                id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                paginas INTEGER,
                capa TEXT
            )
            """)

            # Tabela de exemplares
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

            # Tabela de solicitações de empréstimo
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

            # Tabela de empréstimos
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

            # Tabela de histórico de empréstimos
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_emprestimos (
                id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                id_emprestimo INTEGER,
                status_final TEXT,
                FOREIGN KEY(id_emprestimo) REFERENCES emprestimo(id_emprestimo)
            )
            """)

            # Tabela de avaliações de usuário
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

    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            logger.info("Conexão fechada")

    def __enter__(self):
        """Context manager - entrada"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída"""
        self.fechar()

