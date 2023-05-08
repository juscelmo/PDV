import sqlite3
import os
import tkinter as tk
from tkinter import messagebox

# Cria ou conecta ao banco de dados
conn = sqlite3.connect('pdv.db')

# Cria tabela de produtos
def create_product_table(conn):
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

def add_product(conn, produto):
    try:
        with conn:
            conn.execute('''
            INSERT INTO produtos (nome, descricao, preco, quantidade, codigo_barras)
            VALUES (?, ?, ?, ?, ?)
            ''', (produto['nome'], produto['descricao'], produto['preco'], produto['quantidade'], produto['codigo_barras']))
        messagebox.showinfo(title='Produto cadastrado', message='O produto foi cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        messagebox.showerror(title='Erro', message=f"O código de barras '{produto['codigo_barras']}' já está em uso.")

def search_products(conn, name):
    cursor = conn.execute("SELECT nome, quantidade, preco FROM produtos WHERE nome LIKE ?", ('%' + name + '%',))
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def create_search_window():
    # Cria a janela de busca de produtos
    search_window = tk.Toplevel(root)
    search_window.title('Busca de Produtos')

    # Cria os widgets
    tk.Label(search_window, text='Nome do produto:').grid(row=0, column=0)
    search_entry = tk.Entry(search_window, width=50)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_window, text='Buscar', command=lambda: search_products(search_entry.get()))
    search_button.grid(row=1, column=1)

    result_text = tk.Text(search_window, width=50, height=10)
    result_text.grid(row=2, column=0, columnspan=2)

    def search_products(name):
        # Executa a consulta no banco de dados
        cursor = conn.execute("SELECT nome, quantidade, preco FROM produtos WHERE nome LIKE ?", ('%' + name + '%',))
        results = cursor.fetchall()

        # Exibe os resultados na janela de busca
        result_text.delete(1.0, tk.END)
        for result in results:
            name = result[0]
            quantity = result[1]
            price = result[2]
            result_text.insert(tk.END, f"{name}\t{quantity}\t{price}\n")

        # Fecha a conexão do cursor
        cursor.close()

    return search_window


inventory = {}

# Função para adicionar produto ao inventário
def add_to_inventory(product):
    if product['nome'] in inventory:
        inventory[product['nome']]['quantidade'] += product['quantidade']
    else:
        inventory[product['nome']] = product
    print(f"Adicionado {product['quantidade']} {product['nome']} ao inventário.")
def start_sale():
    # Cria a janela de venda
    sale_window = tk.Toplevel(root)
    sale_window.title('Venda')

    # Cria os widgets
    tk.Label(sale_window, text='Nome do produto:').grid(row=0, column=0)
    product_entry = tk.Entry(sale_window, width=50)
    product_entry.grid(row=0, column=1)

    tk.Label(sale_window, text='Quantidade:').grid(row=1, column=0)
    quantity_entry = tk.Entry(sale_window, width=20)
    quantity_entry.grid(row=1, column=1)

    add_button = tk.Button(sale_window, text='Adicionar', command=lambda: add_to_sale(product_entry.get(), int(quantity_entry.get())))
    add_button.grid(row=2, column=1)

    checkout_button = tk.Button(sale_window, text='Finalizar venda', command=lambda: checkout_sale())
    checkout_button.grid(row=3, column=1)

    # Função para adicionar um produto à venda
    def add_to_sale(product_name, quantity):
        if product_name in inventory:
            product = inventory[product_name]
            if product['quantidade'] >= quantity:
                if product_name in sale:
                    sale[product_name]['quantidade'] += quantity
                else:
                    sale[product_name] = {'preco': product['preco'], 'quantidade': quantity}
                inventory[product_name]['quantidade'] -= quantity
                print(f"Adicionado {quantity} {product_name} à venda.")
            else:
                print(f"Não há {product_name} suficiente no inventário.")
        else:
            print(f"Não foi possível encontrar {product_name} no inventário.")

    # Função para finalizar a venda
    import tkinter as tk

# Dicionário para manter o registro dos produtos vendidos
sale = {}

def start_sale():
    global subtotal_label, total_label, amount_entry, selected_product
    # Criando as labels que irão exibir o subtotal e o total da venda
    subtotal_label = tk.Label(root, text='Subtotal: R$0.00')
    subtotal_label.grid(row=6, column=0)

    total_label = tk.Label(root, text='Total: R$0.00')
    total_label.grid(row=7, column=0)

def checkout_sale():
    total = 0
    for product_name, product_info in sale.items():
        total += product_info['preco'] * product_info['quantidade']
    print(f"Total da venda: R$ {total:.2f}")
    sale.clear()
    sale_window.destroy()

root = tk.Tk()

start_sale_button = tk.Button(root, text='Iniciar venda', command=start_sale)
start_sale_button.grid(row=5, column=0)

root.mainloop()

# Criando a entry que irá receber a quantidade de produtos que o cliente deseja comprar
quantity_label = tk.Label(root, text='Quantidade:')
quantity_label.grid(row=8, column=0)

quantity_entry = tk.Entry(root)
quantity_entry.grid(row=8, column=1)

# Criando o botão que será responsável por adicionar o produto à venda
add_button = tk.Button(root, text='Adicionar', command=add_to_sale)
add_button.grid(row=9, column=0)

# Criando a listbox que irá exibir os produtos disponíveis para venda
products_listbox = tk.Listbox(root, width=50)
products_listbox.grid(row=5, column=1, rowspan=5)

