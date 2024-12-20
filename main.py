from inventory import Inventory
import tkinter as tk
from tkinter import ttk
from styles import *

my_inventory = Inventory()

def name_product():
    product_name = name_entry.get().strip().title()  # Obtener y limpiar el texto
    if product_name:  # Verificar si está vacío
        return product_name
    else:
        print_on_output("Error: El nombre del producto no puede estar vacío.")
        return None
    
    
def validate_stock():
    try:
        stock_value = stock_entry.get().strip()  # Obtener y limpiar el texto
        if not stock_value:  # Verificar si está vacío
            print_on_output("Error: El campo de stock no puede estar vacío.")
            return None
        
        new_stock = int(stock_value)
        if new_stock > 0:  
            return new_stock
        else:
            print_on_output("Error: El stock debe ser un número entero mayor a 0.")
            return None            
    except ValueError:
        print_on_output("Error: El stock debe ser numérico.")
        return None


def validate_price():
    try:
        price_value = price_entry.get().strip()  # Obtener y limpiar el texto
        if not price_value:  # Verificar si está vacío
            print_on_output("Error: El campo de precio no puede estar vacío.")
            return None

        new_price = float(price_value)
        if new_price > 0:
            return round(new_price, 2)
        else:
            print_on_output("Error: El precio debe ser un número real mayor a 0.")
            return None
    except ValueError:
        print_on_output("Error: El precio debe ser numérico.")
        return None


def add_product():
    try:
        name = name_product()
        if name is None:
            return
        stock = validate_stock()
        if stock is None:
            return
        price = validate_price()
        if price is None:
            return
    
        if my_inventory.exist_product(name):
            print_on_output(f'Error: El producto {name} ya existe en el inventario.')
            clean_entries()
            return

        # Agregar a la base de datos
        my_inventory.add_product(name, price, stock)
        print_on_output(f'El producto "{name}" ha sido agregado exitosamente.')
        clean_entries()
        update_treeview()
        
    except Exception as e:
        print_on_output(f"Error inesperado: {e}")

    return



def modify_stock():
    selected_items = product_tree.selection()
    new_stock = validate_stock()
    output = ""
    if selected_items:
        if new_stock:
            clean_entries()
            for item in selected_items:
                product_values = product_tree.item(item)["values"]
                product_name = product_values[1]
            
                my_inventory.modify_stock(product_name, new_stock)
                output = output + f"Stock del producto '{product_name}' actualizado a {new_stock}.\n"
            
            print_on_output(output)
            update_treeview()
        else:
            return
    else:
        print_on_output("Error: Debes seleccionar al menos un producto.")


def low_stock_report():
    low_stock = my_inventory.low_stock_report()
    output = "Productos con stock menor a 5:\n"
    for product in low_stock:
        output = output + f"{product[1]}: {product[3]}.\n"
        print_on_output(output)


def modify_price():
    selected_items = product_tree.selection()
    new_price = validate_price()
    output = ""
    if selected_items:
        if new_price:
            clean_entries()
            for item in selected_items:
                product_values = product_tree.item(item)["values"]
                product_name = product_values[1]

                my_inventory.modify_price(product_name, new_price)
                output = output + f"Precio del producto '{product_name}' actualizado a {new_price}.\n"
            
            print_on_output(output)
            update_treeview()
        else:
            return
    else:
        print_on_output("Error: Debes seleccionar al menos un producto.")


def calculate_total_value():
    total_value = my_inventory.calculate_total_value()
    print_on_output(f"El valor total del inventario es: {round(total_value,2)}")


def search_product():
    search_term = search_entry.get().strip().lower()
    
    for row in product_tree.get_children():
        product_tree.delete(row)
        
    # Obtener los productos del inventario filtrados por el término de búsqueda
    filter_inventory = my_inventory.search_product(search_term)
        
    # Insertar productos en el Treeview
    for item in filter_inventory:
        product_tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3]))


