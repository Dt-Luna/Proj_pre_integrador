-- Só rodar para limpar todas as tabelas e reiniciar os IDs (para facilitar os testes)
-- Desabilitar constraints temporariamente para permitir deleção em ordem
ALTER TABLE Avaliacao DISABLE TRIGGER ALL;
ALTER TABLE Emprestimo DISABLE TRIGGER ALL;
ALTER TABLE Solic_emprestimo DISABLE TRIGGER ALL;
ALTER TABLE Exemplar DISABLE TRIGGER ALL;
ALTER TABLE Livro DISABLE TRIGGER ALL;
ALTER TABLE Usuario DISABLE TRIGGER ALL;

-- Deletar dados de todas as tabelas
TRUNCATE TABLE Avaliacao CASCADE;
TRUNCATE TABLE Emprestimo CASCADE;
TRUNCATE TABLE Solic_emprestimo CASCADE;
TRUNCATE TABLE Exemplar CASCADE;
TRUNCATE TABLE Livro CASCADE;
TRUNCATE TABLE Usuario CASCADE;

-- Reabilitar triggers
ALTER TABLE Usuario ENABLE TRIGGER ALL;
ALTER TABLE Livro ENABLE TRIGGER ALL;
ALTER TABLE Exemplar ENABLE TRIGGER ALL;
ALTER TABLE Solic_emprestimo ENABLE TRIGGER ALL;
ALTER TABLE Emprestimo ENABLE TRIGGER ALL;
ALTER TABLE Avaliacao ENABLE TRIGGER ALL;

-- Reiniciar as sequences dos IDs
ALTER SEQUENCE Usuario_id_seq RESTART WITH 1;
ALTER SEQUENCE Livro_id_seq RESTART WITH 1;
ALTER SEQUENCE Exemplar_id_seq RESTART WITH 1;
ALTER SEQUENCE Solic_emprestimo_id_seq RESTART WITH 1;
ALTER SEQUENCE Emprestimo_id_seq RESTART WITH 1;

-- Confirmação
SELECT 'Tabelas limpas e IDs reiniciados com sucesso!' as status;
