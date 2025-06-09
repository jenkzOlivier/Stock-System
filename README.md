# 📦 Sistema Web com Flask – Controle de Usuários e Produtos

Aplicação web desenvolvida com Flask que oferece:

- 🔐 Autenticação segura com hash de senha (bcrypt)
- 👥 CRUD completo de usuários
- 📦 Gerenciamento de produtos com dados detalhados
- 📄 Geração automática de relatórios em PDF
- 🧩 Estrutura modular organizada em camadas

---

## 🚀 Iniciando o Projeto

Execute localmente com:

```bash
python app.py


Depois, acesse no navegador: http://127.0.0.1:5000


📁 Estrutura do Projeto
app.py
app_models/
    produto_model.py
data/
    database_usuario.py
    database_produto.py
services/
    password_hashing.py
    pdf_generator.py
templates/
    *.html
static/
    *.css, *.js


🌐 Rotas e Funcionalidades
🏠 Página Inicial – Login

    GET / – Exibe o formulário de login

    POST /login – Valida as credenciais e redireciona ao menu principal

👤 Gerenciamento de Usuários

    GET /cadastrar_usuario – Formulário de cadastro de novo usuário

    POST /cadastrar_usuario – Valida e cadastra usuário com senha hash

    GET /listagem_de_usuarios – Lista todos os usuários

    GET|POST /usuarios/<id>/editar – Edita nome, acesso e senha

    POST /usuarios/<id>/excluir – Remove o usuário do sistema

📦 Gerenciamento de Produtos

    GET /produtos – Lista todos os produtos cadastrados

    GET|POST /produtos/novo – Cadastra um novo produto

    GET|POST /produtos/<id>/editar – Edita os dados de um produto

    POST /produtos/<id>/excluir – Exclui um produto

📄 Geração de Relatório em PDF

    GET /relatorio_pdf – Gera e salva automaticamente o relatório em relatorio_produtos.pdf

    O PDF inclui logotipo (se existir), tabela de produtos, valor total, rodapé com numeração e campo de assinatura.

🔐 Autenticação

    Baseada em verificação de hash de senha (bcrypt)

    Controle de acesso por nível (campo acesso)

    Dados armazenados em SQLite (usuarios.db)

📌 Requisitos

    Python 3.10+

    Flask

    Bcrypt

    ReportLab

Instalação dos pacotes: pip install flask bcrypt reportlab

📦 database_produto.py – Acesso ao Banco de Produtos

Módulo responsável pelas operações com o banco produtos.db.
🔧 Principais Métodos:

    criar_tabela()

    cadastrar_produto(produto)

    listar_produtos()

    editar_produto(produto)

    deletar_produto(id)

    buscar_produto_por_id(id)

    Os dados retornam encapsulados na classe ProdutoModel.

👤 database_usuario.py – Gerenciamento de Usuários

Responsável pela persistência de usuários em usuarios.db.
🔧 Funções Principais:

    criar_tabela()

    adicionar_usuario()

    buscar_usuario(user_name)

    listar_usuarios()

    buscar_usuario_por_id(id)

    atualizar_usuario()

    atualizar_usuario_com_senha()

    excluir_usuario(id)

    Senhas armazenadas em formato hash para garantir a segurança.

📄 pdf_generator.py – Geração de Relatório

Gera relatório PDF com os produtos em estoque.
🧾 Conteúdo do Relatório:

    ID, Nome, Marca, Referência, Valor Unitário, Quantidade, Subtotal

    Cálculo do valor total em estoque

    Logotipo opcional (static/assets/snowflake.png)

    Rodapé com número de página

    Campo para assinatura