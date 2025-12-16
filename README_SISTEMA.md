# 📚 BookShare - Sistema de Compartilhamento de Livros

Um sistema de gerenciamento de empréstimos de livros com padrão DAO (Data Access Object) implementado em Python.

## 🎯 Funcionalidades

- ✅ Gerenciamento de Usuários
- ✅ Catálogo de Livros
- ✅ Controle de Exemplares
- ✅ Sistema de Solicitações de Empréstimo
- ✅ Registro de Empréstimos e Devoluções
- ✅ Histórico de Empréstimos
- ✅ Avaliação de Usuários

## 📁 Estrutura do Projeto

```
src/
├── database.py              # Gerenciador de conexão com BD
├── teste.py                 # Teste básico
├── exemplo_completo.py      # Exemplo com todas as funcionalidades
├── models/                  # Modelos de dados
│   ├── usuario.py
│   ├── livro.py
│   ├── exemplar.py
│   ├── emprestimo.py
│   ├── solicitacaoemprestimo.py
│   ├── historicoemprestimos.py
│   └── avaliacaousuario.py
└── DAO/                     # Data Access Objects
    ├── dao.py              # Classe base abstrata
    ├── usuarioDAO.py
    ├── livroDAO.py
    ├── exemplarDAO.py
    ├── emprestimoDAO.py
    ├── solicitacaoemprestimoDAO.py
    ├── historicoemprestimosDAO.py
    └── avaliacaousuarioDAO.py
```

## 🚀 Como Usar

### Instalação

```bash
# Não há dependências externas, apenas Python 3.6+
git clone <repo>
cd Proj_pre_integrador
```

### Exemplo Básico

```python
from database import Database
from models.usuario import Usuario
from DAO.usuarioDAO import UsuarioDAO

# Inicializar banco de dados
db = Database()

# Criar DAO
usuario_dao = UsuarioDAO(db.conn)

# Criar novo usuário
novo_usuario = Usuario(None, "João Silva", "joao@email.com", "senha123", 28)
id_usuario = usuario_dao.inserir(novo_usuario)

# Listar usuários
usuarios = usuario_dao.listar()

# Fechar conexão
db.fechar()
```

### Executar Exemplo Completo

```bash
cd src
python exemplo_completo.py
```

## 📊 Modelo de Dados

### Usuário
- `id_usuario`: ID único
- `username`: Nome de usuário único
- `email`: Email único
- `senha`: Senha criptografada
- `idade`: Idade do usuário

### Livro
- `id_livro`: ID único
- `titulo`: Título do livro
- `autor`: Autor
- `paginas`: Número de páginas
- `capa`: URL da capa (opcional)

### Exemplar
- `id_exemplar`: ID único
- `id_usuario`: Proprietário
- `id_livro`: Referência do livro
- `status`: disponível, emprestado, etc.

### Empréstimo
- `id_emprestimo`: ID único
- `id_exemplar`: Exemplar emprestado
- `id_dono`: Proprietário do livro
- `id_emprestado`: Quem pegou emprestado
- `data_inicio`: Data do empréstimo
- `data_prevista`: Data prevista de devolução
- `data_devolucao`: Data efetiva de devolução

### Solicitação de Empréstimo
- `id_solicitacao`: ID único
- `id_exemplar`: Exemplar solicitado
- `id_solicitante`: Quem solicitou
- `data_solicitacao`: Data da solicitação
- `status`: pendente, aprovada, recusada, etc.

### Avaliação de Usuário
- `id_avaliacao`: ID único
- `id_avaliador`: Quem avaliou
- `id_avaliado`: Quem foi avaliado
- `nota`: Nota (1-5)
- `comentario`: Comentário opcional
- `data_avaliacao`: Data da avaliação

## 🔧 Padrão DAO

Todos os DAOs herdam de `BaseDAO` e implementam a interface CRUD:

```python
class BaseDAO(ABC):
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
    
    @abstractmethod
    def inserir(self, obj):
        """Insere um novo objeto"""
        pass
    
    @abstractmethod
    def listar(self):
        """Lista todos os objetos"""
        pass
    
    @abstractmethod
    def listar_por_id(self, id):
        """Busca objeto por ID"""
        pass
    
    @abstractmethod
    def atualizar(self, obj):
        """Atualiza um objeto"""
        pass
    
    @abstractmethod
    def excluir(self, id):
        """Exclui um objeto"""
        pass
```

## 💾 Banco de Dados

O sistema usa **SQLite** por padrão. O arquivo `bookshare.db` é criado automaticamente na primeira execução.

### Criar conexão manual:
```python
from database import Database

db = Database("meu_banco.db")
# ... operações
db.fechar()
```

## 🛡️ Tratamento de Erros

Todos os DAOs possuem tratamento de exceções integrado:

```python
try:
    usuario_dao.inserir(novo_usuario)
except Exception as e:
    print(f"Erro ao inserir: {e}")
```

## 📝 Logging

O sistema inclui logging automático via módulo `logging`:

```
INFO:database:Conexão estabelecida com bookshare.db
INFO:database:Tabelas criadas com sucesso
INFO:database:Conexão fechada
```

## 🔍 Métodos Especiais dos DAOs

### UsuarioDAO
- `listar_por_email(email)`: Busca por email
- `listar_por_username(username)`: Busca por username

### LivroDAO
- `listar_por_autor(autor)`: Lista livros de um autor
- `listar_por_titulo(titulo)`: Busca por título (parcial)

### ExemplarDAO
- `listar_por_usuario(id_usuario)`: Exemplares de um usuário
- `listar_por_livro(id_livro)`: Exemplares de um livro
- `listar_por_status(status)`: Exemplares com status específico

## 🚀 Próximas Melhorias

- [ ] Adicionar validação de entrada em todos os modelos
- [ ] Implementar sistema de hashing para senhas
- [ ] Adicionar testes unitários
- [ ] Criar API REST com Flask/FastAPI
- [ ] Migrar para ORM (SQLAlchemy)
- [ ] Adicionar suporte a migrations de banco de dados
- [ ] Implementar connection pool
- [ ] Adicionar autenticação JWT

## 📄 Licença

Este projeto é de código aberto.

## 👥 Contribuidores

Contribuições são bem-vindas!

---

**Última atualização:** Dezembro 2025
