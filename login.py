"""Pantalla de inicio de sesión de BUS SYSTEM PRO.
 
- Máximo 3 intentos. Al fallar el tercero, el programa se cierra.
- No modifica main.py, services.py ni storage.py.
- Se usa desde iniciar.py.
"""
import hashlib
import tkinter as tk
from tkinter import messagebox
 
# Mismos colores del sistema principal
NAVY = '#10365d'
TEAL = '#00a8b7'
BG = '#edf3f8'
RED = '#d64545'
 
MAX_INTENTOS = 3
 
# Credenciales (la contraseña se guarda como hash SHA-256, no en texto plano).
# Usuario: admin  |  Contraseña: admin123
USUARIOS = {
    'admin': hashlib.sha256('admin123'.encode('utf-8')).hexdigest(),
}
 
 
def _hash(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()
 
 
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BUS SYSTEM PRO | Iniciar sesión')
        self.resizable(False, False)
        self.configure(bg=BG)
        self.autenticado = False
        self.intentos = 0
        self._centrar(720, 440)
 
        # Panel izquierdo (marca)
        izq = tk.Frame(self, bg=NAVY, width=280, height=440)
        izq.pack(side='left', fill='y')
        izq.pack_propagate(False)
        tk.Label(izq, text='🚌', bg=NAVY, fg='white', font=('Arial', 56)).pack(pady=(90, 5))
        tk.Label(izq, text='BUS SYSTEM PRO', bg=NAVY, fg='white', font=('Arial', 17, 'bold')).pack()
        tk.Label(izq, text='Gestión de transporte terrestre', bg=NAVY, fg='#a9c4de',
                 font=('Arial', 10)).pack(pady=(6, 0))
 
        # Panel derecho (formulario)
        der = tk.Frame(self, bg='white', padx=40)
        der.pack(side='right', expand=True, fill='both')
        tk.Label(der, text='Bienvenido', bg='white', fg='#132638', font=('Arial', 22, 'bold')).pack(anchor='w', pady=(48, 2))
        tk.Label(der, text='Ingrese sus credenciales para continuar', bg='white', fg='#6b7c8d',
                 font=('Arial', 10)).pack(anchor='w', pady=(0, 22))
 
        tk.Label(der, text='USUARIO', bg='white', fg=NAVY, font=('Arial', 9, 'bold')).pack(anchor='w')
        self.usuario = tk.Entry(der, font=('Arial', 12), relief='solid', bd=1,
                                highlightthickness=1, highlightcolor=TEAL, highlightbackground='#c5d3e0')
        self.usuario.pack(fill='x', ipady=6, pady=(3, 14))
 
        tk.Label(der, text='CONTRASEÑA', bg='white', fg=NAVY, font=('Arial', 9, 'bold')).pack(anchor='w')
        fila = tk.Frame(der, bg='white')
        fila.pack(fill='x', pady=(3, 4))
        self.clave = tk.Entry(fila, font=('Arial', 12), show='•', relief='solid', bd=1,
                              highlightthickness=1, highlightcolor=TEAL, highlightbackground='#c5d3e0')
        self.clave.pack(side='left', fill='x', expand=True, ipady=6)
        self.ver = tk.BooleanVar(value=False)
        tk.Checkbutton(fila, text='Ver', variable=self.ver, command=self._toggle, bg='white',
                       activebackground='white', font=('Arial', 9)).pack(side='left', padx=(8, 0))
 
        self.mensaje = tk.Label(der, text='', bg='white', fg=RED, font=('Arial', 10, 'bold'),
                                wraplength=340, justify='left')
        self.mensaje.pack(anchor='w', pady=(8, 0))
        self.contador = tk.Label(der, text=f'Intentos restantes: {MAX_INTENTOS}', bg='white',
                                 fg='#6b7c8d', font=('Arial', 9))
        self.contador.pack(anchor='w', pady=(2, 14))
 
        self.boton = tk.Button(der, text='INGRESAR', command=self.validar, bg=TEAL, fg='white',
                               activebackground=NAVY, activeforeground='white', relief='flat',
                               font=('Arial', 11, 'bold'), cursor='hand2', pady=10)
        self.boton.pack(fill='x')
 
        self.bind('<Return>', lambda e: self.validar())
        self.protocol('WM_DELETE_WINDOW', self.cancelar)
        self.usuario.focus_set()
 
    def _centrar(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f'{ancho}x{alto}+{x}+{y}')
 
    def _toggle(self):
        self.clave.config(show='' if self.ver.get() else '•')
 
    def validar(self):
        usuario = self.usuario.get().strip()
        clave = self.clave.get()
        if not usuario or not clave:
            self.mensaje.config(text='Complete usuario y contraseña.')
            return
        if USUARIOS.get(usuario) == _hash(clave):
            self.autenticado = True
            self.destroy()
            return
 
        self.intentos += 1
        restantes = MAX_INTENTOS - self.intentos
        self.clave.delete(0, 'end')
        if restantes <= 0:
            messagebox.showerror('Acceso denegado',
                                 'Superó los 3 intentos permitidos.\nEl sistema se cerrará.', parent=self)
            self.autenticado = False
            self.destroy()
            return
        self.mensaje.config(text='Usuario o contraseña incorrectos.')
        self.contador.config(text=f'Intentos restantes: {restantes}', fg=RED)
        self.clave.focus_set()
 
    def cancelar(self):
        self.autenticado = False
        self.destroy()
 
 
def pedir_login():
    """Muestra el login. Devuelve True si el acceso fue correcto, False si no."""
    ventana = LoginWindow()
    ventana.mainloop()
    return ventana.autenticado
 
 
if __name__ == '__main__':
    # Permite ejecutar directamente:  python login.py
    if pedir_login():
        from main import App
        App().mainloop()
 