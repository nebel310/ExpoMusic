class LibraryService {
    static async getFavoriteTracks(limit = 10, offset = 0) {
        try {
            return await HttpService.request(
                `/library/favorites?limit=${limit}&offset=${offset}`
            );
        } catch (e) {
            console.error('Failed to get favorite tracks:', e);
            return [];
        }
    }

    static async addToFavorites(trackId) {
        try {
            await HttpService.request(`/library/favorites/add/${trackId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to add to favorites:', e);
            return false;
        }
    }

    static async removeFromFavorites(trackId) {
        try {
            await HttpService.request(`/library/favorites/remove/${trackId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to remove from favorites:', e);
            return false;
        }
    }

    static async getDislikedTracks(limit = 10, offset = 0) {
        try {
            return await HttpService.request(
                `/library/disliked?limit=${limit}&offset=${offset}`
            );
        } catch (e) {
            console.error('Failed to get disliked tracks:', e);
            return [];
        }
    }

    static async addToDisliked(trackId) {
        try {
            await HttpService.request(`/library/disliked/add/${trackId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to add to disliked:', e);
            return false;
        }
    }

    static async removeFromDisliked(trackId) {
        try {
            await HttpService.request(`/library/disliked/remove/${trackId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to remove from disliked:', e);
            return false;
        }
    }

    static async getSavedPlaylists(limit = 10, offset = 0) {
        try {
            return await HttpService.request(
                `/library/saved?limit=${limit}&offset=${offset}`
            );
        } catch (e) {
            console.error('Failed to get saved playlists:', e);
            return [];
        }
    }

    static async savePlaylist(playlistId) {
        try {
            await HttpService.request(`/library/save/${playlistId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to save playlist:', e);
            return false;
        }
    }

    static async unsavePlaylist(playlistId) {
        try {
            await HttpService.request(`/library/unsave/${playlistId}`, 'POST');
            return true;
        } catch (e) {
            console.error('Failed to unsave playlist:', e);
            return false;
        }
    }

    static renderLibrarySection(title, items, itemRenderer) {
        return `
            <div class="library-section">
                <h2>${title}</h2>
                <div class="library-items">
                    ${items.length > 0 
                        ? items.map(item => itemRenderer(item)).join('') 
                        : '<p>Пусто</p>'
                    }
                </div>
            </div>
        `;
    }

    static async loadLibrary() {
        const [favorites, disliked, savedPlaylists] = await Promise.all([
            this.getFavoriteTracks(),
            this.getDislikedTracks(),
            this.getSavedPlaylists()
        ]);

        const container = document.getElementById('library-container');
        if (container) {
            container.innerHTML = [
                this.renderLibrarySection('Избранное', favorites, TrackService.renderTrackItem),
                this.renderLibrarySection('Не понравилось', disliked, TrackService.renderTrackItem),
                this.renderLibrarySection('Сохраненные плейлисты', savedPlaylists, PlaylistService.renderPlaylist)
            ].join('');
        }
    }

    static initEvents() {
        document.addEventListener('DOMContentLoaded', async () => {
            if (document.getElementById('library-container')) {
                await this.loadLibrary();
            }
        });
    }
}

LibraryService.initEvents();