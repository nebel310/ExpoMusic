document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

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

  // Функция для сохранения flash-сообщения в localStorage
  const saveFlashMessage = (message, type = "success") => {
    localStorage.setItem("flash_message", JSON.stringify({ message, type }));
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

  // Функция для отображения ошибок
  const showError = (message) => {
    showFlashMessage(message, "error");
  };

  // Функция для сохранения токенов в localStorage
  const saveTokens = (accessToken, refreshToken) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
  };

  // Функция для удаления токенов из localStorage
  const removeTokens = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  // Функция для обновления access_token
  const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) return null;
  
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken })
      });
  
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        return data.access_token;
      }
    } catch (error) {
      console.error("Ошибка обновления токена:", error);
    }
    return null;
  };

  // Функция для выполнения запросов с автоматическим обновлением токена
  const fetchWithAuth = async (url, options = {}) => {
    let accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      window.location.href = "/frontend/pages/login.html";
      return;
    }

    // Добавляем токен в заголовки
    options.headers = {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    };

    let response = await fetch(url, options);

    // Если токен истек, пытаемся обновить его
    if (response.status === 401) {
      const newAccessToken = await refreshAccessToken();
      if (newAccessToken) {
        options.headers.Authorization = `Bearer ${newAccessToken}`;
        response = await fetch(url, options);
      }
    }

    return response;
  };

  // Обработка регистрации
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);
      const data = {
        username: formData.get("username"),
        email: formData.get("email"),
        password: formData.get("password"),
        password_confirm: formData.get("password_confirm"),
        is_confirmed: false
      };
    
      if (data.password !== data.password_confirm) {
        showError("Пароли не совпадают");
        return;
      }
    
      try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
    
        const responseData = await response.json();
        
        if (response.ok) {
          localStorage.setItem("flash_message", JSON.stringify({
            message: responseData.message,
            type: "success"
          }));
          window.location.href = "login.html";
        } else {
          showError(responseData.detail || "Ошибка регистрации");
        }
      } catch (error) {
        showError("Ошибка сети");
      }
    });
  }

  // Обработка входа
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const data = {
        email: formData.get("email"),
        password: formData.get("password")
      };
    
      try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
    
        const responseData = await response.json();
        
        if (response.ok) {
          localStorage.setItem("access_token", responseData.access_token);
          localStorage.setItem("refresh_token", responseData.refresh_token);
          localStorage.setItem("flash_message", JSON.stringify({
            message: responseData.message,
            type: "success"
          }));
          window.location.href = "../index.html";
        } else {
          showError(responseData.detail || "Ошибка входа");
        }
      } catch (error) {
        showError("Ошибка сети");
      }
    });
  }

  // Обработка выхода
  const logout = async () => {
    try {
      const response = await fetchWithAuth("http://127.0.0.1:8000/auth/logout", {
        method: "POST",
      });

      if (response.ok) {
        removeTokens();
        saveFlashMessage("Выход выполнен успешно!");
        window.location.href = "/frontend/index.html"; // Мгновенный редирект
      } else {
        showError("Ошибка при выходе");
      }
    } catch (error) {
      console.error("Ошибка:", error);
      showError("Произошла ошибка при выходе");
    }
  };

  // Проверка авторизации при загрузке страницы
  const checkAuth = async () => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const response = await fetchWithAuth("http://127.0.0.1:8000/auth/me");
        if (response.ok) {
          const userData = await response.json();
          console.log("Пользователь авторизован:", userData);
          // Можно обновить интерфейс, например, показать имя пользователя
        } else {
          console.error("Ошибка при проверке авторизации:", response.status);
          removeTokens();
        }
      } catch (error) {
        console.error("Ошибка при проверке авторизации:", error);
        removeTokens();
      }
    }
  };

  // Проверяем авторизацию при загрузке страницы
  checkAuth();

  // Обработка выхода
  const logoutButton = document.getElementById("logout-button");
  if (logoutButton) {
    logoutButton.addEventListener("click", logout);
  }
});