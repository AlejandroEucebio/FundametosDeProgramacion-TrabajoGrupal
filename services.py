from storage import load, save

DEFAULT_BUSES = [{'placa':'ABC-123','unidad':'45B','capacidad':40}, {'placa':'DEF-456','unidad':'458','capacidad':32}]
DEFAULT_ROUTES = [{'origen':'Lima','destino':'Ica','hora':'10:00','bus':'45B','precio':45.0}, {'origen':'Lima','destino':'Huacho','hora':'13:00','bus':'458','precio':30.0}]

def records(kind):
    defaults = {'buses': DEFAULT_BUSES, 'rutas': DEFAULT_ROUTES, 'pasajeros': [], 'ventas': []}
    return load(kind, defaults[kind])


def add(kind, item):
    items = records(kind)

    if kind == 'pasajeros':
        dni = str(item.get('dni', '')).strip()

        if not dni.isdigit() or len(dni) != 8:
            raise ValueError('El DNI debe contener 8 dígitos.')

        if any(str(p['dni']) == dni for p in items):
            raise ValueError('El pasajero ya está registrado.')

        item['dni'] = dni

    items.append(item)
    save(kind, items)


def replace(kind, items):
    save(kind, items)

def seats(bus):
    capacity = next((int(b['capacidad']) for b in records('buses') if b['unidad'] == bus), 40)
    occupied = {int(v['asiento']) for v in records('ventas') if v['bus'] == bus}
    return [(i, 'Ocupado' if i in occupied else 'Disponible') for i in range(1, capacity + 1)]

def sell(dni, route_index, seat):
    passengers = records('pasajeros')
    if not any(p['dni'] == dni for p in passengers):
        raise ValueError('Primero registre al pasajero.')
    routes = records('rutas')
    if not 0 <= route_index < len(routes):
        raise ValueError('Ruta no válida.')
    route = routes[route_index]
    if (seat, 'Disponible') not in seats(route['bus']):
        raise ValueError('Asiento ocupado o fuera de rango.')
    sale = {'dni':dni, 'ruta':f"{route['origen']} - {route['destino']}", 'hora':route['hora'], 'bus':route['bus'], 'asiento':seat, 'precio':float(route['precio'])}
    add('ventas', sale)
    return sale
