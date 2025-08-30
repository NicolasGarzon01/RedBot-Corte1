# Importa todos los modelos de todos los servicios para registrar las tablas en el Base centralizado
from account_service.app.models import Account
from task_service.app.models import Task
from user_service.app.models import User as UserServiceUser
from auth_service.app.auth.models import User as AuthServiceUser
from executor_service.app.models import ExecutionLog
