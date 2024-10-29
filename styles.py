# Estilos para widgets
def apply_violet_button(widget):
    widget.configure(bg="#9B5DE5", fg="white", activebackground="#6A0572", relief="flat", font=("Calibri", 12, "bold"), bd=0, padx=10, pady=5, width=20)

def apply_violet_entry(widget):
    widget.configure(bg="#E0BBE4", fg="black", font=("Times", 11), relief="flat", highlightbackground="#9B5DE5", highlightcolor="#9B5DE5", highlightthickness=2)

def apply_violet_label(widget):
    widget.configure(bg="#E6E6FA", fg="#5D3FD3", font=("Times", 12, "bold"))
    
def apply_violet_bg(root):
    root.configure(bg="#E6E6FA")