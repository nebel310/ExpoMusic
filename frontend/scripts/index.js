document.addEventListener("DOMContentLoaded", () => {
  const usernameElement = document.getElementById("username");
  const logoutButton = document.getElementById("logout-button");
  const loginButton = document.getElementById("login-button");
  const registerButton = document.getElementById("register-button");

  // Функция для отображения flash-уведомлений
  const showFlashMessage = (message, type = "success") => {
    const flashContainer = document.createElement("div");
    flashContainer.className = `flash-message ${type}`;
    flashContainer.textContent = message;

    document.body.appendChild(flashContainer);

    // Автоматическое удаление уведомления через 3 секунды
    setTimeout(() => {
      flashContainer.remove();
    }, 3000);
  };

  // Функция для отображения сохраненного flash-сообщения
  const showSavedFlashMessage = () => {
    const flashData = localStorage.getItem("flash_message");
    if (flashData) {
      const { message, type } = JSON.parse(flashData);
      showFlashMessage(message, type);
      localStorage.removeItem("flash_message"); // Удаляем сообщение после отображения
    }
  };

  // Показываем сохраненное сообщение при загрузке страницы
  showSavedFlashMessage();

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