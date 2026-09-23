from database import SessionLocal
from models import Cliente, Servicio


db = SessionLocal()

try:
    # Clientes
    clientes = [
        {
            "nombre": "Juan Pérez",
            "email": "juan@email.com"
        },
        {
            "nombre": "María Gómez",
            "email": "maria@email.com"
        }
    ]

    for datos in clientes:
        cliente_existente = (
            db.query(Cliente)
            .filter(Cliente.email == datos["email"])
            .first()
        )

        if not cliente_existente:
            db.add(
                Cliente(
                    nombre=datos["nombre"],
                    email=datos["email"]
                )
            )

    # Servicios
    servicios = [
        {
            "nombre": "Reparación de computadoras",
            "descripcion": "Diagnóstico y reparación de equipos."
        },
        {
            "nombre": "Instalación de software",
            "descripcion": "Instalación y configuración de software."
        },
        {
            "nombre": "Mantenimiento preventivo",
            "descripcion": "Limpieza y mantenimiento de equipos."
        }
    ]

    for datos in servicios:
        servicio_existente = (
            db.query(Servicio)
            .filter(Servicio.nombre == datos["nombre"])
            .first()
        )

        if not servicio_existente:
            db.add(
                Servicio(
                    nombre=datos["nombre"],
                    descripcion=datos["descripcion"]
                )
            )

    db.commit()

    print("Datos cargados correctamente")

except Exception:
    db.rollback()
    raise

finally:
    db.close()