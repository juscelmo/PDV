import tkinter as tk
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Cria a conexão com o banco de dados
conn = sqlite3.connect('pdv.db')
cursor = conn.cursor()

# Cria a tabela de produtos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        preco REAL,
        estoque INTEGER,
        codigo_de_barras TEXT
    )
''')

# Cria a tabela de clientes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        endereco TEXT,
        telefone TEXT,
        email TEXT
    )
''')

# Cria a tabela de vendas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        valor_total REAL,
        metodo_de_pagamento TEXT,
        cliente_id INTEGER,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
''')

# Cria a tabela de itens de venda
cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_de_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER,
        produto_id INTEGER,
        quantidade INTEGER,
        FOREIGN KEY (venda_id) REFERENCES vendas(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
''')

# Insere alguns produtos de exemplo
cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco, estoque, codigo_de_barras)
    VALUES
        ("Produto 1", "Descrição do produto 1", 10.0, 100, "1234567890"),
        ("Produto 2", "Descrição do produto 2", 20.0, 50, "0987654321"),
        ("Produto 3", "Descrição do produto 3", 5.0, 200, "5555555555")
''')
conn.commit()

# Cria a janela principal
root = tk.Tk()
root.title('Sistema de Vendas')

# Cria as variáveis para os widgets
produto_codigo = tk.StringVar()
produto_nome = tk.StringVar()
produto_preco = tk.StringVar()
produto_quantidade = tk.IntVar()
total_venda = tk.StringVar()

# Cria os widgets
tk.Label(root, text='Código de barras ou nome do produto').grid(row=0, column=0)
tk.Entry(root, textvariable=produto_codigo).grid(row=0, column=1)
tk.Label(root, text='Nome do produto').grid(row=1, column=0)
tk.Entry(root, textvariable=produto_nome).grid(row=1, column=1)
tk.Label(root, text='Preço do produto').grid(row=2, column=0)
tk.Entry(root, textvariable=produto_preco).grid(row=2, column=1)
tk.Label(root, text='Quantidade').grid(row=3, column=0)
tk.Entry(root, textvariable=produto_quantidade).grid(row=3, column=1)
tk.Button(root, text='Adicionar', command=lambda: adicionar_item(produto_codigo.get())).grid(row=4, column=0, columnspan=2)
tk.Label(root, text='Total da venda').grid(row=5, column=0)
tk.Entry(root, textvariable=total_venda, state='readonly').grid(row=5, column=1)

# Função para adicionar um item à venda
def adicionar_item(codigo_ou_nome):
    cursor.execute('''
SELECT * FROM produtos WHERE codigo_de_barras = ? OR nome = ?
''', (codigo_ou_nome, codigo_ou_nome))
produto = cursor.fetchone()
if produto is None:
    tk.messagebox.showerror('Erro', 'Produto não encontrado')
else:
    quantidade = produto_quantidade.get()
    if quantidade > produto[4]:
        tk.messagebox.showerror('Erro', 'Estoque insuficiente')
    else:
        cursor.execute('''
            INSERT INTO itens_de_venda (venda_id, produto_id, quantidade)
            VALUES (?, ?, ?)
        ''', (venda_id, produto[0], quantidade))
        conn.commit()

        produto_quantidade.set(1)
        produto_codigo.set('')
        produto_nome.set('')
        produto_preco.set('')
        calcular_total_venda()
#Função para calcular o total da venda
def calcular_total_venda():
    total = 0
    cursor.execute('''
SELECT SUM(itens_de_venda.quantidade * produtos.preco)
FROM itens_de_venda
INNER JOIN produtos ON itens_de_venda.produto_id = produtos.id
WHERE itens_de_venda.venda_id = ?
''', (venda_id,))
    result = cursor.fetchone()
    if result is not None:
        total = result[0]
        total_venda.set(f'R$ {total:.2f}')
    else:
        tk.messagebox.showerror('Erro', 'Produto não encontrado')

#função para finalizar a venda
def finalizar_venda():
    global total_venda
    metodo_pagamento = var_pagamento.get()
    if metodo_pagamento == "":
        messagebox.showerror("Erro", "Selecione um método de pagamento!")
        return

    #calcula o total da venda
    calcular_total_venda()

    #insere a venda no banco de dados
    cursor.execute('''
        INSERT INTO vendas (data_venda, total_venda, metodo_pagamento)
        VALUES (?, ?, ?)
    ''', (date.today(), total, metodo_pagamento))

    #exibe mensagem de confirmação
    messagebox.showinfo("Venda", "Venda registrada com sucesso!")

    #limpa a tela
    limpar_tela()


#iniciar a janela principal
root.mainloop()

