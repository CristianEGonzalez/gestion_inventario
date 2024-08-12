import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

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
        name = name_entry.get().strip().title()
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

def save_inventory():
    # Abrir un cuadro de diálogo para seleccionar la ubicación y nombre del archivo
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Guardar inventario"
    )

    if file_path:
        # Convertir el inventario en una lista de diccionarios
        inventory_data = []
        for product in inventory:
            if product[0] is not None:
                inventory_data.append({
                    "id": product[0],
                    "name": product[1],
                    "stock": int(product[2]),
                    "price": float(product[3])
                })
        # Guardar el inventario en el archivo seleccionado
        with open(file_path, "w") as f:
            json.dump(inventory_data, f)
        
        # Agregar mensaje de confirmación a la salida
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f'Inventario guardado en el archivo "{file_path}".')
    
    else:
        # Si el usuario cancela la operación no hacer nada
        pass

def load_inventory():
    # Acceder al inventario global para luego sobreescribirlo
    global inventory
    
    # Abrir un cuadro de diálogo para seleccionar el archivo a cargar
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos JSON", "*.json")],
        title="Cargar inventario"
    )

    if file_path:
        try:
            # Cargar los datos del inventario desde el archivo JSON seleccionado
            with open(file_path, "r") as f:
                inventory_data = json.load(f)
            
            # Limpiar el inventario existente
            for i in range(len(inventory)):
                inventory[i] = [None, None, None, None]

            # Crear una nueva matriz con la cantidad de registros(filas) como tantos productos tenga el json
            inventory = np.empty((len(inventory_data), 4), object)
        
            # Limpiar el product_tree
            for item in product_tree.get_children():
                product_tree.delete(item)
            
            # Llenar el inventario y el product_tree con los datos cargados
            for i, product in enumerate(inventory_data):
                inventory[i] = [product["id"], product["name"], product["stock"], product["price"]]
                product_tree.insert("", i, text=product["name"], values=(product["id"], product["name"], product["stock"], product["price"]))

            # Agregar mensaje de confirmación a la salida
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f'Inventario cargado desde el archivo:\n "{file_path}".')
        
        except FileNotFoundError:
            # Si el archivo no existe, agregar un mensaje de error a la salida:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: El archivo seleccionado no se encontró.")
        except json.JSONDecodeError:
            # Si hay un error al cargar los datos JSON, agregar un mensaje de error a la salida
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Error: El archivo JSON está corrupto o tiene un formato incorrecto.")
        
    else:
        # Si el usuario cancela la operación, no hacer nada
        pass

def sort_tree(column_id, reverse=False): # Función para organizar las columnas al clickearlas
    # Obtener los datos del Treeview
    items = [(product_tree.set(child, column_id), child) for child in product_tree.get_children('')]

    # Ordenar columnas numéricas (ID, Stock y Precio)
    if column_id == 0 or column_id == 2 or column_id == 3:  
        items.sort(key=lambda x: float(x[0]), reverse=reverse)
    else:  # Ordenar columna de texto (Nombre)
        items.sort(reverse=reverse)

    # Mover los elementos del product_tree según el nuevo orden
    for index, (value, child) in enumerate(items):
        product_tree.move(child, '', index)

    # Actualizar el estado del ordenamiento en el encabezado de la columna seleccionada
    if reverse:
        product_tree.heading(column_id, text=product_tree.heading(column_id)['text'], command=lambda: sort_tree(column_id, False))
    else:
        product_tree.heading(column_id, text=product_tree.heading(column_id)['text'], command=lambda: sort_tree(column_id, True))

