class HttpService {
    static async request(endpoint, method = 'GET', body = null, requiresAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = localStorage.getItem('accessToken');
        if (requiresAuth && token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers,
            credentials: 'include'
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`http://127.0.0.1:3001${endpoint}`, config);
            
            if (response.status === 401 && requiresAuth) {
                const refreshed = await AuthService.refreshToken();
                if (refreshed) {
                    return this.request(endpoint, method, body, requiresAuth);
                }
                throw new Error('Требуется авторизация');
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || error.message || 'Ошибка запроса');
            }

            return response.headers.get('Content-Type')?.includes('application/json') 
                ? await response.json() 
                : null;
        } catch (error) {
            console.error(`API Error [${method} ${endpoint}]:`, error);
            throw error;
        }
    }
}