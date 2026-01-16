-- Atualiza o nome de todos os usuários para 'fulano'
UPDATE Usuario SET username = 'fulano'; 

-- Atualiza o título do livro com id 2
UPDATE Livro SET titulo = 'A Revolução dos Bichos' WHERE id = 2; 

-- Adiciona 10 páginas a todos os livros do autor J.R.R. Tolkien com mais de 100 páginas
UPDATE Livro SET paginas = paginas + 10 WHERE autor = 'J.R.R. Tolkien' AND paginas > 100; 

-- Atualiza o título e o autor de todos os livros cujo título contém a letra 'A'
UPDATE Livro SET titulo = 'Livro com a', autor = 'Autor com Livro com a' WHERE titulo LIKE '%A%';

-- Atualiza os isbns de todos os livros para acrescentar o prefixo 'ISBN-'
UPDATE Livro SET isbn = CONCAT('ISBN-', isbn);

-- Atualiza todoas as datas de devolução de todos os emprestimos para a data atual
UPDATE Emprestimo SET data_devolucao = CURRENT_DATE;

-- Deleta todos as avaliações
DELETE FROM Avaliacao;

-- Deleta todas as solicitações de empréstimo que não foram aprovadas
DELETE FROM Solic_emprestimo WHERE status_aprovacao = FALSE;

-- Deleta todas solicitações de empréstimo feitas por usuários com id maior que 3
-- Como há foreign key entre Solic_emprestimo e Usuario, isso também irá deletar os empréstimos e avaliações relacionadas
ALTER TABLE Solic_emprestimo DISABLE TRIGGER ALL;
ALTER TABLE Emprestimo DISABLE TRIGGER ALL;
ALTER TABLE Avaliacao DISABLE TRIGGER ALL;
DELETE FROM Solic_emprestimo WHERE id_solicitante > 3;
ALTER TABLE Avaliacao ENABLE TRIGGER ALL;
ALTER TABLE Emprestimo ENABLE TRIGGER ALL;
ALTER TABLE Solic_emprestimo ENABLE TRIGGER ALL;

-- Inserindo as avaliações novamente para testar os deletes abaixo
INSERT INTO Avaliacao (nota, comentario, id_avaliador, tipo_avaliador, id_emprestimo)
VALUES
(9, 'Ótimo estado de devolução', 1, 1, 1),
(8, 'Livro bem conservado', 2, 2, 1),
(10, 'Excelente leitura!', 3, 1, 3),
(1, '', 4, 1, 4),
(2, 'Devolvido fora do prazo', 5, 1, 5);

-- Deleta todos as avaliações com nota menor que 2 e sem comentário
DELETE FROM Avaliacao WHERE nota < 2 AND (comentario IS NULL OR comentario = '');

-- Deleta todas as avaliações com mais de 10 caracteres no comentário
DELETE FROM Avaliacao WHERE LENGTH(comentario) > 5;