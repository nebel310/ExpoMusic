class TrackService {
    static currentPage = 1;
    static limit = 10;

    static async loadTracks(page = 1, genreId = null, search = '') {
        this.currentPage = page;
        let url = `/tracks?limit=${this.limit}&offset=${(page - 1) * this.limit}`;
        
        if (genreId) url += `&genre_id=${genreId}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;

        try {
            const tracks = await HttpService.request(url);
            this.renderTracks(tracks);
            this.updatePagination(tracks.length);
        } catch (e) {
            console.error('Failed to load tracks:', e);
        }
    }

    static async loadTrackDetails(trackId) {
        try {
            return await HttpService.request(`/tracks/${trackId}`);
        } catch (e) {
            console.error('Failed to load track details:', e);
            return null;
        }
    }

    static async uploadTrack(trackData) {
        try {
            await HttpService.request('/tracks', 'POST', trackData);
            await this.loadTracks(this.currentPage);
            return true;
        } catch (e) {
            console.error('Failed to upload track:', e);
            return false;
        }
    }

    static async deleteTrack(trackId) {
        if (!confirm('Вы уверены, что хотите удалить этот трек?')) return;

        try {
            await HttpService.request(`/tracks/${trackId}`, 'DELETE');
            await this.loadTracks(this.currentPage);
        } catch (e) {
            console.error('Failed to delete track:', e);
        }
    }

    static async getTracksByGenre(genreId, limit = 10, offset = 0) {
        try {
            return await HttpService.request(
                `/tracks/genres/${genreId}?limit=${limit}&offset=${offset}`
            );
        } catch (e) {
            console.error('Failed to load tracks by genre:', e);
            return [];
        }
    }

    static renderTracks(tracks) {
        const container = document.getElementById('track-list');
        if (!container) return;

        container.innerHTML = tracks.length > 0 
            ? tracks.map(track => this.renderTrackItem(track)).join('')
            : '<div class="empty">Треки не найдены</div>';
    }

    static renderTrackItem(track) {
        return `
            <div class="track-item" data-id="${track.id}">
                <div class="track-info">
                    <h3>${track.title}</h3>
                    <p>${track.artist}</p>
                    <span class="genre">Жанр: ${track.genre_id}</span>
                </div>
                <div class="track-actions">
                    <button class="btn-secondary" onclick="TrackService.showTrackDetails(${track.id})">
                        Подробнее
                    </button>
                    <button class="btn-danger" onclick="TrackService.deleteTrack(${track.id})">
                        Удалить
                    </button>
                </div>
            </div>
        `;
    }

    static updatePagination(itemsCount) {
        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        const pageInfo = document.getElementById('page-info');

        if (prevBtn && nextBtn && pageInfo) {
            prevBtn.disabled = this.currentPage <= 1;
            nextBtn.disabled = itemsCount < this.limit;
            pageInfo.textContent = `Страница ${this.currentPage}`;
        }
    }

    static async showTrackDetails(trackId) {
        const track = await this.loadTrackDetails(trackId);
        if (!track) return;

        // Реализация модального окна с деталями трека
        console.log('Track details:', track);
    }

    static initEvents() {
        document.addEventListener('DOMContentLoaded', async () => {
            if (!document.getElementById('track-list')) return;

            // Загрузка треков при открытии страницы
            await this.loadTracks(1);

            // Инициализация фильтров
            const genreFilter = document.getElementById('genre-filter');
            if (genreFilter) {
                genreFilter.addEventListener('change', (e) => {
                    this.loadTracks(1, e.target.value || null);
                });

                // Загрузка жанров для фильтра
                const genres = await GenreService.loadGenres();
                genreFilter.innerHTML = '<option value="">Все</option>' + 
                    genres.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
            }

            // Поиск
            const searchInput = document.getElementById('search');
            if (searchInput) {
                searchInput.addEventListener('input', Utils.debounce(() => {
                    this.loadTracks(1, null, searchInput.value.trim());
                }, 500));
            }

            // Пагинация
            document.getElementById('prev-page')?.addEventListener('click', () => {
                if (this.currentPage > 1) {
                    this.loadTracks(this.currentPage - 1);
                }
            });

            document.getElementById('next-page')?.addEventListener('click', () => {
                this.loadTracks(this.currentPage + 1);
            });

            // Добавление трека
            const addTrackModal = document.getElementById('add-track-modal');
            if (addTrackModal) {
                document.getElementById('add-track-btn')?.addEventListener('click', () => {
                    addTrackModal.classList.remove('hidden');
                });

                document.getElementById('cancel-track')?.addEventListener('click', () => {
                    addTrackModal.classList.add('hidden');
                });

                document.getElementById('track-form')?.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = {
                        title: document.getElementById('track-title').value.trim(),
                        artist: document.getElementById('track-artist').value.trim(),
                        genre_id: parseInt(document.getElementById('track-genre').value)
                    };

                    const success = await this.uploadTrack(formData);
                    if (success) {
                        addTrackModal.classList.add('hidden');
                        e.target.reset();
                    }
                });

                // Загрузка жанров для формы
                const genreSelect = document.getElementById('track-genre');
                if (genreSelect) {
                    const genres = await GenreService.loadGenres();
                    genreSelect.innerHTML = genres.map(g => 
                        `<option value="${g.id}">${g.name}</option>`
                    ).join('');
                }
            }
        });
    }
}

TrackService.initEvents();