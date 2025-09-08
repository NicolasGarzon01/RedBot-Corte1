function logout() {
  localStorage.removeItem('token');
  window.location.href = '/login.html'; // Redirige al login al salir
}

async function fetchAccounts() {
  const token = localStorage.getItem('token');
  if (!token) {
    document.getElementById('accounts').innerHTML = `<div style='color:red'>No estás autenticado.</div>`;
    return;
  }
  try {
    const res = await fetch('/api/accounts', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.status === 401) {
       logout(); // Si el token es inválido, cierra sesión
       return;
    }
    if (!res.ok) {
      document.getElementById('accounts').innerHTML = `<div style='color:red'>Error: ${res.status} ${res.statusText}</div>`;
      return;
    }
    const accounts = await res.json();
    const container = document.getElementById('accounts');
    if (!Array.isArray(accounts)) {
      container.innerHTML = `<div style='color:red'>Respuesta inesperada del servidor.</div>`;
      return;
    }
    container.innerHTML = accounts.map(acc => `<div>ID: ${acc.id} - ${acc.handle} (${acc.platform})</div>`).join('');
  } catch (err) {
    document.getElementById('accounts').innerHTML = `<div style='color:red'>Error de conexión con el servicio de cuentas.</div>`;
  }
}

async function fetchTasks() {
  const token = localStorage.getItem('token');
  if (!token) {
    document.getElementById('tasks').innerHTML = `<div style='color:red'>No estás autenticado.</div>`;
    return;
  }
  try {
    // Se añade la barra final para coincidir con la configuración de NGINX
    const res = await fetch('/api/tasks/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.status === 401) {
       logout(); // Si el token es inválido, cierra sesión
       return;
    }
    if (!res.ok) {
      document.getElementById('tasks').innerHTML = `<div style='color:red'>Error: ${res.status} ${res.statusText}</div>`;
      return;
    }
    const tasks = await res.json();
    const container = document.getElementById('tasks');
    if (!Array.isArray(tasks)) {
      container.innerHTML = `<div style='color:red'>Respuesta inesperada del servidor.</div>`;
      return;
    }
    container.innerHTML = tasks.map(task => `<div>${task.type} - ${task.status}</div>`).join('');
  } catch (err) {
    document.getElementById('tasks').innerHTML = `<div style='color:red'>Error de conexión con el servicio de tareas.</div>`;
  }
}

// Llama a las funciones para cargar los datos cuando la página carga
document.addEventListener('DOMContentLoaded', () => {
  fetchAccounts();
  fetchTasks();
});