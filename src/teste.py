from database import Database
from models.solicitacaoemprestimo import SolicitacaoEmprestimo
from DAO.solicitacaoemprestimoDAO import SolicitacaoEmprestimoDAO
from datetime import date

# Inicializa o banco de dados
db = Database()

# Cria o DAO com a conexão
solicitacao_dao = SolicitacaoEmprestimoDAO(db.conn)

# Cria uma nova solicitação
solicitacao = SolicitacaoEmprestimo(
    id_solicitacao=None,
    id_exemplar=1,
    id_solicitante=1,
    data=str(date.today()),
    status="pendente"
)

# Insere a solicitação
id_inserido = solicitacao_dao.inserir(solicitacao)

if id_inserido:
    print(f"✓ Solicitação inserida com sucesso! ID: {id_inserido}")
    
    # Lista as solicitações
    solicitacoes = solicitacao_dao.listar()
    print(f"\n✓ Total de solicitações: {len(solicitacoes)}")
    for sol in solicitacoes:
        print(f"  - ID: {sol[0]}, Status: {sol[4]}")
else:
    print("✗ Erro ao inserir solicitação")

# Fecha a conexão
db.fechar()

