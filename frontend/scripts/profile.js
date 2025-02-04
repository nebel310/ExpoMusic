document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "../index.html";
    return;
  }

  // Функция для сохранения flash-сообщений
  const saveFlashMessage = (message, type = "success") => {
    localStorage.setItem("flash_message", JSON.stringify({ message, type }));
  };

  // Функция для отображения flash-уведомлений
  const showFlashMessage = (message, type = "success") => {
    const flashContainer = document.createElement("div");
    flashContainer.className = `flash-message ${type}`;
    flashContainer.textContent = message;
    document.body.appendChild(flashContainer);

    setTimeout(() => flashContainer.remove(), 3000);
  };

  // Показываем сохраненное сообщение
  const flashData = localStorage.getItem("flash_message");
  if (flashData) {
    try {
      const { message, type } = JSON.parse(flashData);
      showFlashMessage(message, type);
      localStorage.removeItem("flash_message");
    } catch (e) {
      console.error("Ошибка парсинга сообщения:", e);
    }
  }

  // Функция для выхода
  const logout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/logout", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      if (response.ok) {
        saveFlashMessage("Выход выполнен успешно!", "success");
      } else {
        saveFlashMessage("Ошибка сервера при выходе", "error");
      }
    } catch (error) {
      saveFlashMessage("Ошибка сети", "error");
    } finally {
      window.location.href = "../index.html";
    }
  };

  // Обработчик кнопки выхода
  const logoutButton = document.getElementById("logout-button");
  if (logoutButton) {
    logoutButton.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  }

  // Загрузка данных пользователя
  fetch("http://127.0.0.1:8000/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then(response => {
      if (!response.ok) throw new Error("Ошибка авторизации");
      return response.json();
    })
    .then(userData => {
      document.getElementById("profile-username").textContent = userData.username;
      document.getElementById("profile-email").textContent = userData.email;
      document.getElementById("profile-created-at").textContent = 
        new Date(userData.created_at).toLocaleDateString();
    })
    .catch(error => {
      console.error("Ошибка:", error);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "../index.html";
    });
});