def delete_product():
    if product_tree.selection():
        # La nueva ventana Toplevel se asocia con la principal.
        confirm_del_root = tk.Toplevel(root)
        confirm_del_root.title("Eliminar elementos")
        confirm_del_root.transient(root)
        # El usuario no puede usar la ventana principal hasta cerrar esta
        confirm_del_root.grab_set()
        apply_violet_bg(confirm_del_root)

        # Obtener las dimensiones de la ventana principal
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # Calcula las coordenadas para centrar la ventana emergente
        confirm_del_root_width = 450
        confirm_del_root_height = 400
        confirm_del_root_x = root.winfo_x() + (root_width // 2) - (confirm_del_root_width // 2)
        confirm_del_root_y = root.winfo_y() + (root_height // 2) - (confirm_del_root_height // 2)

        # Establece la posición y el tamaño de la ventana emergente
        confirm_del_root.geometry(f"{confirm_del_root_width}x{confirm_del_root_height}+{int(confirm_del_root_x)}+{int(confirm_del_root_y)}")

        del_label = tk.Label(confirm_del_root, text="Confirma que desea eliminar los siguientes elementos: ")
        apply_violet_label(del_label)
        del_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        #Eliminacion de todos los productos seleccionados y actualización del treeview
        def confirm_and_destroy():
            output = ""
            for product in delete_tree.get_children():
                product_name = delete_tree.item(product)["values"][1]
                my_inventory.delete_product(product_name)
                output = output + f"Producto '{product_name}' eliminado.\n"
            confirm_del_root.destroy()
            print_on_output(output)
            update_treeview()

        # Tkinter interfaz para confirmar la eliminación de productos
        confirm_button = tk.Button(confirm_del_root, text="Confirmar", command=confirm_and_destroy)
        confirm_button.grid(row=1, column=0)
        apply_violet_button(confirm_button)
        cancel_button = tk.Button(confirm_del_root, text="Cancelar", command=confirm_del_root.destroy)
        cancel_button.grid(row=1, column=1)
        apply_violet_button(cancel_button)

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
    else:
        print_on_output("Error: Debes seleccionar al menos un producto.")


def print_on_output(texto):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, texto)
    output_text.config(state="disabled")


def clean_entries():
    # Limpiar los campos de entrada y colocar foco en el name_entry (Se usa 0,tk.END para vaciar widgets Entry)
    name_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    name_entry.focus_set()


def update_treeview():
    for row in product_tree.get_children():
        product_tree.delete(row)
    
    # Obtener los productos del inventario actualizado
    inventory = my_inventory.show_inventory()

    # Insertar productos en el Treeview
    for item in inventory:
        product_tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3]))


def orderBy(type):
    for row in product_tree.get_children():
        product_tree.delete(row)
    
    # Obtener los productos del inventario actualizado
    inventory = my_inventory.sort_by(type)
    
    # Insertar productos en el Treeview
    for item in inventory:
        product_tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3]))


