document.addEventListener("DOMContentLoaded", () => {
  let token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "../index.html";
    return;
  }

  // Функция для обновления токена (без автоматического логаута)
  const refreshAccessToken = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) return null;
  
      // Исправленный запрос
      const response = await fetch("http://127.0.0.1:8000/auth/refresh", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `refresh_token=${encodeURIComponent(refreshToken)}`
      });
  
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        return data.access_token;
      }
      return null;
    } catch (error) {
      console.error("Ошибка обновления токена:", error);
      return null;
    }
  };

  // Модифицированная функция загрузки данных
  const loadUserData = async () => {
    try {
      let response = await fetch("http://127.0.0.1:8000/auth/me", {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.status === 401) {
        const newToken = await refreshAccessToken();
        if (newToken) {
          token = newToken;
          response = await fetch("http://127.0.0.1:8000/auth/me", {
            headers: { Authorization: `Bearer ${newToken}` }
          });
        } else {
          // Перенаправляем на вход без логаута
          localStorage.setItem("flash_message", JSON.stringify({
            message: "Требуется повторная авторизация",
            type: "error"
          }));
          window.location.href = "../pages/login.html";
          return;
        }
      }

      if (!response.ok) throw new Error("Ошибка загрузки данных");

      const userData = await response.json();
      document.getElementById("profile-username").textContent = userData.username;
      document.getElementById("profile-email").textContent = userData.email;
      document.getElementById("profile-created-at").textContent = 
        new Date(userData.created_at).toLocaleDateString();

    } catch (error) {
      console.error("Ошибка:", error);
      // Не вызываем logout, только показываем ошибку
      showFlashMessage("Ошибка загрузки данных профиля", "error");
    }
  };

  // Функция выхода ТОЛЬКО при явном клике
  const logout = async () => {
    try {
      await fetch("http://127.0.0.1:8000/auth/logout", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch (error) {
      console.error("Ошибка при выходе:", error);
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "../index.html";
    }
  };

  // Инициализация
  loadUserData();
  
  // Обработчики событий
  document.getElementById("logout-button")?.addEventListener("click", (e) => {
    e.preventDefault();
    logout();
  });

  document.querySelector('.save-button')?.addEventListener('click', () => {
    const flashContainer = document.createElement('div');
    flashContainer.className = 'flash-message info';
    flashContainer.textContent = 'Изменение данных временно недоступно';
    document.body.appendChild(flashContainer);
    
    setTimeout(() => flashContainer.remove(), 3000);
  });
});