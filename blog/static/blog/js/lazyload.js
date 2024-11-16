document.addEventListener("DOMContentLoaded", function() {
    const videos = document.querySelectorAll('video[data-src]');

    const lazyLoad = target => {
        const io = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const video = entry.target;
                    video.src = video.dataset.src;
                    video.removeAttribute('data-src');
                    observer.unobserve(video);
                }
            });
        });

        io.observe(target);
    };

    videos.forEach(lazyLoad);
});