def main_menu():
    global root, name_entry, stock_entry, price_entry, output_text, search_entry, product_tree

    root = tk.Tk()
    root.title("Gestión de Inventario")

    # Configurar el tamaño inicial de la ventana
    root.geometry("620x700")

    # Asegurarse de que las dimensiones de la ventana estén actualizadas
    root.update_idletasks()

    # Obtener el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obtener el ancho y alto de la ventana
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calcular las coordenadas para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Ajustar la posición de la ventana
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Crear los widgets
    name_label = tk.Label(root, text="Nombre del producto:")
    apply_violet_label(name_label)
    name_entry = tk.Entry(root)
    apply_violet_entry(name_entry)
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    stock_label = tk.Label(root, text="Stock:")
    apply_violet_label(stock_label)
    stock_entry = tk.Spinbox(root, from_=0, to=100, width=5)
    apply_violet_entry(stock_entry)
    stock_label.grid(row=1, column=0, padx=10, pady=10)
    stock_entry.grid(row=1, column=1, padx=10, pady=10)

    price_label = tk.Label(root, text="Precio unitario:")
    apply_violet_label(price_label)
    price_entry = tk.Entry(root)
    apply_violet_entry(price_entry)
    price_label.grid(row=2, column=0, padx=10, pady=10)
    price_entry.grid(row=2, column=1, padx=10, pady=10)

    search_label = tk.Label(root, text="Buscar Producto:")
    apply_violet_label(search_label)
    search_entry = tk.Entry(root)
    apply_violet_entry(search_entry)
    search_button = tk.Button(root, text="Buscar", command=search_product)
    apply_violet_button(search_button)
    search_label.grid(row=3, column=0, padx=10, pady=10)
    search_entry.grid(row=3, column=1, padx=10, pady=10)
    search_button.grid(row=3, column=2, padx=10, pady=10)

    add_button = tk.Button(root, text="Agregar Producto", command=add_product)
    del_button = tk.Button(root, text="Eliminar Producto", command=delete_product)
    modify_stock_button = tk.Button(root, text="Modificar Stock", command=modify_stock)
    modify_price_button = tk.Button(root, text="Modificar Precio", command=modify_price)
    total_button = tk.Button(root, text="Calcular Valor Total", command=calculate_total_value) 
    low_stock_button = tk.Button(root, text="Reporte de Bajo Stock", command=low_stock_report)
    add_button.grid(row=4, column=0, padx=5, pady=10)
    del_button.grid(row=4, column=1, padx=5, pady=10)
    modify_stock_button.grid(row=4, column=2, padx=5, pady=10)
    modify_price_button.grid(row=5, column=0, padx=5, pady=10)
    total_button.grid(row=5, column=1, padx=5, pady=10)
    low_stock_button.grid(row=5, column=2, padx=5, pady=10)
    apply_violet_button(add_button)
    apply_violet_button(del_button)
    apply_violet_button(modify_stock_button)
    apply_violet_button(modify_price_button)
    apply_violet_button(total_button)
    apply_violet_button(low_stock_button)
    
    # Vincular el evento <Return> a la función add_prod() Para que al precionar **Enter** en cualquiera de estos campos agregue el producto
    name_entry.bind("<Return>", lambda event: add_product())
    stock_entry.bind("<Return>", lambda event: add_product())
    price_entry.bind("<Return>", lambda event: add_product())

    # Vincular el evento <Return> a la función search_prod()
    search_entry.bind("<Return>", lambda event: search_product())

    output_text = tk.Text(root, height=3, width=50, highlightthickness=1, highlightbackground="gray", bg="#F3E8FF", fg="#5D3FD3", font=("Times", 12))
    output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    output_text_scrollbar = ttk.Scrollbar(root, orient="vertical", command=output_text.yview)
    output_text_scrollbar.grid(row=7, column=3, padx=10, pady=10, sticky="ns")
    output_text_scrollbar.configure(command=output_text.yview)

    # Crear un estilo para el Treeview
    style = ttk.Style()
    # Configurar el estilo del Treeview
    style.configure("Treeview",
                    background="#E6E6FA",  # Color de fondo
                    foreground="#5D3FD3",  # Color del texto
                    rowheight=25,          # Altura de las filas
                    font=("Times", 12))    # Fuente de las filas

    # Configurar el estilo del encabezado
    style.configure("Treeview.Heading",
                    background="#A45DBD",  # Color de fondo del encabezado (violeta más claro)
                    foreground="#5D3FD3",   # Color del texto del encabezado (violeta oscuro)
                    font=("Times", 12, "bold"))  # Fuente del encabezado

    # Crear Treeview (Lista seleccionable)
    product_tree = ttk.Treeview(root, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    product_tree_scrollbar = ttk.Scrollbar(root, command=product_tree.yview)

    # Vincular el evento <Delete> a la función delete_prod() Presionar Delete activa la función
    product_tree.bind("<Delete>", lambda event: delete_product())        
    
    # Establecer el título de las columnas
    product_tree.heading("ID", text="ID", command=lambda: update_treeview())
    product_tree.heading("Nombre", text="Nombre", command=lambda: orderBy("name"))
    product_tree.heading("Precio", text="Precio", command=lambda: orderBy("price"))
    product_tree.heading("Stock", text="Stock", command=lambda: orderBy("stock"))    
    
    # Establecer el ancho de las columnas
    product_tree.column("ID", width=40)
    product_tree.column("Nombre", width=200)
    product_tree.column("Precio", width=80)
    product_tree.column("Stock", width=80)

    
    # sticky="nsew" hace que el widget se expanda dentro de la celda hacia North, South, West, East
    product_tree.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    product_tree_scrollbar.grid(row=8, column=3, padx=10, pady=10, sticky="ns")

    product_tree.configure(yscrollcommand=product_tree_scrollbar.set)
    product_tree_scrollbar.configure(command=product_tree.yview)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Al iniciar el programa coloca el foco en el primer campo (Entry)
    name_entry.focus_set()
    
    # Configurar el peso de las columnas 0,1 y 2 para que todas se redimensionen proporcionalmente
    for col in range(3):
        root.grid_columnconfigure(col, weight=1)

    update_treeview()
    
    root.mainloop()


if __name__ == "__main__":
    main_menu()
