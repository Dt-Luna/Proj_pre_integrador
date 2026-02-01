* **CDU016 – Realizar Empréstimo**

*1\. Descrição*

Este caso de uso formaliza o empréstimo de um exemplar após a aprovação da solicitação pelo dono, criando o registro oficial do empréstimo no sistema.

*2\. Atores*

Dono do exemplar, Usuário solicitante e Sistema

*3\. Pré-condições*

Usuário solicitante está logado

Existe uma solicitação de empréstimo aprovada

Exemplar está marcado como disponível

*4\. Pós-condições*

Empréstimo é registrado no sistema

Exemplar passa para o status emprestado

Datas de início e devolução prevista são salvas

*5\. Fluxos*

*5.1 Fluxo Principal*

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

