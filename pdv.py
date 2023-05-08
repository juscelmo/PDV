import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
# Cria ou conecta ao banco de dados
conn = sqlite3.connect('pdv.db')

# Cria tabela de produtos
conn.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    codigo_barras TEXT UNIQUE
);
''')

def adicionar_produto(produto):
    try:
        conn.execute('''
        INSERT INTO produtos (nome, descricao, preco, quantidade, codigo_barras)
        VALUES (?, ?, ?, ?, ?)
        ''', (produto['nome'], produto['descricao'], produto['preco'], produto['quantidade'], produto['codigo_barras']))
        conn.commit()
        messagebox.showinfo(title='Produto cadastrado', message='O produto foi cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        messagebox.showerror(title='Erro', message=f"O código de barras '{produto['codigo_barras']}' já está em uso.")
        

        
# Cria a janela principal
root = tk.Tk()
root.title('Cadastro de Produtos')

# Cria os widgets
tk.Label(root, text='Nome:').grid(row=0, column=0)
tk.Entry(root, width=50, name='nome_entry').grid(row=0, column=1)

tk.Label(root, text='Descrição:').grid(row=1, column=0)
tk.Entry(root, width=50, name='descricao_entry').grid(row=1, column=1)

tk.Label(root, text='Preço:').grid(row=2, column=0)
tk.Entry(root, width=20, name='preco_entry').grid(row=2, column=1)

tk.Label(root, text='Quantidade:').grid(row=3, column=0)
tk.Entry(root, width=20, name='quantidade_entry').grid(row=3, column=1)

tk.Label(root, text='Código de barras:').grid(row=4, column=0)
tk.Entry(root, width=50, name='codigo_entry').grid(row=4, column=1)
nome_entry = tk.Entry(root, width=50)
nome_entry.grid(row=0, column=1)

descricao_entry = tk.Entry(root, width=50)
descricao_entry.grid(row=1, column=1)

preco_entry = tk.Entry(root, width=20)
preco_entry.grid(row=2, column=1)

quantidade_entry = tk.Entry(root, width=20)
quantidade_entry.grid(row=3, column=1)

codigo_entry = tk.Entry(root, width=50)
codigo_entry.grid(row=4, column=1)

tk.Button(root, text='Cadastrar', command=lambda: adicionar_produto({
        'nome': nome_entry.get(),
        'descricao': descricao_entry.get(),
        'preco': float(preco_entry.get()),
        'quantidade': int(quantidade_entry.get()),
        'codigo_barras': codigo_entry.get()
    })).grid(row=5, column=1)



def listar_produtos():
    print("\n---- Lista de Produtos ----")
    for produto in estoque:
        print(f"{produto['codigo']} - {produto['nome']} - R$ {produto['preco']:.2f} - Quantidade: {produto['quantidade']}")
    
def vender_produto():
    print("\n---- Produtos Disponíveis ----")
    for produto in estoque:
        print(f"{produto['codigo']} - {produto['nome']} - R$ {produto['preco']:.2f}")

    codigo = input("\nDigite o código do produto que deseja comprar: ")
    produto = None
    for p in estoque:
        if p["codigo"] == codigo:
            produto = p
            break

    if produto is None:
        print("Produto não encontrado.")
    else:
        quantidade = int(input("Digite a quantidade que deseja comprar: "))
        if quantidade > produto["quantidade"]:
            print("Não há estoque suficiente para atender a demanda.")
        else:
            total = quantidade * produto["preco"]
            print(f"Valor total da compra: R$ {total:.2f}")

            produto["quantidade"] -= quantidade
            print(f"Compra realizada com sucesso. {quantidade} unidades de {produto['nome']} foram vendidas.")

def cadastrar_produto():
    codigo = input("\nDigite o código do produto: ")
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    
    estoque.append({"codigo": codigo, "nome": nome, "preco": preco, "quantidade": quantidade})
    
def main():
    while True:
        print("\n---- Menu Principal ----")
        print("1 - Cadastrar Produto")
        print("2 - Listar Produtos")
        print("3 - Vender Produto")
        print("0 - Sair")
        opcao = input("Digite uma opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            vender_produto()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            
if __name__ == "__main__":
    estoque = []
    main()

# Inicia a janela principal
root.mainloop()
