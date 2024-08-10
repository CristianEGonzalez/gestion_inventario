import numpy as np
import tkinter as tk
from tkinter import ttk

inventory = np.empty((1, 4), object) # Una matriz autoincrementable de 4 columnas

def array_test():
    # Testear al array (BORRAR)
    print("-----------*------------")
    print(inventory)


def exist_prod(name):
    # Obtener la primera columna (Nombre) del inventario
    name_column = inventory[:, 1]

    # Comprobar si el nombre del producto está en la columna
    return name in name_column

def show_inventory(): # Función para ver el inventario completo (después de utilizar una busqueda filtrada)
    # Eliminar todos los productos que se encuentran actualmente en la lista seleccionable
    product_tree.delete(*product_tree.get_children())

    # Agregar todos los productos del inventario a la lista seleccionable
    for product in inventory:
        product_tree.insert("", tk.END, values=([int(product[0]), product[1], int(product[2]), product[3]]))
    
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Inventario completo:")

def search_prod(): # Función para filtrar en la lista seleccionable los productos que contengan determinado texto.
    search_term = search_entry.get().strip().lower()
    product_tree.delete(*product_tree.get_children())
    
    for product in inventory:
        if product[0] and (search_term in product[1].lower()):
            product_tree.insert("", tk.END, values=([int(product[0]), product[1], int(product[2]), product[3]]))
        
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f'Filtro actual: "{search_term}"')

def clean_entries():
    # Limpiar los campos de entrada y colocar foco en el name_entry (Se usa 0,tk.END para vaciar widgets Entry)
    name_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    name_entry.focus_set()

def add_prod(): # Función para agregar productos
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
        clean_entries()
        return
    
    if stock <= 0:
        output_text.delete("1.0", tk.END)
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

            # Agregar el producto a la lista seleccionable
            product_tree.insert("", tk.END, values=([id,name,stock,price]))

            clean_entries()

            # Testear al array (BORRAR)########################################
            array_test()#######################################################

            return

    # Si no hay filas vacías crear nuevo inventario con una fila más y reasignarlo a inventory
    id = len(inventory)+1
    new_inventory = np.vstack((inventory, [id, name, stock, price]))
    inventory = new_inventory

    # Agregar el producto a la lista seleccionable
    product_tree.insert("", tk.END, values=([id,name,stock,price]))

    clean_entries()

    # Testear al array (BORRAR)########################################
    array_test()#######################################################

def delete_prod(): # Función para eliminar productos
    selected_items = product_tree.selection()
    if selected_items != None: # != None es innecesario, lo puse sólo para ejemplificar que se puede usar optativamente
        for item in selected_items:
            # Obtener los valores de las columnas del elemento seleccionado
            product_values = product_tree.item(item)["values"]
            product_name = product_values[1]

            # Eliminar producto de la lista
            product_tree.delete(item)

            # Buscar el producto en el inventario (array)
            for i in range(len(inventory)):
                if inventory[i][1] == product_name:
                    #Eliminar producto del inventario
                    inventory[i] = [None, None, None, None]
                    break
        
        # Agregar mensaje de confirmación a la salida
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Producto(s) eliminado(s) del inventario.")

        clean_entries()
    else:
        # Si no se seleccionó ningún producto, mensaje de error
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: Debes seleccionar al menos un producto.")
    
    # Testear al array (BORRAR)########################################
    array_test()#######################################################
    

def modify_stock(): # Función para modificar el stock
    selected_item = product_tree.selection()
    if selected_item:
        try:
            # Obtener los valores de las columnas del elemento seleccionado
            product_values = product_tree.item(selected_item)["values"]
            product_name = product_values[1]
            new_stock = int(stock_entry.get())
        except ValueError:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: Por favor, ingrese un valor válido para el stock.")
            return
        
        if new_stock <= 0:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: El valor de stock debe ser mayor a 0.")
        else:
            for i in range(len(inventory)):
                if inventory[i][1] == product_name:
                    # Actualizar el stock del producto
                    inventory[i][2] = new_stock

                    # Actualizar el valor en el product_tree
                    product_tree.item(selected_item, values=(product_values[0],product_name, new_stock, product_values[3]))

                    # Agregar mensaje de confirmación a la salida
                    output_text.delete("1.0", tk.END)
                    output_text.insert(tk.END, f"Stock del producto '{product_name}' actualizado a {new_stock}.")
                    
                    return
    else:
        # Si no hay un producto seleccionado, agregar mensaje de error a la salida
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: Debes seleccionar un producto.")


