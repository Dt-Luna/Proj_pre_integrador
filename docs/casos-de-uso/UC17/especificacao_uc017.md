* **CDU017 – Solicitar Devolução de Exemplar**

*1\. Descrição*

O usuário que pegou o livro emprestado informa ao sistema que está   devolvendo o exemplar.

*2\. Atores*

Usuário solicitante e Sistema

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