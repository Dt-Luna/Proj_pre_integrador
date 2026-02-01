 **DOCUMENTO DE VISÃO**

**1\. Nome do Produto**

BookShare

**2\. Problema a Ser Solucionado**

Atualmente, muitas pessoas possuem livros parados em casa, enquanto outras desejam ler exatamente esses mesmos títulos, mas não possuem acesso fácil por motivos como:

* Falta de dinheiro para comprar novos livros;  
* Dificuldade de encontrar edições específicas;  
* Distância de bibliotecas tradicionais;  
* Falta de um meio organizado para emprestar ou pedir livros para outras pessoas com segurança.

Além disso, quando empréstimos informais acontecem, não há controle de prazos, lembretes, registro de quem pegou o livro ou garantia de devolução, o que gera perda, atraso ou conflitos.

**3\. Oportunidades**

**3.1 Para os Usuários**

* Acesso mais fácil e gratuito a vários livros.  
* Economia por não precisar comprar todos os livros que deseja ler.  
* Possibilidade de compartilhar livros e conhecer novas obras.  
* Registro seguro dos empréstimos feitos e recebidos.

**3.2 Para a Comunidade**

* Incentivo à leitura e circulação de livros.  
* Redução de desperdício, já que livros parados passam a ser reutilizados.

	

**4\. Stakeholders e Necessidades**

**4.1 Usuários Leitores**

Necessidades:

* Cadastrar exemplares de livros próprios.  
* Oferecer os exemplares para empréstimo.  
* Solicitar exemplares de outros usuários.  
* Controlar seus empréstimos ativos e históricos.

**4.2 Donos dos Exemplares**

Necessidades:

* Registrar quais exemplares possui.  
* Aceitar ou rejeitar pedidos de empréstimo.  
* Definir prazo de devolução.  
* Ver lista de exemplares emprestados e situação de cada um.


**4.3 Administrador**

Necessidades:

* Cadastrar livros no sistema

 Ver mais funções no diagrama de CDU

**5\. Requisitos Funcionais**

| RF01  | Cadastrar usuário  | O sistema deve permitir que novos usuários se registrem informando nome, email e senha. |
| :---- | :---- | :---- |
| RF02 | Login e autenticação | Usuários devem acessar o sistema com email e senha. |
| RF03  | Cadastrar livros | O Administrador deve cadastrar os livros no sistema com: título, quantidade de páginas, autor e ano de publicação.  |
| RF04  | Cadastrar exemplares | O usuário deve cadastrar os exemplares de livros que possui e disponibilizá-los ou não para empréstimo  |
| RF05  | Listar exemplares de livros disponíveis | O sistema deve listar todos os exemplares cadastrados pelos usuários e informados como “disponíveis para empréstimo”. |
| RF06 | Solicitar empréstimo | O usuário deve poder enviar uma solicitação para pegar um exemplar emprestado. |
| RF07  | Aceitar ou recusar pedido | O dono do exemplar deve poder aprovar ou negar pedidos.  |
| RF08  | Registrar empréstimo | Quando o dono aprova, o sistema registra: Data de início Data de devolução prevista Usuário solicitante Livro emprestado  |
| RF09  | Registrar devolução | O usuário que pegou o livro deve marcar a devolução, e o dono confirma. |
| RF10  | Gerenciar disponibilidade | O dono pode definir se um livro está: Disponível Indisponível Emprestado |

**6\. Requisitos Não Funcionais**

| Código | Requisito Funcional | Descrição |
| :---- | :---- | :---- |
| RNF01  | Usabilidade | A interface deve ser simples, objetiva e acessível, construída com Streamlit, permitindo uso no celular sem dificuldade.  |
| RNF02  | Desempenho | O sistema deve responder a ações do usuário com rapidez  para consultas e atualizações.  |
| RNF03  | Persistência | Todos os dados devem ser armazenados em SQLite 3\.  |
| RNF04  | Segurança | Senhas de usuários não devem ser visíveis para outros usuários ou pelo administrador.  |
| RNF05  | Confiabilidade | O sistema não deve permitir conflitos, como dois usuários pegando o mesmo livro ao mesmo tempo. |
| RNF06  | Simplicidade tecnológica | O sistema deve utilizar apenas: Python Streamlit SQLite  |
| RNF07  | Controle de Acesso | Usuários só podem alterar livros próprios e dados de seus empréstimos.  |
| RNF08  | Manutenibilidade | Código organizado em camadas: database/ controllers/ views/ app.py  |

