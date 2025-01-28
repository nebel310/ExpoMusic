document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "../index.html";
    return;
  }

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

  // Функция для выхода из системы
  const logout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/logout", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        saveFlashMessage("Выход выполнен успешно!");
        window.location.href = "../index.html"; // Мгновенный редирект
      } else {
        showFlashMessage("Ошибка при выходе", "error");
      }
    } catch (error) {
      console.error("Ошибка:", error);
      showFlashMessage("Произошла ошибка при выходе", "error");
    }
  };

  // Обработчик для кнопки выхода
  const logoutButton = document.getElementById("logout-button");
  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }

  // Загрузка данных пользователя
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
      document.getElementById("profile-username").textContent = userData.username;
      document.getElementById("profile-email").textContent = userData.email;
      document.getElementById("profile-created-at").textContent = new Date(
        userData.created_at
      ).toLocaleDateString();
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "../index.html";
    });
});