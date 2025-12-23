# Sistema de Empréstimo de Livros - BookShare

---

## 📁 Estrutura do Projeto

```
src/
├── database.py                  # Gerenciador de banco de dados
├── exceptions.py                # Exceções customizadas    
├── teste_completo.py            # Demonstração completa 
├── models/
│   ├── usuario.py              # Usuário com validação
│   ├── livro.py                # Livro com validação
│   ├── exemplar.py             # Exemplar com estados
│   ├── emprestimo.py           # Empréstimo com cálculos
│   ├── solicitacaoemprestimo.py # Solicitação com transições
│   ├── avaliacaousuario.py     # Avaliação com validação
│   ├── historicoemprestimos.py # Histórico de empréstimos
    └── dao.py


---

## 🛠️ Tecnologias Usadas

- **Python 3.8+** - Linguagem principal
- **SQLite3** - Banco de dados
- **logging** - Rastreamento de erros
- **ABC (Abstract Base Class)** - Herança abstrata
- **@property** - Encapsulamento

---