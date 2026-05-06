document.addEventListener('mousemove', (e) => {
    const album = document.querySelector('.album-cover-wrapper');
    if (!album) return;
    
    const x = (window.innerWidth / 2 - e.pageX) / 30;
    const y = (window.innerHeight / 2 - e.pageY) / 30;
    
    album.style.transform = `translateY(-50%) rotate(5deg) rotateY(${x}deg) rotateX(${y}deg)`;
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Music Player Logic
const playBtn = document.getElementById('master-play');
const playIcon = document.getElementById('play-icon');
const progressBar = document.getElementById('player-progress');
let isPlaying = false;
let progress = 35;

if (playBtn) {
    playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
            playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path>';
            simulateProgress();
        } else {
            playIcon.innerHTML = '<path d="M8 5v14l11-7z"></path>';
        }
    });
}

function simulateProgress() {
    if (!isPlaying) return;
    progress += 0.1;
    if (progress > 100) progress = 0;
    progressBar.style.width = `${progress}%`;
    requestAnimationFrame(simulateProgress);
}
