document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
  
    if (registerForm) {
      registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());
  
        try {
          const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });
  
          if (response.ok) {
            window.location.href = "login.html";
          } else {
            alert("Ошибка регистрации");
          }
        } catch (error) {
          console.error("Ошибка:", error);
        }
      });
    }
  
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());
  
        try {
          const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });
  
          if (response.ok) {
            const result = await response.json();
            localStorage.setItem("access_token", result.access_token);
            window.location.href = "/";
          } else {
            alert("Ошибка входа");
          }
        } catch (error) {
          console.error("Ошибка:", error);
        }
      });
    }
  });