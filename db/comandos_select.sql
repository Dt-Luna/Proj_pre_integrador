-- Lista todos os usuarios
SELECT * FROM Usuario;

-- Lista informações dos usuarios (nome, email e id) com idade maior que 18 anos
SELECT id, username, email FROM Usuario WHERE data_nascimento < '2008-01-01';

-- Lista o id do avaliador das avaliações com nota maior ou igual a 9 e que possuem comentário
SELECT id_avaliador FROM Avaliacao WHERE nota >= 9 AND comentario IS NOT NULL;

-- Lista quantos exemplares de cada livro existem na biblioteca
SELECT id_livro, COUNT(*) AS quantidade_exemplares FROM Exemplar GROUP BY id_livro;

-- Lista os títulos e autores dos livros escritos pelo mesmo autor do livro com ISBN '978-3-16-148410-0'
SELECT titulo, autor FROM livro where autor = (SELECT autor FROM livro WHERE isbn = '978-3-16-148410-0');

