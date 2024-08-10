import numpy as np
import tkinter as tk

inventory = np.empty((1, 4), object) # Una matriz autoincrementable de 4 columnas

def exist_prod(name):
    # Obtener la primera columna (Nombre) del inventario
    name_column = inventory[:, 1]

    # Comprobar si el nombre del producto está en la columna
    return name in name_column

def update_prod_list():
    # Limpiar los campos de entrada (Se usa 0,tk.END para vaciar widgets Entry)
    name_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def add_prod():
    # Acceder al inventario global para sobreescribirlo luego
    global inventory
    
    try:
        name = name_entry.get().strip().capitalize()
        stock = int(stock_entry.get())
        price = round(float(price_entry.get()), 2) # Limitar el precio a 2 decimales
    
        # Comprobar que el campo de nombre no esté vacío
        if not name:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: El nombre del producto no puede estar vacío")
            return
    
    except ValueError:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error, por favor ingrese valores válidos para Stock y/o Precio")
        return

    # Comprobar si el producto ya existe en el inventario
    if exist_prod(name):
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f'Error: El producto {name} ya existe en el inventario.')
    
    if stock <= 0:
        output_text.insert(tk.END, "Error: El valor de stock debe ser mayor a 0.")
        return
    if price <= 0:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: El precio del producto debe ser mayor a 0.")
        return
    
    # Buscar la primera fila vacía en el inventario
    for i in range(len(inventory)):
        if inventory[i,0] is None:
            # Agregar nuevo producto a la primera fila vacía
            id = i+1
            inventory[i] = [id, name, stock, price]

            update_prod_list()

            # Test de que los productos se agregan correctamente (BORRAR)
            print("-----------*------------")
            print(inventory)

            return

    # Si no hay filas vacías crear nuevo inventario con una fila más y reasignarlo a inventory
    id = len(inventory)+1
    new_inventory = np.vstack((inventory, [id, name, stock, price]))
    inventory = new_inventory

    update_prod_list()

    # Test de que los productos se agregan correctamente (BORRAR)
    print("-----------*------------")
    print(inventory)

def program():
    global name_entry, stock_entry, price_entry, output_text, search_entry

    root = tk.Tk()
    root.title("Gestión de Inventario")

    menu = tk.Menu(root)
    menu2 = tk.Menu(menu, tearoff=0)
    menu2.add_command(label="Guardar Inventario")
    menu2.add_command(label="Cargar Inventario")
    menu2.add_command(label="Salir", command=root.quit)
    menu.add_cascade(label="Archivo", menu=menu2)
    root.config(menu=menu)

    # Crear los widgets
    name_label = tk.Label(root, text="Nombre del producto:")
    name_entry = tk.Entry(root)
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    stock_label = tk.Label(root, text="Stock:")
    stock_entry = tk.Spinbox(root, from_=0, to=100, width=5)
    stock_label.grid(row=1, column=0, padx=10, pady=10)
    stock_entry.grid(row=1, column=1, padx=10, pady=10)

    price_label = tk.Label(root, text="Precio unitario:")
    price_entry = tk.Entry(root)
    price_label.grid(row=2, column=0, padx=10, pady=10)
    price_entry.grid(row=2, column=1, padx=10, pady=10)

    search_label = tk.Label(root, text="Buscar Producto:")
    search_entry = tk.Entry(root)
    search_button = tk.Button(root, text="Buscar")
    search_label.grid(row=3, column=0, padx=10, pady=10)
    search_entry.grid(row=3, column=1, padx=10, pady=10)
    search_button.grid(row=3, column=2, padx=10, pady=10)

    add_button = tk.Button(root, text="Agregar Producto", command=add_prod)
    del_button = tk.Button(root, text="Eliminar Producto")
    modify_stock_button = tk.Button(root, text="Modificar Stock")
    modify_price_button = tk.Button(root, text="Modificar Precio")
    total_button = tk.Button(root, text="Calcular Valor Total")
    show_inventory_button = tk.Button(root, text="Ver Inventario Completo")
    add_button.grid(row=4, column=0, padx=5, pady=10)
    del_button.grid(row=4, column=1, padx=5, pady=10)
    modify_stock_button.grid(row=5, column=0, padx=5, pady=10)
    modify_price_button.grid(row=5, column=1, padx=5, pady=10)
    total_button.grid(row=6, column=0, padx=5, pady=10)
    show_inventory_button.grid(row=6, column=1, padx=5, pady=10)

    output_text = tk.Text(root, height=3, width=50, highlightthickness=1, highlightbackground="gray")
    output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

program()