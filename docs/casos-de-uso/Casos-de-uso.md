**CASOS DE USO**

**7\. Casos de Uso**

**![][image1]**

* **CDU001 \- Login:**

	*1.Descrição:* 

Para entrar no sistema o usuário/administrador precisa logar com um email e uma senha definida ao criar a conta ou editá-la

*2.Atores:*  
Usuário/administrador e sistema

*3\. Pré-condições:*  
O usuário/administrador precisa ter uma conta criada

*4\. Pós-condições:*  
O usuário/administrador estará logado no sistema e o registro deve ser cadastrado

*5\. Fluxos:*

*5.1.Fluxo principal:*

1.0) \[Usuário / Administrador\] ativa login;  
2.0) \[Usuário / Administrador\] adiciona email e senha;  
3.0) \[Usuário / Administrador\] ativa verificação;  
4.0) \[Sistema\] valida email e senha;  
5.0) \[Sistema\] encerra tela de login.

*5.2 Fluxos de exceção:*

Exceção 1: Senha inválida

1.0) \[Usuário / Administrador\] ativa login;  
2.0) \[Usuário / Administrador\] adiciona email e senha;  
3.0) \[Usuário / Administrador\] ativa verificação;  
4.0) \[Sistema\] invalida senha;  
	

Exceção 2: Email inválido  
	  
           1.0) Usuário / Administrador ativa login;  
2.0) \[Usuário / Administrador\] adiciona email e senha;  
3.0) \[Usuário / Administrador\] ativa verificação;  
4.0) \[Sistema\] invalida email;

* **CDU002 \- Criar Conta:**  
    
  *1\. Descrição:*  
  O usuário cria uma conta que deve possuir: username, email e senha de login. A conta deve ser validada pelo sistema para impedir que haja usernames iguais, além do uso de um email já cadastrado.  
    
  *2\. Atores:*  
  Usuário e sistema  
    
  *3\. Pré-condições:*  
  O usuário ainda não estar logado (sem sessão ativa) e possuir email, username e senha válidos  
    
  *4\. Pós-condições:*  
  O usuário estará logado no sistema e o registro deve ser cadastrado  
    
  *5.Fluxos:*  
    
  *5.1 Fluxo Principal:*  
    
  1.0) \[Usuário\] ativa “criar conta”;  
  2.0) \[Usuário\] adiciona username, email e senha;  
  3.0) \[Usuário\] ativa verificação;  
  4.0) \[Sistema\] valida username, email e senha;  
  5.0) \[Sistema\] leva usuário a tela inicial.  
    
  *5.2 Fluxos de exceção:*   
    
  Exceção 1: Username inválido  
    
  1.0) \[Usuário\] ativa “criar conta”;  
  2.0) \[Usuário\] adiciona username, email e senha;  
  3.0) \[Usuário\] ativa verificação;  
  4.0) \[Sistema\] invalida username;  
    
  Exceção 2: Email inválido  
    
  1.0) \[Usuário\] ativa “criar conta”;  
  2.0) \[Usuário\] adiciona username, email e senha;  
  3.0) \[Usuário\] ativa verificação;  
  4.0) \[Sistema\] invalida email;  
    
* **CDU003 \- Adicionar exemplar:**


*1.Descrição:*  
 O usuário pode adicionar um novo exemplar de um livro cadastrado no sistema à sua biblioteca

*2.Atores:*  
 Usuário e sistema

*3.Pré-condições:*  
O usuário deve estar logado no sistema, deve estar na tela principal e deve estar dentro da página “Minha estante”

*4.Pós-condições:*  
O exemplar será adicionado à estante e ficará disponível para visualização de outros usuários/empréstimos  
	  
           *5.Fluxos*

*5.1 Fluxo principal:*

1.0) \[Usuário\] acessa a opção “Adicionar novo exemplar”  
	2.0) \[Sistema\] exibe campo para busca ou cadastro de novo exemplar           	3.0) \[Usuário\] seleciona o título   
           4.0) \[Sistema\] confirma a adição à estante  
   
          *5.2 Fluxos de exceção:*

         Exceção 1: Título não encontrado

        1.0) \[Usuário\] seleciona o livro após busca ou cadastro.  
        2.0) \[Sistema\] não encontra o livro no catálogo (buscar por nome/id).  
        3.0) \[Sistema\] exibe mensagem de erro: “Livro não encontrado no catálogo.”  
        4.0) \[Sistema\] oferece opção de cadastro manual ou nova busca.  
        5.0) \[Fim do caso\].

      Exceção 2: Falha no sistema (ex: rede/BD)

      1.0) \[Sistema\] falha ao salvar.  
      2.0) \[Sistema\] exibe mensagem: “Erro ao adicionar. Tente novamente mais      tarde.”  
      3.0) \[Sistema\] sugere tentar novamente ou entrar em contato com o suporte.

