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