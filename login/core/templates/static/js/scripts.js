// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const videoList = document.querySelector(".video-list");

    // Lista de videos de YouTube (IDs de video)
    const videos = [
        {id: 'VIDEO_ID_1', title: 'Video 1'},
        {id: 'VIDEO_ID_2', title: 'Video 2'},
        {id: 'VIDEO_ID_3', title: 'Video 3'}
        // Añade más videos aquí
    ];

    videos.forEach(video => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = `https://www.youtube.com/watch?v=${video.id}`;
        link.target = "_blank";

        const thumbnail = document.createElement("img");
        thumbnail.src = `https://img.youtube.com/vi/${video.id}/default.jpg`;
        //thumbnail.src = `/perro.png`
        thumbnail.alt = video.title;

        link.appendChild(thumbnail);
        link.appendChild(document.createTextNode(video.title));
        listItem.appendChild(link);
        videoList.appendChild(listItem);
    });
});
