import praw
import os
import time
from datetime import datetime

# Cargar las credenciales de la app desde el entorno
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "RedBot by MyUser (v1.0)"

def get_reddit_instance(account_token: str):
    """
    Crea una instancia de PRAW y verifica que la autenticación sea exitosa.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        refresh_token=account_token,
        user_agent=REDDIT_USER_AGENT,
    )
    
    # ▼▼▼ AÑADIMOS ESTA VERIFICACIÓN CRUCIAL ▼▼▼
    # Esto fuerza a PRAW a verificar la autenticación.
    # Si el token es inválido, aquí se generará un error.
    if not reddit.user.me():
        raise Exception("Autenticación fallida. El refresh_token es inválido o ha sido revocado.")
        
    print(f"--- Autenticación exitosa como el usuario: {reddit.user.me().name} ---")
    return reddit

### --- Lógica de Tareas --- ###

def execute_reply_task(reddit: praw.Reddit, config: dict):
    """Lógica para la tarea de "responder comentarios"."""
    print(f"--- Ejecutando tarea de respuesta para el post: {config.get('post_url')} ---")
    post_url = config.get("post_url")
    keywords = config.get("keywords", [])
    reply_text = config.get("reply_text")

    if not all([post_url, keywords, reply_text]):
        raise ValueError("Configuración inválida para la tarea de respuesta.")

    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)
    
    for comment in submission.comments.list():
        if comment.author and comment.author.name == reddit.user.me().name:
            continue
        if any(keyword.lower() in comment.body.lower() for keyword in keywords):
            print(f"Palabra clave encontrada en el comentario de '{comment.author}'. Respondiendo...")
            comment.reply(reply_text)
            print("Respuesta enviada.")
    
    print("--- Tarea de respuesta finalizada ---")

def execute_schedule_post_task(reddit: praw.Reddit, config: dict):
    """Lógica para la tarea de "publicaciones programadas"."""
    print(f"--- Ejecutando tarea de publicación programada ---")
    subreddit_name = config.get("subreddit")
    title = config.get("title")
    text = config.get("text")
    
    # Esta es una implementación simple: la tarea se ejecutará la próxima vez que el worker la revise.
    # Una implementación avanzada usaría la fecha/hora del JSON.
    if not all([subreddit_name, title, text]):
        raise ValueError("Configuración inválida para la tarea de publicación programada.")

    subreddit = reddit.subreddit(subreddit_name)
    print(f"Publicando en r/{subreddit_name} con el título '{title}'...")
    subreddit.submit(title=title, selftext=text)
    print("--- Publicación enviada exitosamente ---")

def execute_moderate_comments_task(reddit: praw.Reddit, config: dict):
    """Lógica para la tarea de "moderar comentarios" con verificación de permisos."""
    print("--- Iniciando tarea de moderación ---")

    authenticated_user = reddit.user.me()
    if not authenticated_user:
        raise Exception("Fallo de autenticación DENTRO de la tarea de moderación.")
    print(f"Confirmado: Ejecutando como el usuario '{authenticated_user.name}'.")

    post_url = config.get("post_url")
    action = config.get("action")
    forbidden_words = config.get("forbidden_words", [])

    if not all([post_url, action, forbidden_words]):
        raise ValueError("Configuración inválida para la tarea de moderación.")

    submission = reddit.submission(url=post_url)
    subreddit = submission.subreddit

    # ▼▼▼ VERIFICACIÓN DE PERMISOS DE MODERADOR ▼▼▼
    try:
        print(f"Verificando si '{authenticated_user.name}' es moderador en 'r/{subreddit.display_name}'...")
        moderators = [str(mod) for mod in subreddit.moderator()]
        if authenticated_user.name in moderators:
            print(f"✅ ÉXITO: El usuario SÍ es moderador.")
        else:
            print(f"❌ FALLO: El usuario NO es moderador de este subreddit. Lista de moderadores: {moderators}")
            # Si no es moderador, no tiene sentido continuar.
            print("--- Tarea de moderación finalizada (sin permisos) ---")
            return 
    except Exception as e:
        print(f"ERROR al intentar verificar los permisos de moderador: {e}")
        # Si hay un error aquí, probablemente el token no tiene el scope 'modconfig'.
        print("--- Tarea de moderación finalizada (error de permisos) ---")
        return

    print(f"Revisando post: {post_url}")
    print(f"Buscando palabras prohibidas: {forbidden_words}")
    
    submission.comments.replace_more(limit=0)
    
    for comment in submission.comments.list():
        if any(word.lower() in comment.body.lower() for word in forbidden_words):
            print(f"¡PALABRA PROHIBIDA ENCONTRADA! En el comentario de '{comment.author}'.")
            if action == "remove":
                print("Intentando ejecutar comment.delete()...")
                comment.delete()
                print("¡ACCIÓN DE BORRADO EJECUTADA!")
            
    print("--- Tarea de moderación finalizada ---")

### --- Procesador Principal de Tareas --- ###

def process_task(db_session, task, account):
    """
    Función principal que decide qué lógica de bot ejecutar según el tipo de tarea.
    """
    reddit = get_reddit_instance(account.token)

    # ▼▼▼ CORRECCIÓN FINAL AQUÍ ▼▼▼
    # Usamos los nombres cortos y en minúsculas para que coincidan con la base de datos
    if task.type == "responder":
        execute_reply_task(reddit, task.config_json)
    elif task.type == "publicar":
        execute_schedule_post_task(reddit, task.config_json)
    elif task.type == "moderar":
        execute_moderate_comments_task(reddit, task.config_json)
    else:
        raise NotImplementedError(f"El tipo de tarea '{task.type}' no está implementado.")