from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image
from reportlab.lib.units import cm


from datetime import datetime
import locale
import sys
import os

# Caminho base: sobe um nível (da pasta services para o diretório do projeto)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona os caminhos necessários
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'app_models'))

# Agora os imports funcionam
from database_produto import ProdutoDatabase
from produto_model import ProdutoModel

# Locale para R$
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

# Rodapé com número da página
def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.drawString(2 * cm, 1 * cm, f"Página {doc.page}")
    canvas.restoreState()

def gerar_relatorio_pdf(nome_arquivo="relatorio_produtos.pdf"):
    produtos = ProdutoDatabase.listar_produtos()
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=30,
        bottomMargin=30
    )
    
    elementos = []
    estilos = getSampleStyleSheet()
    estilo_normal = estilos["Normal"]

    # Logotipo da empresa
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'static','assets', 'snowflake.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=4*cm, height=4*cm)
        elementos.append(img)

    # Cabeçalho
    elementos.append(Paragraph("<b>Estoque</b>", estilos["Title"]))
    elementos.append(Paragraph(f"Relatório de Produtos em Estoque — {datetime.now().strftime('%d/%m/%Y')}", estilo_normal))
    elementos.append(Spacer(1, 20))


    # Cabeçalhos da tabela
    dados = [["ID", "Nome", "Marca", "Referência", "Valor (R$)", "Qtd", "Subtotal (R$)"]]
    total = 0

    for p in produtos:
        subtotal = p.valor * p.quantidade
        total += subtotal
        dados.append([
            str(p.id),
            p.nome,
            p.marca,
            p.referencia,
            f"{p.valor:.2f}",
            str(p.quantidade),
            f"{subtotal:.2f}"
        ])

    # Colunas mais proporcionais
    largura_colunas = [30, 100, 80, 80, 70, 50, 80]

    tabela = Table(dados, repeatRows=1, colWidths=largura_colunas)
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A237E')),  # Azul escuro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ])
    tabela.setStyle(estilo_tabela)

    elementos.append(tabela)
    elementos.append(Spacer(1, 20))

    total_formatado = locale.currency(total, grouping=True)
    elementos.append(Paragraph(f"<b>Total em estoque (R$): {total_formatado}</b>", estilo_normal))
    elementos.append(Spacer(1, 40))

    # Assinatura
    assinatura = Paragraph("<i>_________________________<br/>Responsável pelo estoque</i>", estilo_normal)
    elementos.append(assinatura)

    # Construir PDF com rodapé
    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)
    print(f"PDF '{nome_arquivo}' gerado com sucesso.")