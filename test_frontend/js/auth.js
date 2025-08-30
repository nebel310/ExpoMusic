class AuthService {
    static async register() {
        const payload = {
            username: document.getElementById('reg-username').value.trim(),
            email: document.getElementById('reg-email').value.trim(),
            password: document.getElementById('reg-password').value,
            password_confirm: document.getElementById('reg-password-confirm').value
        };

        try {
            await HttpService.request('/auth/register', 'POST', payload, false);
            Utils.showMessage('register-message', 'Регистрация успешна! Проверьте email для подтверждения');
            Utils.switchAuthForms();
        } catch (e) {
            Utils.showMessage('register-message', `Ошибка: ${e.message}`, true);
        }
    }

    static async login() {
        const payload = {
            email: document.getElementById('login-email').value.trim(),
            password: document.getElementById('login-password').value
        };

        try {
            const data = await HttpService.request('/auth/login', 'POST', payload, false);
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            window.location.href = 'dashboard.html';
        } catch (e) {
            Utils.showMessage('login-message', `Ошибка: ${e.message}`, true);
        }
    }

    static async logout() {
        try {
            await HttpService.request('/auth/logout', 'POST');
            this.clearAuthData();
            window.location.href = '/index.html';
        } catch (e) {
            console.error('Logout error:', e);
        }
    }

    static async refreshToken() {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) return false;

        try {
            const data = await HttpService.request(
                '/auth/refresh',
                'POST',
                { token: refreshToken },
                false
            );
            localStorage.setItem('accessToken', data.access_token);
            return true;
        } catch (e) {
            this.clearAuthData();
            return false;
        }
    }

    static async getCurrentUser() {
        try {
            return await HttpService.request('/auth/me');
        } catch (e) {
            if (e.message.includes('401')) {
                const refreshed = await this.refreshToken();
                if (refreshed) return this.getCurrentUser();
            }
            throw e;
        }
    }

    static clearAuthData() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    static async checkAuth() {
        const token = localStorage.getItem('accessToken');
        if (!token) return false;

        try {
            await this.getCurrentUser();
            return true;
        } catch (e) {
            return false;
        }
    }
}

// Инициализация событий
document.addEventListener('DOMContentLoaded', async () => {
    if (document.getElementById('login-btn')) {
        document.getElementById('login-btn').addEventListener('click', AuthService.login);
        document.getElementById('register-btn').addEventListener('click', AuthService.register);
        document.getElementById('show-register').addEventListener('click', Utils.switchAuthForms);
        document.getElementById('show-login').addEventListener('click', Utils.switchAuthForms);
    }

    if (document.getElementById('logout-btn')) {
        document.getElementById('logout-btn').addEventListener('click', AuthService.logout);
        
        // Загружаем данные пользователя
        try {
            const user = await AuthService.getCurrentUser();
            if (user && document.getElementById('username')) {
                document.getElementById('username').textContent = user.username;
            }
        } catch (e) {
            console.error('Failed to load user:', e);
        }
    }

    // Проверка аутентификации для защищенных страниц
    const protectedPages = ['dashboard.html', 'tracks.html', 'genres.html', 'playlists.html', 'library.html'];
    if (protectedPages.some(page => window.location.pathname.includes(page))) {
        const isAuthenticated = await AuthService.checkAuth();
        if (!isAuthenticated) {
            window.location.href = '/index.html';
        }
    }
});