document.addEventListener("DOMContentLoaded", () => {
  const usernameElement = document.getElementById("username");
  const logoutButton = document.getElementById("logout-button");
  const loginButton = document.getElementById("login-button");
  const registerButton = document.getElementById("register-button");

  const token = localStorage.getItem("access_token");
  if (token) {
    fetch("http://127.0.0.1:8000/auth/me", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Не удалось получить данные пользователя");
        }
      })
      .then((userData) => {
        usernameElement.textContent = userData.username;
        usernameElement.style.display = "inline";
        logoutButton.style.display = "block";
        loginButton.style.display = "none";
        registerButton.style.display = "none";

        // Добавляем обработчик клика на имя пользователя
        usernameElement.addEventListener("click", () => {
          window.location.href = "pages/profile.html";
        });
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        localStorage.removeItem("access_token");
      });
  }

  // Обработка выхода
  logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    window.location.href = "/frontend/index.html";
  });

  // Обработка клика на кнопку "Войти"
  loginButton.addEventListener("click", () => {
    window.location.href = "pages/login.html";
  });

  // Обработка клика на кнопку "Зарегистрироваться"
  registerButton.addEventListener("click", () => {
    window.location.href = "pages/register.html";
  });
});