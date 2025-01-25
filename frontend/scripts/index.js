document.addEventListener("DOMContentLoaded", () => {
    const usernameElement = document.getElementById("username");
    const logoutButton = document.getElementById("logout-button");
  
    const token = localStorage.getItem("access_token");
    if (token) {
      fetch("/auth/me", {
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
          logoutButton.style.display = "block";
        })
        .catch((error) => {
          console.error("Ошибка:", error);
          localStorage.removeItem("access_token");
        });
    }
  
    // Обработка выхода
    logoutButton.addEventListener("click", () => {
      localStorage.removeItem("access_token");
      window.location.href = "/";
    });
  });