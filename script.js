particlesJS.load('particles-js', 'https://cdn.jsdelivr.net/gh/VincentGarreau/particles.js@master/demo/particles.json', function() {
    console.log('Particles.js config loaded');
});

window.onscroll = function () {
    const scrollIndicator = document.getElementById("scrollIndicator");
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    scrollIndicator.style.transform = `scaleX(${scrolled / 100})`;
};