def confirm_del():
    # La nueva ventana Toplevel se asocia con la principal.
    confirm_del_root = tk.Toplevel(root)
    confirm_del_root.title("Eliminar elementos")
    confirm_del_root.transient(root)
    # El usuario no puede usar la ventana principal hasta cerrar esta
    confirm_del_root.grab_set()

    # Obtener las dimensiones de la ventana principal
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # Calcula las coordenadas para centrar la ventana emergente
    confirm_del_root_width = 450
    confirm_del_root_height = 320
    confirm_del_root_x = root.winfo_x() + (root_width // 2) - (confirm_del_root_width // 2)
    confirm_del_root_y = root.winfo_y() + (root_height // 2) - (confirm_del_root_height // 2)

    # Establece la posición y el tamaño de la ventana emergente
    confirm_del_root.geometry(f"{confirm_del_root_width}x{confirm_del_root_height}+{int(confirm_del_root_x)}+{int(confirm_del_root_y)}")

    label = tk.Label(confirm_del_root, text="Confirma que desea eliminar los siguientes elementos: ")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def confirm_and_destroy():
        delete_prod()
        confirm_del_root.destroy()

    confirm_button = tk.Button(confirm_del_root, text="Confirmar", command=confirm_and_destroy)
    confirm_button.grid(row=1, column=0)
    cancel_button = tk.Button(confirm_del_root, text="Cancelar", command=confirm_del_root.destroy)
    cancel_button.grid(row=1, column=1)

    delete_tree = ttk.Treeview(confirm_del_root, columns=("ID", "Nombre", "Stock", "Precio"), show="headings")
    delete_tree_scrollbar = tk.Scrollbar(confirm_del_root, command=product_tree.yview)

    delete_tree.heading("ID", text="ID")
    delete_tree.heading("Nombre", text="Nombre")
    delete_tree.heading("Stock", text="Stock")
    delete_tree.heading("Precio", text="Precio")
    delete_tree.column("ID", width=40)
    delete_tree.column("Nombre", width=200)
    delete_tree.column("Stock", width=80)
    delete_tree.column("Precio", width=80)

    delete_tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    delete_tree_scrollbar.grid(row=2, column=2, padx=10, pady=10, sticky="ns")

    delete_tree.configure(yscrollcommand=delete_tree_scrollbar.set)
    delete_tree_scrollbar.configure(command=product_tree.yview)

    all_selected_items = product_tree.selection()
    for selected_item in all_selected_items:
        product_info = product_tree.item(selected_item)["values"]
        delete_tree.insert("", tk.END, values=([product_info[0],product_info[1], product_info[2], product_info[3]]))

def confirm_quit():
    quit_root = tk.Toplevel()
    quit_root.title("Salir")
    quit_root.transient(root)
    quit_root.grab_set()

    # Obtener las dimensiones de la ventana principal
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # Calcula las coordenadas para centrar la ventana emergente
    quit_root_width = 250
    quit_root_height = 100
    quit_root_x = root.winfo_x() + (root_width // 2) - (quit_root_width // 2)
    quit_root_y = root.winfo_y() + (root_height // 2) - (quit_root_height // 2)

    # Establece la posición y el tamaño de la ventana emergente
    quit_root.geometry(f"{quit_root_width}x{quit_root_height}+{int(quit_root_x)}+{int(quit_root_y)}")

    label = tk.Label(quit_root, text="¿Desea guardar los cambios antes de salir?")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def save_and_quit():
        save_inventory()
        root.quit()

    confirm_button = tk.Button(quit_root, text="Guardar Cambios", command=save_and_quit)
    cancel_button = tk.Button(quit_root, text="Salir sin Guardar", command=root.quit)
    confirm_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    cancel_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

def program():
    global root, name_entry, stock_entry, price_entry, output_text, search_entry, product_tree

    root = tk.Tk()
    root.title("Gestión de Inventario")

    # Obtener el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular la posición x para centrar horizontalmente
    x = (screen_width - root.winfo_reqwidth()) // 2

    # Calcular la posición y para que la ventana quede un poco por encima del centro
    window_height = root.winfo_reqheight()
    y = (screen_height - window_height) // 4

    # Establecer la posición de la ventana
    root.geometry(f"+{x}+{y}")

    menu = tk.Menu(root)
    menu2 = tk.Menu(menu, tearoff=0)
    menu2.add_command(label="Guardar Inventario", command=save_inventory)
    menu2.add_command(label="Cargar Inventario", command=load_inventory)
    menu2.add_command(label="Salir", command=confirm_quit)
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
    del_button = tk.Button(root, text="Eliminar Producto", command=confirm_del)
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
    product_tree.bind("<Delete>", lambda event: confirm_del())
    
    # Establecer el título de las columnas
    product_tree.heading("ID", text="ID", command=lambda: sort_tree(0))
    product_tree.heading("Nombre", text="Nombre", command=lambda: sort_tree(1))
    product_tree.heading("Stock", text="Stock", command=lambda: sort_tree(2))
    product_tree.heading("Precio", text="Precio", command=lambda: sort_tree(3))
    
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