# Adicionando os produtos à listbox
for product in products:
    products_listbox.insert(tk.END, product['name'])

# Configurando o evento que será chamado ao selecionar um produto na listbox
products_listbox.bind('<<ListboxSelect>>', select_product)

# Define a função que será executada quando o botão "Iniciar venda" for clicado
def start_sale():
    global sale_started, cart
    
    if not sale_started:
        sale_started = True
        cart = [] # cria um carrinho vazio
        cart_label.config(text="Carrinho de compras:\n\n") # limpa o rótulo do carrinho
        products_listbox.selection_clear(0, tk.END) # limpa a seleção de produtos na lista
        add_to_cart_button.config(state=tk.NORMAL) # habilita o botão "Adicionar ao carrinho"
        start_sale_button.config(text="Encerrar venda") # altera o texto do botão para "Encerrar venda"
    else:
        sale_started = False
        cart_total = 0
        for item in cart:
            cart_total += item["price"] # soma o preço de todos os itens do carrinho
        messagebox.showinfo("Total da venda", f "Total da venda: R${cart_total:.2f}") # exibe o total da venda em uma caixa de mensagem
        cart = [] # limpa o carrinho
        cart_label.config(text="Carrinho de compras:\n\n") # limpa o rótulo do carrinho
        add_to_cart_button.config(state=tk.DISABLED) # desabilita o botão "Adicionar ao carrinho"
        start_sale_button.config(text="Iniciar venda") # altera o texto do botão de volta para "Iniciar venda"

# Cria um rótulo para exibir o carrinho de compras
cart_label = tk.Label(root, text="Carrinho de compras:\n\n", font=("Arial", 12))
cart_label.grid(row=4, column=1)

#Cria uma lista de produtos
product_listbox = tk.Listbox(root, width=30, height=10)
product_listbox.grid(row=3, column=0, padx=10, pady=10)

#Adiciona os produtos na lista
product_listbox.insert(tk.END, product["name"])

#Cria um botão para adicionar um produto ao carrinho
add_to_cart_button = tk.Button(root, text="Adicionar ao carrinho", state=tk.DISABLED, command=add_to_cart)
add_to_cart_button.grid(linha=4, coluna=0)

#Cria um botão para iniciar/encerrar a venda
start_sale_button = tk.Button(root, text='Iniciar venda', command=start_sale)
start_sale_button.grid(linha=5, coluna=0)

root.mainloop()
#Define a função que atualiza o subtotal e o total
def update_totals(): # Limpa a lista de produtos products_list.delete(0, tk.END) # Reinicia o subtotal e o total subtotal = 0 total = 0 # Atualiza o subtotal e adiciona cada produto na lista de produtos para produtos à venda[ "products"]: products_list.insert(tk.END, f'{product["name"]} - R${product["price"]:.2f}') subtotal += product["price"] # Atualiza o total com base no desconto e no subtotal total = subtotal - sale["discount"] # Atualiza os rótulos de subtotal e total subtotal_label.config(text=f'Subtotal: R${subtotal:.2f}') discount_label.config (text=f'Desconto: R${venda["desconto"]:.2f}') total_label.config(text=f'Total: R${total:.2f}')

#Defina a função que processa o pagamento
    def    process_payment(): # Verifica se o total é maior que zero if sale["total"] > 0: # Cria uma janela de diálogo para obter o valor do pagamento payment = simpledialog.askfloat("Pagamento", "Valor pago: ") # Verifica se o valor do pagamento é suficiente if payment >= sale["total"]: # Calcula o troco e exibe uma mensagem de sucesso change = payment - sale["total"] messagebox.showinfo("Pagamento", f'Troco: R${change:.2f}\n\nPagamento processado com sucesso!') # Reinicia a venda start_sale() else: # Exibe uma mensagem de erro se o valor do pagamento for insuficiente messagebox.showerror("Pagamento ", "Valor insuficiente!") else: # Exibe uma mensagem de erro se o total for igual a zero messagebox.showerror("Pagamento", "Não há produtos na venda!")

#Cria os rótulos de subtotal, desconto e total
        subtotal_label = tk.Label(root, text='Subtotal: R$0,00')
    subtotal_label.grid(linha=6, coluna=0, sticky='w')
    discount_label = tk.Label(root, text='Desconto: R$0,00 ')
    discount_label.grid(row=7, column=0, sticky='w')
    total_label = tk.Label(root, text='Total: R$0,00')
    total_label.grid(row=8, column=0, sticky ='w')

#Cria os botões de processamento de pagamento e cancelamento de venda
process_payment_button = tk.Button(root, text='Processar pagamento', command=process_payment)
process_payment_button.grid(linha=9, coluna=0)
cancel_sale_button = tk.Button(root, text='Cancelar venda', command=start_sale)
cancel_sale_button.grid(linha=9, coluna=1)

#Cria uma lista de produtos
lista_produtos = tk.Listbox(raiz, largura=40)
lista_produtos.grid(linha=4, coluna=1,intervalo de linhas=6)

#Crie uma barra de rolagem para uma lista de produtos
scrollbar = tk.Scrollbar(root, orient='vertical')
scrollbar.grid(row=4, column=2, rowspan=6, sticky='ns')
products_list.config(yscrollcommand=scrollbar.set)
scrollbar.config( comando=lista_de_produtos.yview)

#Inicia a interface gráfica
root.mainloop()
root
