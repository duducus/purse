document.addEventListener("DOMContentLoaded", function() {
    const API_KEY = 'AIzaSyDlwWbkTGdAxtlgoMc6XrMM_rIZ0RSqzbk';
    const PLAYLIST_ID = 'PLU8fI-5lkaHpWr-pBBrYCYiw_KqZXWpKE';

    async function fetchPlaylistItems() {
        const response = await fetch(`https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${PLAYLIST_ID}&maxResults=20&key=${API_KEY}`);
        const data = await response.json();
        return data.items;
    }

    function createVideoElement(video) {
        const videoElement = document.createElement('div');
        videoElement.classList.add('video-item');
        videoElement.innerHTML = `
            <a href="https://www.youtube.com/watch?v=${video.snippet.resourceId.videoId}" target="_blank">
                <img src="${video.snippet.thumbnails.default.url}" alt="${video.snippet.title}" class="video-thumbnail">
            </a>
            <div class="video-info">
                <a href="https://www.youtube.com/watch?v=${video.snippet.resourceId.videoId}" target="_blank">
                    <h3 class="video-title">${video.snippet.title}</h3>
                </a>
            </div>
        `;
        return videoElement;
    }

    async function loadPlaylist() {
        const videos = await fetchPlaylistItems();
        const videoContainer = document.getElementById('video-container');
        videoContainer.innerHTML = ''; // Clear previous content

        videos.forEach(video => {
            const videoElement = createVideoElement(video);
            videoContainer.appendChild(videoElement);
        });
    }

    loadPlaylist();

    // Recarga la lista de reproducción cada 5 minutos
    setInterval(loadPlaylist, 300000);
});
