from app.database import Base, engine
from app.models import Usuario, Administrador, Test, Respuestas , Estadisticas , TestEstadistica
# importa los modelos que tengas

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

print("✔️ Base de datos y tablas creadas correctamente.")
