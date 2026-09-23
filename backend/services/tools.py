from database import SessionLocal
from models import Cliente, Servicio


def consultar_servicios():
    db = SessionLocal()

    try:
        servicios = db.query(Servicio).all()

        return [
            {
                "id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion
            }
            for servicio in servicios
        ]

    finally:
        db.close()


def consultar_cliente(nombre: str):
    db = SessionLocal()

    try:
        cliente = (
            db.query(Cliente)
            .filter(Cliente.nombre.ilike(nombre))
            .first()
        )

        if not cliente:
            return {
                "error": "Cliente no encontrado"
            }

        return {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email
        }

    finally:
        db.close()