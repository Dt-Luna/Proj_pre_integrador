**CDU018 – Avaliar Usuário**

*1\. Descrição*

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