def modify_price(): # Función para modificar el precio
    selected_item = product_tree.selection()
    if selected_item:
        try:
            # Obtener los valores de las columnas del elemento seleccionado
            product_values = product_tree.item(selected_item)["values"]
            product_name = product_values[1]
            new_price = round(float(price_entry.get()), 2) # Limitar el precio a dos decimales
        except ValueError:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: Por favor, ingrese un valor válido para el stock.")
            return

        if new_price <= 0:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: El valor de stock debe ser mayor a 0.")
        else:
            for i in range(len(inventory)):
                if inventory[i][1] == product_name:
                    # Actualizar el precio del producto
                    inventory[i][3]

                    # Actualizar el valor del producto en el product_tree
                    product_tree.item(selected_item, values=(product_values[0],product_name, product_values[2], new_price))

                    # Agregar mensaje de confirmación a la salida
                    output_text.delete("1.0", tk.END)
                    output_text.insert(tk.END, f"Precio del producto '{product_name}' actualizado a {new_price}.")

                    return
    else:
        # Si no hay un producto seleccionado, agregar mensaje de error a la salida
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: Debes seleccionar un producto.")



def calculate_total_value(): # Función para calcular el valor total del inventario
    total_value = 0

    # Iterar a través del inventario y sumar el valor de cada producto multiplicado por la cantidad de existencias
    for product in inventory:
        if product[0]: # is not None (no es necesario escribirlo)
            total_value += int(product[2]) * float(product[3])
    
    # Agregar el valor total a la salida
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f'El valor total del inventario es: ${total_value:.2f}')

def sort_tree(column):
    # Función para organizar columnas
    return

def program():
    global name_entry, stock_entry, price_entry, output_text, search_entry, product_tree

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
    search_button = tk.Button(root, text="Buscar", command=search_prod)
    search_label.grid(row=3, column=0, padx=10, pady=10)
    search_entry.grid(row=3, column=1, padx=10, pady=10)
    search_button.grid(row=3, column=2, padx=10, pady=10)

    add_button = tk.Button(root, text="Agregar Producto", command=add_prod)
    del_button = tk.Button(root, text="Eliminar Producto", command=delete_prod)
    modify_stock_button = tk.Button(root, text="Modificar Stock", command=modify_stock)
    modify_price_button = tk.Button(root, text="Modificar Precio", command=modify_price)
    total_button = tk.Button(root, text="Calcular Valor Total", command=calculate_total_value)
    show_inventory_button = tk.Button(root, text="Ver Inventario Completo", command=show_inventory)
    add_button.grid(row=4, column=0, padx=5, pady=10)
    del_button.grid(row=4, column=1, padx=5, pady=10)
    modify_stock_button.grid(row=5, column=0, padx=5, pady=10)
    modify_price_button.grid(row=5, column=1, padx=5, pady=10)
    total_button.grid(row=6, column=0, padx=5, pady=10)
    show_inventory_button.grid(row=6, column=1, padx=5, pady=10)

    # Vincular el evento <Return> a la función add_prod() Para que al precionar **Enter** en cualquiera de estos campos agregue el producto
    name_entry.bind("<Return>", lambda event: add_prod())
    stock_entry.bind("<Return>", lambda event: add_prod())
    price_entry.bind("<Return>", lambda event: add_prod())

    # Vincular el evento <Return> a la función search_prod()
    search_entry.bind("<Return>", lambda event: search_prod())

    output_text = tk.Text(root, height=3, width=50, highlightthickness=1, highlightbackground="gray")
    output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Crear Treeview (Lista seleccionable)
    product_tree = ttk.Treeview(root, columns=("ID", "Nombre", "Stock", "Precio"), show="headings")
    product_tree_scrollbar = tk.Scrollbar(root, command=product_tree.yview)

    # Vincular el evento <Delete> a la función delete_prod() Presionar Delete activa la función
    product_tree.bind("<Delete>", lambda event: delete_prod())
    
    # Establecer el título de las columnas
    product_tree.heading("ID", text="ID")
    product_tree.heading("Nombre", text="Nombre")
    product_tree.heading("Stock", text="Stock")
    product_tree.heading("Precio", text="Precio")
    
    # Establecer el ancho de las columnas
    product_tree.column("ID", width=40)
    product_tree.column("Nombre", width=200)
    product_tree.column("Stock", width=80)
    product_tree.column("Precio", width=80)
    
    # sticky="nsew" hace que el widget se expanda dentro de la celda hacia North, South, West, East
    product_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    product_tree_scrollbar.grid(row=8, column=2, padx=10, pady=10, sticky="ns")

    product_tree.configure(yscrollcommand=product_tree_scrollbar.set)
    product_tree_scrollbar.configure(command=product_tree.yview)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Al iniciar el programa coloca el foco en el primer campo (Entry)
    name_entry.focus_set()

    root.mainloop()

program()
