CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL, -- armazena hash da senha
    data_nascimento DATE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Livro(
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    paginas INT NOT NULL,
    capa VARCHAR(80),
    isbn VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE Exemplar(
    id SERIAL PRIMARY KEY,
    status_emprestimo VARCHAR(30) NOT NULL CHECK (
        status_emprestimo IN ('disponivel', 'emprestado')
    ),
    limite_dias INT NOT NULL,
    id_livro INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_livro) REFERENCES livro(id),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

CREATE TABLE Solic_emprestimo(
    id SERIAL PRIMARY KEY,
    status_aprovacao BOOLEAN NOT NULL, 
    data DATE NOT NULL,
    dias_emprestimo INT NOT NULL,
    id_exemplar INT NOT NULL,
    id_solicitante INT NOT NULL,
    FOREIGN KEY (id_exemplar) REFERENCES exemplar(id),
    FOREIGN KEY (id_solicitante) REFERENCES usuario(id)
);

CREATE TABLE Emprestimo(
    id SERIAL PRIMARY KEY, 
    data_emprestimo DATE NOT NULL,
    data_prevista DATE NOT NULL,
    data_devolucao DATE NOT NULL,
    id_solicitacao INT NOT NULL,
    FOREIGN KEY (id_solicitacao) REFERENCES solic_emprestimo(id)
);

CREATE TABLE Avaliacao(
    nota INT NOT NULL CHECK (nota >= 1 AND nota <= 10),
    comentario TEXT,
    id_avaliador INT NOT NULL,
    tipo_avaliador INT NOT NULL, 
    id_emprestimo INT NOT NULL,
    PRIMARY KEY (id_avaliador, id_emprestimo),
    FOREIGN KEY (id_emprestimo) REFERENCES Emprestimo(id)
)