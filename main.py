import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from services import records, add, replace, seats, sell

NAVY = '#10365d'
TEAL = '#00a8b7'
BG = '#edf3f8'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BUS SYSTEM PRO | Gestión de transporte')
        self.geometry('1150x730')
        self.minsize(900, 600)
        self.configure(bg=BG)
        sidebar = tk.Frame(self, bg=NAVY, width=240)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text='🚌 BUS SYSTEM PRO', bg=NAVY, fg='white', font=('Arial', 16, 'bold'), pady=24).pack(fill='x')
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side='right', expand=True, fill='both')
        for title, callback in [('TABLERO PRINCIPAL',self.dashboard),('VENTA DE PASAJES',self.sales),('MAPA DE ASIENTOS',self.map_seats),('REGISTRO DE PASAJEROS',self.passengers),('GESTIÓN DE BUSES',self.buses),('RUTAS Y HORARIOS',self.routes),('INFORMES',self.reports),('CONFIGURACIÓN',self.settings),('CERRAR SESIÓN',self.destroy)]:
            tk.Button(sidebar, text=title, command=callback, bg=NAVY, fg='white', activebackground=TEAL, activeforeground='white', relief='flat', anchor='w', padx=18, pady=15, font=('Arial',10,'bold')).pack(fill='x')
        self.dashboard()

    def page(self, title):
        for child in self.content.winfo_children(): child.destroy()
        tk.Label(self.content, text=title, font=('Arial',20,'bold'), bg=BG, fg='#132638').pack(anchor='w', padx=28, pady=(25,18))
        panel = tk.Frame(self.content, bg='white', padx=18, pady=18)
        panel.pack(fill='both', expand=True, padx=28, pady=(0,28))
        return panel

    def dashboard(self):
        p = self.page('TABLERO PRINCIPAL - Empresa de Buses El Sol')
        sales = records('ventas')
        for label, value in [('VIAJES PROGRAMADOS',str(len(records('rutas')))),('PASAJEROS REGISTRADOS',str(len(records('pasajeros')))),('VENTAS TOTALES',f"S/ {sum(x['precio'] for x in sales):,.2f}")]:
            f = tk.Frame(p, bg='#e8f6f8', padx=20, pady=18)
            f.pack(side='top', fill='x', pady=7)
            tk.Label(f, text=label, bg='#e8f6f8', fg=NAVY, font=('Arial',11,'bold')).pack(anchor='w')
            tk.Label(f, text=value, bg='#e8f6f8', fg='#102334', font=('Arial',22,'bold')).pack(anchor='w')
        tk.Label(p, text='Seleccione una opción del menú lateral para administrar el sistema.', bg='white', font=('Arial',12)).pack(pady=20)

    def table(self, parent, columns, items):
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=13)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor='center')
        for item in items: tree.insert('', 'end', values=item)
        tree.pack(fill='both', expand=True, pady=10)
        return tree

    def passengers(self):
        p = self.page('REGISTRO DE PASAJEROS')
        toolbar = tk.Frame(p, bg='white'); toolbar.pack(fill='x')
        query = tk.StringVar()
        tk.Entry(toolbar, textvariable=query, width=30).pack(side='left', padx=5)
        data = records('pasajeros')
        def redraw():
            for row in tree.get_children(): tree.delete(row)
            for person in records('pasajeros'):
                if query.get().lower() in ' '.join(str(v) for v in person.values()).lower():
                    tree.insert('', 'end', values=(person['dni'],person['nombres'],person['apellidos'],person['telefono']))
        def edit(new=False):
            selected = tree.selection()
            if not new and not selected:
                messagebox.showwarning('Selección', 'Seleccione un pasajero.'); return
            old_dni = '' if new else tree.item(selected[0])['values'][0]
            current = next((x for x in records('pasajeros') if str(x['dni']) == str(old_dni)), {})
            fields = {}
            for key in ('dni','nombres','apellidos','telefono'):
                val = simpledialog.askstring('Nuevo pasajero' if new else 'Editar pasajero', key.capitalize(), initialvalue=current.get(key,''), parent=self)
                if val is None: return
                if not val.strip(): messagebox.showerror('Error', 'Todos los campos son obligatorios.'); return
                fields[key] = val.strip()
            people = records('pasajeros')
            if any(x['dni'] == fields['dni'] and x['dni'] != str(old_dni) for x in people):
                messagebox.showerror('Error', 'El DNI ya existe.'); return
            if new: people.append(fields)
            else:
                for i,x in enumerate(people):
                    if str(x['dni']) == str(old_dni): people[i] = fields; break
            replace('pasajeros',people); redraw()
        def delete():
            if not tree.selection(): return
            dni = str(tree.item(tree.selection()[0])['values'][0])
            if any(v['dni']==dni for v in records('ventas')):
                messagebox.showerror('Error','No se puede eliminar un pasajero con ventas registradas.'); return
            if messagebox.askyesno('Confirmar','¿Eliminar pasajero?'):
                replace('pasajeros',[x for x in records('pasajeros') if x['dni']!=dni]); redraw()
        tk.Button(toolbar,text='+ Nuevo pasajero',command=lambda:edit(True),bg='#24a35a',fg='white').pack(side='right',padx=5)
        tk.Button(toolbar,text='Editar',command=edit,bg='#1788cf',fg='white').pack(side='right',padx=5)
        tk.Button(toolbar,text='Eliminar',command=delete).pack(side='right',padx=5)
        tk.Button(toolbar,text='Buscar',command=redraw).pack(side='left',padx=5)
        tree = self.table(p,('DNI','Nombres','Apellidos','Teléfono'),[(x['dni'],x['nombres'],x['apellidos'],x['telefono']) for x in data])

    def buses(self):
        p=self.page('GESTIÓN DE BUSES')
        def create():
            vals=[]
            for name in ('Placa','Número de unidad','Capacidad'):
                value=simpledialog.askstring('Nuevo bus',name,parent=self)
                if not value: return
                vals.append(value.strip())
            try:
                capacity=int(vals[2]); assert capacity>0
            except (ValueError,AssertionError): messagebox.showerror('Error','Capacidad inválida'); return
            if any(x['unidad']==vals[1] for x in records('buses')):
                messagebox.showerror('Error','Unidad duplicada'); return
            add('buses',{'placa':vals[0],'unidad':vals[1],'capacidad':capacity}); self.buses()
        tk.Button(p,text='+ Registrar bus',command=create,bg=TEAL,fg='white').pack(anchor='e')
        self.table(p,('Placa','Unidad','Capacidad'),[(x['placa'],x['unidad'],x['capacidad']) for x in records('buses')])

    def routes(self):
        p=self.page('RUTAS Y HORARIOS')
        def create():
            vals=[]
            for name in ('Origen','Destino','Hora de salida (HH:MM)','Unidad de bus','Precio S/'):
                v=simpledialog.askstring('Nueva ruta',name,parent=self)
                if not v: return
                vals.append(v.strip())
            if not any(x['unidad']==vals[3] for x in records('buses')):
                messagebox.showerror('Error','El bus no existe'); return
            try:
                datetime.strptime(vals[2],'%H:%M'); price=float(vals[4]); assert price>0
            except (ValueError,AssertionError): messagebox.showerror('Error','Hora o precio inválido'); return
            add('rutas',dict(zip(('origen','destino','hora','bus','precio'),(vals[0],vals[1],vals[2],vals[3],price))))
            self.routes()
        tk.Button(p,text='+ Nueva ruta',command=create,bg=TEAL,fg='white').pack(anchor='e')
        self.table(p,('Origen','Destino','Salida','Bus','Precio S/'),[(x['origen'],x['destino'],x['hora'],x['bus'],x['precio']) for x in records('rutas')])

    def sales(self):
        p=self.page('VENTA DE PASAJES')
        routes=records('rutas')
        tk.Label(p,text='DNI del pasajero',bg='white').pack(anchor='w')
        dni=tk.Entry(p); dni.pack(fill='x',pady=5)
        tk.Label(p,text='Seleccione ruta',bg='white').pack(anchor='w')
        choices=[f"{r['origen']} → {r['destino']} | {r['hora']} | Bus {r['bus']} | S/ {r['precio']}" for r in routes]
        route=ttk.Combobox(p,values=choices,state='readonly'); route.pack(fill='x',pady=5)
        if choices: route.current(0)
        tk.Label(p,text='Número de asiento',bg='white').pack(anchor='w')
        seat=tk.Entry(p); seat.pack(fill='x',pady=5)
        def purchase():
            try:
                sale=sell(dni.get().strip(),route.current(),int(seat.get()))
                messagebox.showinfo('Venta realizada',f"Pasaje registrado: S/ {sale['precio']:.2f}")
                self.sales()
            except (ValueError,IndexError) as exc: messagebox.showerror('Error',str(exc))
        tk.Button(p,text='Registrar venta',command=purchase,bg='#24a35a',fg='white',padx=15,pady=10).pack(pady=15)
        self.table(p,('DNI','Ruta','Bus','Asiento','Precio'),[(x['dni'],x['ruta'],x['bus'],x['asiento'],x['precio']) for x in records('ventas')])

    def map_seats(self):
        p=self.page('MAPA DE ASIENTOS')
        buses=records('buses')
        selection=ttk.Combobox(p,values=[b['unidad'] for b in buses],state='readonly')
        selection.pack(anchor='w')
        area=tk.Frame(p,bg='white'); area.pack(pady=15)
        def render(event=None):
            for widget in area.winfo_children():widget.destroy()
            if not selection.get(): return
            for num,status in seats(selection.get()):
                color='#ef5555' if status=='Ocupado' else '#1db66b'
                tk.Label(area,text=f'{num:02}',bg=color,fg='white',width=5,height=2,font=('Arial',10,'bold')).grid(row=(num-1)//4,column=(num-1)%4+((num-1)%4>=2),padx=5,pady=4)
            tk.Label(area,text='Verde: Disponible     Rojo: Ocupado',bg='white').grid(row=12,column=0,columnspan=5,pady=12)
        selection.bind('<<ComboboxSelected>>',render)
        if buses:selection.current(0);render()

    def reports(self):
        p=self.page('INFORMES DE VENTAS')
        sales=records('ventas')
        tk.Label(p,text=f"Total de pasajes vendidos: {len(sales)}     |     Ingresos: S/ {sum(x['precio'] for x in sales):,.2f}",bg='white',font=('Arial',14,'bold')).pack(pady=15)
        self.table(p,('DNI','Ruta','Hora','Bus','Asiento','Importe'),[(x['dni'],x['ruta'],x['hora'],x['bus'],x['asiento'],x['precio']) for x in sales])

    def settings(self):
        p=self.page('CONFIGURACIÓN')
        tk.Label(p,text='BUS SYSTEM PRO\nEmpresa de Buses El Sol\nAlmacenamiento local en archivos JSON\nVersión académica 1.0',bg='white',font=('Arial',13),justify='left').pack(anchor='w',pady=15)

if __name__=='__main__':
    App().mainloop()
