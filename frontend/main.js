let token = null;

// Tabs logic
const tabLogin = document.getElementById("tabLogin");
const tabRegister = document.getElementById("tabRegister");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

function showTab(tab) {
  if (tab === "login") {
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    loginForm.style.display = "flex";
    registerForm.style.display = "none";
  } else {
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    registerForm.style.display = "flex";
    loginForm.style.display = "none";
  }
}

tabLogin.addEventListener("click", () => showTab("login"));
tabRegister.addEventListener("click", () => showTab("register"));

// Inicializa en login
showTab("login");

// Registro
registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("regUsername").value;
  const password = document.getElementById("regPassword").value;

  const response = await fetch("http://localhost:8000/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();
  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
});

// Login

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;

  const response = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (response.ok) {
    const data = await response.json();
    token = data.access_token;
    document.getElementById("output").textContent = "Login exitoso. Token guardado:\n" + token;

    // Mostrar ventana emergente con el token y botón para copiar
    mostrarTokenModal(token);
  } else {
    document.getElementById("output").textContent = "Error en login";
  }
});

// Función para mostrar el modal del token
function mostrarTokenModal(token) {
  const overlay = document.createElement("div");
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100vw";
  overlay.style.height = "100vh";
  overlay.style.background = "rgba(0,0,0,0.4)";
  overlay.style.display = "flex";
  overlay.style.justifyContent = "center";
  overlay.style.alignItems = "center";
  overlay.style.zIndex = "9999";

  // Crear ventana modal
  const modal = document.createElement("div");
  modal.style.background = "#fff";
  modal.style.padding = "2rem";
  modal.style.borderRadius = "10px";
  modal.style.boxShadow = "0 2px 16px rgba(0,0,0,0.18)";
  modal.style.textAlign = "center";
  modal.style.maxWidth = "400px";

  const title = document.createElement("h2");
  title.textContent = "Token de acceso";
  modal.appendChild(title);

  const tokenText = document.createElement("textarea");
  tokenText.value = token;
  tokenText.readOnly = true;
  tokenText.style.width = "100%";
  tokenText.style.height = "60px";
  tokenText.style.marginBottom = "1rem";
  modal.appendChild(tokenText);

  const copyBtn = document.createElement("button");
  copyBtn.textContent = "Copiar token";
  copyBtn.style.marginRight = "1rem";
  copyBtn.onclick = () => {
    tokenText.select();
    document.execCommand("copy");
    copyBtn.textContent = "¡Copiado!";
    setTimeout(() => { copyBtn.textContent = "Copiar token"; }, 1500);
  };
  modal.appendChild(copyBtn);

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "Cerrar";
  closeBtn.onclick = () => {
    document.body.removeChild(overlay);
  };
  modal.appendChild(closeBtn);

  overlay.appendChild(modal);
  document.body.appendChild(overlay);
}


