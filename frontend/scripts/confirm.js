document.addEventListener("DOMContentLoaded", async () => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const email = params.get('email');
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/auth/confirm/token=${token}/email=${email}`);
      
      let message, type;
      if (response.ok) {
        message = "Email успешно подтверждён!";
        type = "success";
      } else {
        const errorData = await response.json();
        message = errorData.detail || "Ошибка подтверждения";
        type = "error";
      }
      
      localStorage.setItem("flash_message", JSON.stringify({message, type}));
    } catch (error) {
      localStorage.setItem("flash_message", JSON.stringify({
        message: "Ошибка сети",
        type: "error"
      }));
    }
    
    window.location.href = "login.html";
  });