* **CDU004 – Editar Perfil**  
  *1.Descrição:*  
   O usuário pode alterar suas informações pessoais cadastradas, como username, email ou senha

*2.Atores:*  
 	Usuário e sistema

*3.Pré-condições:*  
 O usuário deve estar logado no sistema.

*4.Pós-condições:*  
 As informações do perfil são atualizadas no banco de dados.

*5.Fluxos*

### *5.1 Fluxo Principal:*

1.0) \[Usuário\] acessa a opção “Editar perfil”;  
 2.0) \[Sistema\] exibe os campos editáveis;  
 3.0) \[Usuário\] altera as informações desejadas;  
 4.0) \[Usuário\] ativa “Salvar alterações”;  
 5.0) \[Sistema\] valida as alterações;  
 6.0) \[Sistema\] salva as novas informações;  
 7.0) \[Sistema\] exibe confirmação.

### *5.2 Fluxos de Exceção:*

*Exceção 1 – Email já cadastrado*  
 4.0) \[Sistema\] identifica email duplicado;  
 5.0) \[Sistema\] exibe erro: “Email já está em uso”.

*Exceção 2 – Senha inválida*  
 4.0) \[Sistema\] rejeita senha por não atender requisitos;  
 5.0) \[Sistema\] exibe mensagem: “Senha inválida”.

---

* **CDU005 – Sair do Sistema**  
  *1.Descrição:*  
   O usuário encerra sua sessão no sistema.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   O usuário deve estar logado.  
  *4.Pós-condições:*  
   A sessão é encerrada.  
    
  *5.Fluxos*

  ### *5.1 Fluxo Principal:*

  1.0) \[Usuário\] ativa “Sair”;  
   2.0) \[Sistema\] encerra sessão;  
   3.0) \[Sistema\] redireciona para tela inicial.  
* **CDU006 – Visualizar Perfis**  
  *1.Descrição:*  
   O usuário pode visualizar perfis de outros usuários, como donos dos exemplares.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   O usuário deve estar logado.  
  *4.Pós-condições:*  
   Nenhuma alteração — apenas visualização.  
  *5.Fluxos*  
  *5.1 Fluxo Principal:*  
   1.0) \[Usuário\] acessa um perfil;  
   2.0) \[Sistema\] mostra informações públicas (nome, livros, avaliações);  
   3.0) \[Sistema\] exibe exemplares disponíveis do usuário.  
  *5.2 Fluxos de exceção*  
  Exceção 1: Perfil inexistente:  
   1.0) \[Sistema\] não encontra usuário;  
   2.0) \[Sistema\] exibe erro: “Perfil não encontrado”.

* # **CDU007 – Cadastrar Livro (Admin)**

  *1.Descrição:*  
  O Administrador cadastra novos livros no catálogo geral.

  *2.Atores:*  
   Administrador e sistema.  
  *3.Pré-condições:*  
   O administrador deve estar logado com permissões especiais.

  *4.Pós-condições:*  
   O livro passa a fazer parte do catálogo disponível para exemplares.  
  *5.Fluxos:*  
  5.1 Fluxo Principal:  
   1.0) \[Admin\] acessa “Cadastrar livro”;  
   2.0) \[Sistema\] exibe formulário (título, autor, ano);  
   3.0) \[Admin\] preenche dados;  
   4.0) \[Sistema\] salva registro;  
   5.0) \[Sistema\] confirma cadastro.

  5.2 Fluxos de Exceção – Livro duplicado:  
   4.0) \[Sistema\] encontra título já existente;  
   5.0) \[Sistema\] notifica: “Livro já existe no catálogo”.

* # **CDU008 – Manter Cadastro de Livros (Admin)**

  *1.Descrição*  
   O administrador pode editar ou remover livros do catálogo  
  *2.Atores:*  
   Administrador e sistema.  
  *3.Pré-condições:*  
   Administrador logado.  
  *4.Pós-condições:*  
   Catálogo atualizado.  
  *5\. Fluxos*  
  *5.1 Fluxo Principal:*  
   1.0) \[Admin\] acessa lista de livros;  
   2.0) \[Admin\] escolhe editar ou remover;  
   3.0) \[Sistema\] executa ação escolhida;  
   4.0) \[Sistema\] salva mudanças.

