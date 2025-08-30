class Utils {
    static showMessage(elementId, message, isError = false) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.textContent = message;
        element.className = isError ? 'error' : 'success';
        
        if (message) {
            setTimeout(() => {
                element.textContent = '';
            }, 5000);
        }
    }

    static switchAuthForms() {
        const loginForm = document.querySelector('.auth-form:not(.hidden)');
        const registerForm = document.getElementById('register-form');
        
        if (loginForm && registerForm) {
            loginForm.classList.add('hidden');
            registerForm.classList.toggle('hidden');
        }
    }

    static debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}