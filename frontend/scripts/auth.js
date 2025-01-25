document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  // Функция для отображения ошибок
  const showError = (message) => {
    alert(message); // Можно заменить на более красивый вывод ошибок
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
        password_confirm: formData.get("password_confirm"), // Добавляем подтверждение пароля
      };

      // Проверка совпадения паролей
      if (data.password !== data.password_confirm) {
        showError("Пароли не совпадают");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          window.location.href = "login.html"; // Перенаправляем на страницу входа после успешной регистрации
        } else {
          const errorData = await response.json();
          console.error("Ошибка регистрации:", errorData); // Логируем ошибку
          showError(errorData.message || "Ошибка регистрации");
        }
      } catch (error) {
        console.error("Ошибка:", error); // Логируем ошибку
        showError("Произошла ошибка при регистрации");
      }
    });
  }

  // Обработка входа
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const data = {
        email: formData.get("email"), // Убедись, что name="email" в поле ввода
        password: formData.get("password"), // Убедись, что name="password" в поле ввода
      };

      try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          const result = await response.json();
          localStorage.setItem("access_token", result.access_token); // Сохраняем токен
          window.location.href = "/frontend/index.html"; // Перенаправляем на главную страницу
        } else {
          const errorData = await response.json();
          console.error("Ошибка входа:", errorData); // Логируем ошибку
          showError(errorData.detail || "Ошибка входа");
        }
      } catch (error) {
        console.error("Ошибка:", error); // Логируем ошибку
        showError("Произошла ошибка при входе");
      }
    });
  }

  // Проверка авторизации при загрузке страницы
  const checkAuth = async () => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const response = await fetch("http://127.0.0.1:8000/auth/me", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          console.log("Пользователь авторизован:", userData);
          // Можно обновить интерфейс, например, показать имя пользователя
        } else {
          console.error("Ошибка при проверке авторизации:", response.status); // Логируем ошибку
          localStorage.removeItem("access_token"); // Удаляем токен, если он недействителен
        }
      } catch (error) {
        console.error("Ошибка при проверке авторизации:", error); // Логируем ошибку
        localStorage.removeItem("access_token");
      }
    }
  };

  // Проверяем авторизацию при загрузке страницы
  checkAuth();
});