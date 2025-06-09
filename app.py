from flask import Flask, render_template, request, redirect, send_file, url_for
import sys
import os

# Caminho absoluto da pasta onde está o app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adiciona manualmente os diretórios ao sys.path
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

# Agora os imports personalizados funcionam
import database_usuario
from database_produto import ProdutoDatabase
from produto_model import ProdutoModel
from services import password_hashing
from pdf_generator import gerar_relatorio_pdf


# Agora os módulos podem ser importados diretamente
app = Flask(__name__)
database_usuario.criar_tabela()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']

    dados = database_usuario.buscar_usuario(usuario)

    if dados and password_hashing.check_hashed_password(senha, dados[1]):
        return redirect(url_for('menu', usuario=usuario))
    else:
        message = "Usuário ou senha incorretos"
        return render_template('login.html', message=message)

@app.route('/menu/<usuario>')
def menu(usuario):
    dados = database_usuario.buscar_usuario(usuario)
    if dados:
        return render_template('menu.html', usuario=usuario, acesso=dados[2])
    else:
        return redirect(url_for('home'))

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        funcionario = request.form['funcionario']
        senha = request.form['senha']
        confirm_senha = request.form['confirm_senha']
        acesso = request.form['acesso']

        if senha != confirm_senha:
            errors = "As senhas não coincidem"
            return render_template('cadastro_usuario.html', mode=False, errors=errors)

        if database_usuario.buscar_usuario(funcionario):
            errors = "Usuário já existe"
            return render_template('cadastro_usuario.html', mode=False, errors=errors)

        senha_hash = password_hashing.hash_password(senha)
        database_usuario.adicionar_usuario(funcionario, senha_hash, acesso)
        return redirect(url_for('home'))

    return render_template('cadastro_usuario.html', mode=False)







##### WEB USUARIO CRUD
@app.route('/listagem_de_usuarios')
def usuarios():
    usuarios_lista = database_usuario.listar_usuarios()
    return render_template('listagem_de_usuario.html', usuarios=usuarios_lista)

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        novo_nome = request.form['user_name']
        novo_acesso = request.form['acesso']
        nova_senha = request.form['nova_senha']

        if nova_senha:
            senha_hash = password_hashing.hash_password(nova_senha)  # Corrigido aqui
            database_usuario.atualizar_usuario_com_senha(id, novo_nome, senha_hash, novo_acesso)
        else:
            database_usuario.atualizar_usuario(id, novo_nome, novo_acesso)

        return redirect(url_for('usuarios'))

    usuario = database_usuario.buscar_usuario_por_id(id)
    if usuario:
        return render_template('editar_usuario_crud.html', usuario=usuario)
    return 'Usuário não encontrado', 404


@app.route('/usuarios/<int:id>/excluir', methods=['POST'])
def excluir_usuario(id):
    database_usuario.excluir_usuario(id)
    return redirect(url_for('usuarios'))




#### CRUD WEB DE PRODUTOS####
# Listagem de produtos
@app.route('/produtos')
def listar_produtos():
    produtos = ProdutoDatabase.listar_produtos()
    return render_template('listagem_de_produtos.html', produtos=produtos)

# Cadastro de novo produto
@app.route('/produtos/novo', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        produto = ProdutoModel(
            nome=request.form['nome'],
            marca=request.form['marca'],
            descricao=request.form['descricao'],
            referencia=request.form['referencia'],
            valor=float(request.form['valor']),
            quantidade=int(request.form['quantidade'])
        )
        ProdutoDatabase.cadastrar_produto(produto)
        return redirect(url_for('listar_produtos'))
    return render_template('cadastrar_produto.html')


# Editar produto
@app.route('/produtos/<int:id>/editar', methods=['GET', 'POST'])
def editar_produto(id):
    produto = ProdutoDatabase.buscar_produto_por_id(id)

    if not produto:
        return "Produto não encontrado", 404

    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.marca = request.form['marca']
        produto.descricao = request.form['descricao']
        produto.referencia = request.form['referencia']
        produto.valor = float(request.form['valor'])
        produto.quantidade = int(request.form['quantidade'])
        ProdutoDatabase.editar_produto(produto)
        return redirect(url_for('listar_produtos'))

    return render_template('editar_produto.html', produto=produto)


# Excluir produto
@app.route('/produtos/<int:id>/excluir', methods=['POST'])
def excluir_produto(id):
    ProdutoDatabase.deletar_produto(id)
    return redirect(url_for('listar_produtos'))

#sent product
@app.route('/relatorio_pdf')
def relatorio_pdf():
    nome_arquivo = "relatorio_produtos.pdf"
    gerar_relatorio_pdf(nome_arquivo)
    caminho_pdf = os.path.join(os.getcwd(), nome_arquivo)
    return send_file(caminho_pdf, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
