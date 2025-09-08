document.getElementById('addTaskForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const type = document.getElementById('taskType').value;
  const accountId = document.getElementById('accountId').value;
  let config;
  try {
    config = JSON.parse(document.getElementById('config').value);
  } catch {
    document.getElementById('addTaskError').textContent = 'Configuración JSON inválida';
    return;
  }
  const userToken = localStorage.getItem('token');
  try {
  const res = await fetch('/api/tasks/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken}`
      },
      body: JSON.stringify({ type, account_id: accountId, config_json: config })
    });
    if (res.ok) {
      window.location.href = 'main.html';
    } else {
      document.getElementById('addTaskError').textContent = 'Error al agregar la tarea';
    }
  } catch (err) {
    document.getElementById('addTaskError').textContent = 'Error de conexión';
  }
});
