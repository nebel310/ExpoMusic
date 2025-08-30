class PlaylistService {
    static async createPlaylist(name, isPublic = false) {
        try {
            return await HttpService.request('/playlists', 'POST', { name, is_public: isPublic });
        } catch (e) {
            console.error('Failed to create playlist:', e);
            return null;
        }
    }

    static async getPlaylist(playlistId) {
        try {
            return await HttpService.request(`/playlists/${playlistId}`);
        } catch (e) {
            console.error('Failed to get playlist:', e);
            return null;
        }
    }

    static async updatePlaylist(playlistId, updateData) {
        try {
            return await HttpService.request(
                `/playlists/update/${playlistId}`,
                'PUT',
                updateData
            );
        } catch (e) {
            console.error('Failed to update playlist:', e);
            return null;
        }
    }

    static async deletePlaylist(playlistId) {
        try {
            await HttpService.request(`/playlists/remove/${playlistId}`, 'DELETE');
            return true;
        } catch (e) {
            console.error('Failed to delete playlist:', e);
            return false;
        }
    }

    static async addTrackToPlaylist(playlistId, trackId) {
        try {
            await HttpService.request('/playlists/add-track', 'POST', {
                playlist_id: playlistId,
                track_id: trackId
            });
            return true;
        } catch (e) {
            console.error('Failed to add track to playlist:', e);
            return false;
        }
    }

    static async removeTrackFromPlaylist(playlistId, trackId) {
        try {
            await HttpService.request('/playlists/remove-track', 'POST', {
                playlist_id: playlistId,
                track_id: trackId
            });
            return true;
        } catch (e) {
            console.error('Failed to remove track from playlist:', e);
            return false;
        }
    }

    static async getUserPlaylists() {
        try {
            return await HttpService.request('/playlists');
        } catch (e) {
            console.error('Failed to get user playlists:', e);
            return [];
        }
    }

    static renderPlaylist(playlist) {
        return `
            <div class="playlist-item" data-id="${playlist.id}">
                <h3>${playlist.name}</h3>
                <p>${playlist.is_public ? 'Публичный' : 'Приватный'}</p>
                <p>Треков: ${playlist.track_ids?.length || 0}</p>
                <div class="playlist-actions">
                    <button class="btn-secondary" onclick="PlaylistService.showPlaylistDetails(${playlist.id})">
                        Открыть
                    </button>
                    <button class="btn-danger" onclick="PlaylistService.deletePlaylistConfirm(${playlist.id})">
                        Удалить
                    </button>
                </div>
            </div>
        `;
    }

    static async deletePlaylistConfirm(playlistId) {
        if (confirm('Вы уверены, что хотите удалить этот плейлист?')) {
            const success = await this.deletePlaylist(playlistId);
            if (success) {
                this.loadUserPlaylists();
            }
        }
    }

    static async loadUserPlaylists() {
        const playlists = await this.getUserPlaylists();
        const container = document.getElementById('user-playlists');
        if (container) {
            container.innerHTML = playlists.length > 0
                ? playlists.map(p => this.renderPlaylist(p)).join('')
                : '<p>У вас пока нет плейлистов</p>';
        }
    }

    static initEvents() {
        document.addEventListener('DOMContentLoaded', async () => {
            if (document.getElementById('user-playlists')) {
                await this.loadUserPlaylists();
            }
        });
    }
}

PlaylistService.initEvents();