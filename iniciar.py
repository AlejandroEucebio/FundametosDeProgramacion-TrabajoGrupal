"""Punto de entrada con login. Ejecutar:  python iniciar.py

main.py queda intacto: solo se importa la clase App después de validar el acceso.
"""
from login import pedir_login

if __name__ == '__main__':
    if pedir_login():
        from main import App
        App().mainloop()
