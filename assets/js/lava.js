const canvas = document.getElementById('lava-canvas');
const ctx = canvas.getContext('2d');
let width, height, dots = [];
const colors = ['#00ffff', '#ff00ff', '#00ff00', '#0000ff'];
let mouse = { x: -1000, y: -1000 };
let gyro = { x: 0, y: 0 };

function init() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    dots = Array.from({length: 10}, (_, i) => ({
        x: Math.random() * width, y: Math.random() * height,
        vx: (Math.random() - 0.5) * 3, vy: (Math.random() - 0.5) * 3,
        size: Math.random() * 80 + 80, color: colors[i % colors.length]
    }));
}

function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, width, height);
    
    dots.forEach(dot => {
        dot.x += dot.vx + gyro.x; dot.y += dot.vy + gyro.y;
        if (dot.x < 0 || dot.x > width) dot.vx *= -1;
        if (dot.y < 0 || dot.y > height) dot.vy *= -1;

        let dx = mouse.x - dot.x, dy = mouse.y - dot.y;
        if (Math.hypot(dx, dy) < 250) { dot.x += dx * 0.02; dot.y += dy * 0.02; }

        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
        ctx.fillStyle = dot.color;
        ctx.fill();
    });
    requestAnimationFrame(draw);
}

window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
window.addEventListener('deviceorientation', e => {
    if(!e.gamma || !e.beta) return;
    gyro.x = e.gamma * 0.15; gyro.y = (e.beta - 45) * 0.15;
});
window.addEventListener('resize', init);
init(); draw();