* # **CDU009 – Manter Cadastro de Usuários (Admin)**

    
  *1.Descrição:*  
   O administrador pode visualizar, editar ou bloquear contas.  
  *2.Atores:*  
   Administrador e sistema.  
  *3.Pré-condições:*  
   Administrador logado.  
  *4.Pós-condições:*  
   Dados de usuários atualizados.  
  *5.Fluxo Principal:*  
   1.0) \[Admin\] acessa “Usuários cadastrados”;  
   2.0) \[Admin\] seleciona um usuário;  
   3.0) \[Admin\] edita dados ou aplica ação;  
   4.0) \[Sistema\] registra atualização.

* # **CDU010 – CRUD Biblioteca**

  *1.Descrição:*  
   O usuário pode gerenciar sua biblioteca pessoal: editar, remover e alterar disponibilidade de seus exemplares.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   Usuário logado e com exemplares cadastrados.  
  *4.Pós-condições:*  
   Sua lista de exemplares é atualizada.  
  *5.Fluxo Principal:*  
   1.0) \[Usuário\] acessa “Minha biblioteca”;  
   2.0) \[Usuário\] escolhe exemplar;  
   3.0) \[Usuário\] edita informações ou disponibilidade;  
   4.0) \[Sistema\] salva atualização.

* # **CDU011 – Visualizar Exemplar**

  *1.Descrição:*  
   O usuário visualiza detalhes de um exemplar específico.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   Usuário logado.  
  *4.Pós-condições:*  
   Nenhuma — apenas visualização.i  
  *5.Fluxos:*  
  *5.1 Fluxo Principal:*  
   1.0) \[Usuário\] seleciona um exemplar;  
   2.0) \[Sistema\] mostra estado, dono, disponibilidade e histórico;  
   3.0) \[Sistema\] oferece ações como “Solicitar empréstimo”.

* **CDU012 – Pesquisar Livros**  
  *1.Descrição:*  
   Permite buscar livros no catálogo geral ou entre exemplares disponíveis.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   Usuário logado.  
  *4.Pós-condições:*  
   Nenhuma — apenas exibição de resultados.  
  *5.Fluxos:*  
  *5.1 Fluxo Principal:*  
   1.0) \[Usuário\] acessa campo de busca;  
   2.0) \[Usuário\] insere título/autor;  
   3.0) \[Sistema\] filtra catálogo;  
   4.0) \[Sistema\] exibe resultados.

           *5.2 Exceção – Nada encontrado:*  
               3.0) \[Sistema\] não encontra livros;  
               4.0) \[Sistema\] exibe: “Nenhum resultado encontrado”.

* **CDU013 – Reservar Exemplares**  
  *1.Descrição:*  
   O usuário solicita empréstimo de um exemplar disponível.  
  *2.Atores:*  
   Usuário solicitante, dono do livro e sistema.  
  *3.Pré-condições:*  
   Usuário logado e exemplar deve estar disponível.  
  *4.Pós-condições:*  
   A solicitação é registrada e encaminhada ao dono.  
  *5.Fluxos:*  
  *5.1 Fluxo Principal:*  
   1.0) \[Usuário\] acessa exemplar;  
   2.0) \[Usuário\] ativa “Solicitar empréstimo”;  
   3.0) \[Sistema\] envia notificação ao dono;  
   4.0) \[Sistema\] registra solicitação como “pendente”.

           *5.2 Exceção – Exemplar indisponível:*  
              2.0) \[Sistema\] identifica status ≠ disponível;  
              3.0) \[Sistema\] exibe: “Exemplar no momento indisponível”.

* # **CDU014 – Ver Solicitações**

  *1.Descrição:*  
   O usuário visualiza solicitações recebidas de empréstimo.  
  *2.Atores:*  
   Usuário e sistema.  
  *3.Pré-condições:*  
   Usuário ser dono de exemplares.  
  *4.Pós-condições:*  
   Nenhuma — apenas visualização.

	*5\. Fluxos*

*5.1 Fluxo Principal:*  
 1.0) \[Usuário\] acessa “Solicitações”;  
 2.0) \[Sistema\] lista solicitações pendentes e concluídas.

* **CDU015 – Avaliar Solicitações**  
  *1.Descrição:*  
   O dono do exemplar aceita ou recusa pedidos de empréstimo.

  *2.Atores:*  
   Usuário dono, solicitante e sistema.

  *3.Pré-condições:*  
   Haver uma solicitação pendente.

  *4.Pós-condições:*  
   Empréstimo aprovado é registrado;  
   Recusa encerra solicitação.  
  *5\. Fluxo*  
  *5.1 Fluxo Principal:*  
   1.0) \[Dono\] acessa solicitação;  
   2.0) \[Dono\] escolhe aprovar ou recusar;  
   3.0) \[Sistema\] registra decisão;  
   4.0) \[Sistema\] envia notificação ao solicitante.

  *5.2 Fluxos de exceção:*

