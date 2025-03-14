from banco import EstoqueDB
from produto import Produto

# Inicializa o banco
banco = EstoqueDB()

# Cadastra um produto
produto1 = Produto(banco, "Teclado Mecânico", 10, 250.99)
produto1.salvar()

# Lista os produtos
produtos = Produto.listar_todos(banco)
for p in produtos:
    print(f"Nome: {p.nome}, Quantidade: {p.quantidade}, Preço: R${p.preco:.2f}")

# Fecha a conexão com o banco
banco.fechar_conexao()
