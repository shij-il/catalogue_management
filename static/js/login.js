document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const loginMsg = document.getElementById("login-msg");

  loginForm.addEventListener("submit", e => {
    e.preventDefault();
    loginMsg.textContent = "";
    loginMsg.className = "message";

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
      loginMsg.textContent = "Username and password are required.";
      loginMsg.className = "message error show";
      return;
    }

    fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
      if (ok) {
        loginMsg.textContent = "Login successful! Redirecting...";
        loginMsg.className = "message success show";
        setTimeout(() => window.location.href = "/", 1000);
      } else {
        loginMsg.textContent = data.error || "Login failed.";
        loginMsg.className = "message error show";
      }
    })
    .catch(() => {
      loginMsg.textContent = "Login request failed.";
      loginMsg.className = "message error show";
    });
  });
});