Exceção 1: Falha no sistema:

	 3.0) \[Sistema\] falha ao registrar decisão;  
	 4.0) \[Sistema\] exibe: “Erro ao processar. Tente novamente.”

* **CDU016 – Realizar Empréstimo**

*1\. Descrição*

Este caso de uso formaliza o empréstimo de um exemplar após a aprovação da solicitação pelo dono, criando o registro oficial do empréstimo no sistema.

*2\. Atores*

Dono do exemplar

Usuário solicitante

Sistema

*3\. Pré-condições*

Usuário solicitante está logado

Existe uma solicitação de empréstimo aprovada

Exemplar está marcado como disponível

*4\. Pós-condições*

Empréstimo é registrado no sistema

Exemplar passa para o status emprestado

Datas de início e devolução prevista são salvas

*5\. Fluxos*

*5.1 Fluxo Principa*l

1.0) \[Sistema\] identifica solicitação aprovada

2.0) \[Sistema\] cria registro de empréstimo

3.0) \[Sistema\] define data de início

4.0) \[Sistema\] define data prevista de devolução

5.0) \[Sistema\] atualiza status do exemplar para “emprestado”

6.0) \[Sistema\] notifica dono e solicitante

*5.2 Fluxos de Exceção*

Exceção 1 – Exemplar já emprestado

2.0) \[Sistema\] detecta conflito

3.0) \[Sistema\] cancela operação

4.0) \[Sistema\] exibe mensagem: “Exemplar indisponível no momento”

* **CDU017 – Solicitar Devolução de Exemplar**

*1\. Descrição*

O usuário que pegou o livro emprestado informa ao sistema que está devolvendo o exemplar.

*2\. Atores*

Usuário solicitante

Sistema

*3\. Pré-condições*

Usuário está logado

Existe um empréstimo ativo associado ao usuário

*4\. Pós-condições*

Devolução fica registrada como pendente de confirmação

*5\. Fluxos*

*5.1 Fluxo Principal*

1.0) \[Usuário\] acessa lista de empréstimos ativos

2.0) \[Usuário\] seleciona “Marcar devolução”

3.0) \[Sistema\] registra devolução como pendente

4.0) \[Sistema\] notifica o dono do exemplar

* **CDU018 \- Avaliar Usuário**

           1.Descrição

O usuário avalia outro usuário ou empréstimo com base em um empréstimo realizado, atribuindo uma nota de 1 a 5 e opcionalmente adicionar um comentário sobre sua experiência.

*2\. Atores*

Usuário e Sistema

*3\. Pré-condições*

Usuário está logado 

Existe um empréstimo ativo associado ao usuário

O empréstimo deve estar finalizado

Ainda não deve existir uma avaliação do mesmo usuário para o mesmo empréstimo

*4\. Pós-condições*

A avaliação é registrada e fica visível para outros usuários.

*5\. Fluxos*

*5.1 Fluxo Principal*

1.0) \[Usuário\] seleciona "Avaliar" no menu

2.0)  \[Sistema\] exibe lista de empréstimos do usuário (já devolvidos)

3.0)  \[Usuário\] seleciona um empréstimo da lista

4.0)  \[Sistema\] exibe formulário de avaliação com campos:

   \- Campo de nota (seletor 1-5 ou botões)

   \- Campo de comentário (texto)

   \- Informações do empréstimo (livro, exemplar, data)

5.0) \[Usuário\] preenche a nota (obrigatório)

6.0) \[Usuário\] preenche comentário (opcional)

7.0)  \[Usuário\] clica no botão "Enviar Avaliação"

8.0) \[Sistema\] valida se os dados estão corretos

9.0) \[Sistema\] exibe mensagem de sucesso

*5.2 Fluxos de Exceção*

Exceção 1 \- Nota Inválida

1.0) \[Usuário\] digita valor inválido (ex: 0, 6, \-1, texto)

2.0) \[Usuário\] clica em “Enviar Avaliação”

3.0 \[Sistema\] valida se os dados estão corretos

4.0 \[Sistema\] exibe mensagem de erro “Nota deve estar entre 1 e 5”

Exceção 2 \- Comentário muito longo

1.0) \[Usuário\] escreve comentário muito longo (\>500chars)

