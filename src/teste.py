from database import Database
from models.solicitacaoemprestimo import SolicitacaoEmprestimo
from DAO.solicitacaoemprestimoDAO import SolicitacaoEmprestimoDAO
from datetime import date

db = Database()

solicitacao_dao = SolicitacaoEmprestimoDAO(db.conn)

solicitacao = SolicitacaoEmprestimo(
    id_solicitacao=None,
    id_exemplar=1,
    id_solicitante=1,
    data=str(date.today()),
    status="pendente"
)

id_inserido = solicitacao_dao.inserir(solicitacao)

if id_inserido:
    print(f"✓ Solicitação inserida com sucesso! ID: {id_inserido}")
    
    solicitacoes = solicitacao_dao.listar()
    print(f"\n✓ Total de solicitações: {len(solicitacoes)}")
    for sol in solicitacoes:
        print(f"  - ID: {sol[0]}, Status: {sol[4]}")
else:
    print("✗ Erro ao inserir solicitação")

db.fechar()

