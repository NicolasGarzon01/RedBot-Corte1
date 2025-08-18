from app.database import SessionLocal
from app.auth.models import User  # Ajusta la ruta según tu estructura real
from app.auth.utils import hash_password  # Ajusta también

db = SessionLocal()

# Datos del administrador
admin_username = "admin"
admin_password = "admin123"

# Verificar si ya existe
existing_user = db.query(User).filter_by(username=admin_username).first()
if not existing_user:
    hashed_password = hash_password(admin_password)
    admin_user = User(
        username=admin_username,
        password_hash=hashed_password,
        role="admin"  
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Administrador creado con éxito:", admin_user.username)
else:
    print("El usuario admin ya existe")