2.0) \[Usuário\] clica em “Enviar Avaliação”

3.0) \[Sistema\] valida se os dados estão corretos

4.0) \[Sistema\] exibe mensagem de erro: "Comentário não pode exceder 500 caracteres"

Exceção 3 \- Avaliação Duplicada

1.0) \[ Usuário\] já avaliou este empréstimo

2.0) \[Usuário\] tenta enviar uma nova avaliação para o mesmo empréstimo

3.0) \[Sistema} exibe “Você já avaliou este empréstimo” 

* **CDU019 – Confirmar Devolução de Exemplar**  
  *1\. Descrição*  
  O dono do exemplar confirma que o livro foi devolvido corretamente.  
    
  *2\. Atores*  
    
  Dono do exemplar  
    
  Sistema  
    
  *3\. Pré-condições*  
    
  Existe uma devolução pendente  
    
  Dono está logado  
    
  *4\. Pós-condições*  
    
  Empréstimo é encerrado  
    
  Exemplar volta ao status disponível  
    
  Histórico do empréstimo é atualizado  
    
  *5\. Fluxos*  
  *5.1 Fluxo Principal*  
    
  1.0) \[Dono\] acessa devoluções pendentes  
  2.0) \[Dono\] confirma devolução  
  3.0) \[Sistema\] encerra empréstimo  
  4.0) \[Sistema\] atualiza status do exemplar  
  5.0) \[Sistema\] notifica usuário solicitante     
                                                                                                                                                                                              5.2 Fluxos de Exceção     
                                                                                                                                  Exceção 1 – Devolução já confirmada  
  2.0) \[Sistema\] detecta devolução concluída  
  3.0) \[Sistema\] exibe: “Este empréstimo já foi encerrado”  
  

[image1]: <data:image/png;base64,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WlSoIguCIBQGjz76qG731qyZqdyXeCKyceM8VaPGnhG9YNWqVQ0rRcuWPRhWkhYuHKfTypcvq///8MNyddddVxaraLHtkiXj9bak/f47cQPFnssWyq5IERWE3OL5FMqDKghCofDVV1/pMDDYOrkv70SF8DKXXnp6RFq/ft3DihAKGIpY1aq7q99+W6XTOnU6KqwYFCkIsRUte1uOsWHD3KhtRVbrMiRPKFNByCWeWpQoWoIgFArly5fXbd63376g3Be3SLCEMkQRpUwFIZd4alGiaAmCUCjYvUkiwZf//Cc0a1QQconnEygPqSAIhQLtXalSuyr3hS0STPn111fkHSbkHM8nUB5SQRAKBVG08ktE0RL8gOcTKA+pIAiFggwd5pe8/XZoBqkg5BLPJ1AeUkEQCoUKFSroNu+bb5Yp96WdSTHKnZeiZ69/4YWJUetFioQyrFy5oi5TQcglnlqUKFqCIBQK27ZtU3vuuaf25O6+uDMpxSlX8SSVfQpJKEPyiDIVhFziqUWJoiUIQiExb9483e699NJk5b68E5U+fbqoWrWqqXr1aqprrz0vnL5u3RztAb5ixXLqgw+eDKfH6tF65plx6tBDD9DbHnPM4RHrbSEd31z16++rdtuttOrevb36+OOn4x6juOt4+ul71EEH1dNhgEzatm3L9P3gyZ77ITajWedXoezIm1AoI0HILZ5alChagiAUGn379tVt36677qLcl3giwr4rV05VkyYNjeh5YhklCGG5d+/O4XTzay+fe+5J6rHHRsZdb467//611MMP36KVINJRoOIdA6XJvQ77+mbNul3NmTNKnXJKW53GsUjHsJz72WefvcLb+1EoM66XMhQEP+CpRYUqoSAIQuHw119/hZWac845UX333YvKfaEXJ+xXu3Z1NXv2Her775dHpNvLeIi30805zfKWLc9EHddeb6+zA03bQandY6AoudfhHh+pXn0PndaiRWP9/+KLu+n7sY/lJ6GMKCtz/ZShIPgBTy0qVAkFQRAKj1dffTX84u7YsYVyX+7FyYoVU1X79kdEKTL2MsOLdro5l1nevPmpiGO66016w4Z1Vf/+p6kFC8ZGbeMeo2bNalHXYS9/9dVzEdsbGTKkt76fOnVqRK3LtVA25r4pM0HwE55aVKgSCoIgFC7vvPNO+EXO0BQ2Tu7L3hazra30ILvvHgrx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>