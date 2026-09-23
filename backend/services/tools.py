def consultar_servicios():
    return [
        {
            "id": 1,
            "nombre": "Reparación de computadoras",
            "descripcion": "Diagnóstico y reparación de equipos."
        },
        {
            "id": 2,
            "nombre": "Instalación de software",
            "descripcion": "Instalación y configuración de software."
        },
        {
            "id": 3,
            "nombre": "Mantenimiento preventivo",
            "descripcion": "Limpieza y mantenimiento de equipos."
        }
    ]

def consultar_cliente(nombre: str):
    clientes = [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@email.com"
        },
        {
            "id": 2,
            "nombre": "María Gómez",
            "email": "maria@email.com"
        }
    ]

    for cliente in clientes:
        if cliente["nombre"].lower() == nombre.lower():
            return cliente

    return {
        "error": "Cliente no encontrado"
    }