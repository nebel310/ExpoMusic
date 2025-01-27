document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      window.location.href = "../index.html";
      return;
    }
  
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
        window.location.href = "../index.html";
      });
  });