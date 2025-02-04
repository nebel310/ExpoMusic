document.addEventListener("DOMContentLoaded", () => {
  // Элементы интерфейса
  const usernameElement = document.getElementById("username");
  const logoutButton = document.getElementById("logout-button");
  const loginButton = document.getElementById("login-button");
  const registerButton = document.getElementById("register-button");

  // ==================== Flash-сообщения ====================
  const showFlashMessage = (message, type = "success") => {
    const flashContainer = document.createElement("div");
    flashContainer.className = `flash-message ${type}`;
    flashContainer.textContent = message;
    document.body.appendChild(flashContainer);

    setTimeout(() => flashContainer.remove(), 3000);
  };

  const showSavedFlashMessage = () => {
    const flashData = localStorage.getItem("flash_message");
    if (flashData) {
      try {
        const { message, type } = JSON.parse(flashData);
        showFlashMessage(message, type);
        localStorage.removeItem("flash_message");
      } catch (e) {
        console.error("Ошибка парсинга flash-сообщения:", e);
      }
    }
  };

  // ==================== Авторизация ====================
  const checkAuth = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      const response = await fetch("http://127.0.0.1:8000/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        const newToken = await refreshAccessToken();
        if (!newToken) throw new Error("Auth failed");
        return checkAuth();
      }

      const userData = await response.json();
      
      if (usernameElement) {
        usernameElement.textContent = userData.username;
        usernameElement.style.display = "inline";
        usernameElement.addEventListener("click", () => {
          window.location.href = "pages/profile.html";
        });
      }

      [logoutButton, loginButton, registerButton].forEach(btn => {
        if (btn) btn.style.display = btn === logoutButton ? "block" : "none";
      });

    } catch (error) {
      console.error("Ошибка авторизации:", error);
      localStorage.removeItem("access_token");
      localStorage.setItem("flash_message", JSON.stringify({
        message: "Сессия истекла, войдите снова",
        type: "error"
      }));
      window.location.href = "pages/login.html";
    }
  };

  // ==================== Обработчики кнопок ====================
  const setupAuthHandlers = () => {
    // Обработчик выхода
    if (logoutButton) {
      logoutButton.addEventListener("click", async () => {
        try {
          const response = await fetch("http://127.0.0.1:8000/auth/logout", {
            method: "POST",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          });

          if (response.ok) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.setItem("flash_message", JSON.stringify({
              message: "Вы успешно вышли",
              type: "success"
            }));
            window.location.href = "pages/login.html";
          }
        } catch (error) {
          localStorage.setItem("flash_message", JSON.stringify({
            message: "Ошибка при выходе",
            type: "error"
          }));
          window.location.reload();
        }
      });
    }

    // Обработчик входа
    if (loginButton) {
      loginButton.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = "pages/login.html";
      });
    }

    // Обработчик регистрации
    if (registerButton) {
      registerButton.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = "pages/register.html";
      });
    }
  };

  // ==================== Анимации ====================
  const createVisualizer = () => {
    const visualizer = document.querySelector('.hero__visualizer');
    if (!visualizer) return;

    const colors = ['#1DB954', '#FF0000', '#FFFFFF', '#1ED760'];
    let animationInterval;

    const createWave = () => {
      if (Math.random() > 0.5) {
        const wave = document.createElement('div');
        wave.className = 'visualizer-waves';
        wave.style.borderColor = colors[Math.floor(Math.random() * colors.length)];
        visualizer.appendChild(wave);
        
        setTimeout(() => wave.remove(), 3000);
      }
    };

    const startAnimation = () => {
      if (!animationInterval) {
        animationInterval = setInterval(createWave, 1000);
      }
    };

    const stopAnimation = () => {
      if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
      }
    };

    document.addEventListener('visibilitychange', () => {
      document.hidden ? stopAnimation() : startAnimation();
    });

    startAnimation();
    return stopAnimation;
  };

  const setupParallax = () => {
    if (window.innerWidth <= 768) return;

    const heroContainer = document.querySelector('.hero__container');
    if (!heroContainer) return;

    const handleMouseMove = (e) => {
      const x = (window.innerWidth / 2 - e.clientX) / 30;
      const y = (window.innerHeight / 2 - e.clientY) / 30;
      heroContainer.style.transform = `translate(${x}px, ${y}px)`;
    };

    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  };

  // ==================== Инициализация ====================
  const init = () => {
    showSavedFlashMessage();
    checkAuth();
    setupAuthHandlers();
    
    const cleanVisualizer = createVisualizer();
    const cleanParallax = setupParallax();

    window.addEventListener('beforeunload', () => {
      if (cleanVisualizer) cleanVisualizer();
      if (cleanParallax) cleanParallax();
    });
  };

  init();
});