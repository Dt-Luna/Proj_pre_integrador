-- Usuarios
INSERT INTO Usuario (username, senha, data_nascimento, email)
VALUES 
('alice', 'hash123', '2002-05-10', 'alice@email.com'),
('bruno', 'hash456', '2009-08-15', 'b.oliveira@email.com'),
('caio', 'hash333', '1999-10-31', 'caio@email.com'),
('diana', 'hash999', '2007-04-30', 'diana@email.com'),
('eduardo', 'hash000', '2003-02-17', 'eduardo@email.com');

-- Livros
INSERT INTO Livro (titulo, autor, paginas, capa, isbn)
VALUES
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 96, 'capa1.jpg', '978-3-16-148410-0'),
('1984', 'George Orwell', 328, 'capa2.jpg', '978-0-452-28423-4'),
('Dom Quixote', 'Miguel de Cervantes', 863, 'capa3.jpg', '978-0-14-243723-0'),
('O Senhor dos Anéis', 'J.R.R. Tolkien', 1216, 'capa4.jpg', '978-0-618-00222-8'),
('Alice no País das Maravilhas', 'Lewis Carroll', 200, 'capa5.jpg', '978-0-14-132107-4');

-- Exemplares
INSERT INTO Exemplar (status_emprestimo, limite_dias, id_livro, id_usuario)
VALUES
('disponivel', 14, 1, 1),
('disponivel', 7, 2, 2),
('disponivel', 21, 3, 3),
('disponivel', 14, 4, 4),
('disponivel', 10, 5, 5);

-- Solicitações de Empréstimo
INSERT INTO Solic_emprestimo (status_aprovacao, data, dias_emprestimo, id_exemplar, id_solicitante)
VALUES
(TRUE, '2024-01-10', 14, 1, 2),
(TRUE, '2024-01-12', 7, 2, 3),
(TRUE, '2024-01-15', 21, 3, 4),
(TRUE, '2024-01-18', 14, 4, 5),
(TRUE, '2024-01-20', 10, 5, 1);  

-- Empréstimos
INSERT INTO Emprestimo (data_emprestimo, data_prevista, data_devolucao, id_solicitacao)
VALUES
('2024-01-11', '2024-01-25', '2024-01-24', 1),
('2024-01-13', '2024-01-20', '2024-01-19', 2),
('2024-01-16', '2024-02-06', '2024-02-05', 3),
('2024-01-19', '2024-02-02', '2024-02-01', 4),
('2024-01-21', '2024-01-31', '2024-01-30', 5);
-- importante ressaltar que todo empréstimo nasce de uma solicitação aprovada
-- por enquanto não há validação para impedir que um emprestimo seja criado sem aprovação
-- futuramente adicionar trigger (a camada de lógica já garante isso)

-- Avaliações
INSERT INTO Avaliacao (nota, comentario, id_avaliador, tipo_avaliador, id_emprestimo)
VALUES
(9, 'Ótimo estado de devolução', 1, 1, 1),
(8, 'Livro bem conservado', 2, 2, 1),
(10, 'Excelente leitura!', 3, 1, 3),
(1, '', 4, 1, 4),
(2, 'Devolvido fora do prazo', 5, 1, 5);


