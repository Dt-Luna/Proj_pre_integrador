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

