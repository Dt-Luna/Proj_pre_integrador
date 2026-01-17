-- Comandos para junções de tabelas no banco de dados

-- Lista todos os exemplares de todos os usuários junto com as informações do usuário
SELECT Usuario.id, Usuario.username, Exemplar.id AS id_exemplar
FROM Usuario
LEFT JOIN Exemplar ON Usuario.id = Exemplar.id_usuario;

-- Lista todos os usuários junto com suas avaliações
SELECT Usuario.id, Usuario.username, Avaliacao.nota, Avaliacao.comentario
FROM Usuario
LEFT JOIN Avaliacao ON Usuario.id = Avaliacao.id_avaliador; 

-- Lista todos os livros junto com seus exemplares
SELECT Livro.titulo, Exemplar.id AS id_exemplar
FROM Livro
LEFT JOIN Exemplar ON Livro.id = Exemplar.id_livro;

-- Lista todos os empréstimos e suas avaliações
SELECT Emprestimo.id, Emprestimo.data_emprestimo, Avaliacao.nota, Avaliacao.comentario
FROM Emprestimo
FULL JOIN Avaliacao ON Emprestimo.id =  Avaliacao.id_emprestimo
