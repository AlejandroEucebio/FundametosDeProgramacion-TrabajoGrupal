# BUS SYSTEM PRO

Prototipo académico de gestión de transporte terrestre desarrollado en Python con Tkinter y archivos JSON. Inspirado en las pantallas de referencia proporcionadas.

## Requisitos
- Python 3.10 o superior
- Tkinter (incluido normalmente con Python en Windows)

## Ejecución
```bash
python main.py
```

## Módulos
- `main.py`: interfaz gráfica, eventos, controles y navegación.
- `services.py`: operaciones de negocio, pasajeros, rutas, buses, venta y asientos.
- `storage.py`: persistencia de datos en JSON.
- `data/`: se crea automáticamente al ejecutar.

## Funciones implementadas
Registro, búsqueda, edición y eliminación de pasajeros; registro de buses y rutas; venta de pasajes; validación de asientos; mapa visual; tablero e informes. Los datos persisten entre ejecuciones.

**Nota:** Prototipo local académico, sin autenticación real, pagos bancarios ni soporte multiusuario. La ocupación se controla por unidad de bus y no por fecha de viaje; para producción se requeriría modelar salidas individuales.

## Git y GitHub: historial progresivo real
Realiza estos commits durante el desarrollo, incorporando los archivos en cada etapa (no inventes fechas ni commits). Puedes empezar con el proyecto completo y un commit inicial honesto, y continuar registrando mejoras posteriores.

```bash
git init
git add storage.py
git commit -m "feat: implementar persistencia JSON"
git add services.py
git commit -m "feat: agregar logica de buses rutas pasajeros y ventas"
git add main.py
git commit -m "feat: construir interfaz grafica modular"
git add README.md .gitignore
git commit -m "docs: documentar instalacion y funcionamiento"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/bus-system-pro.git
git push -u origin main
```

Crea antes el repositorio vacío en GitHub y reemplaza `TU_USUARIO` por tu usuario. Los comandos de commit requieren tener Git configurado con nombre y correo.
