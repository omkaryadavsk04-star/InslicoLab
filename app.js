const canvas = document.querySelector("#bioCanvas");
const ctx = canvas.getContext("2d");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

let width = 0;
let height = 0;
let particles = [];

function resizeCanvas() {
  const ratio = window.devicePixelRatio || 1;
  width = canvas.clientWidth;
  height = canvas.clientHeight;
  canvas.width = Math.floor(width * ratio);
  canvas.height = Math.floor(height * ratio);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

  const count = Math.max(34, Math.min(92, Math.floor(width / 18)));
  particles = Array.from({ length: count }, (_, index) => ({
    x: (index * 89) % Math.max(width, 1),
    y: (index * 137) % Math.max(height, 1),
    vx: (Math.sin(index) * 0.45) + 0.18,
    vy: (Math.cos(index * 1.7) * 0.34) + 0.08,
    radius: index % 5 === 0 ? 3.2 : 2.1,
    tone: index % 7 === 0 ? "#f4b860" : index % 3 === 0 ? "#58d68d" : "#39d7ec",
  }));
}

function drawNetwork() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#050607";
  ctx.fillRect(0, 0, width, height);

  for (let i = 0; i < particles.length; i += 1) {
    const current = particles[i];

    for (let j = i + 1; j < particles.length; j += 1) {
      const next = particles[j];
      const dx = current.x - next.x;
      const dy = current.y - next.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 150) {
        ctx.strokeStyle = `rgba(57, 215, 236, ${0.16 * (1 - distance / 150)})`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(current.x, current.y);
        ctx.lineTo(next.x, next.y);
        ctx.stroke();
      }
    }
  }

  particles.forEach((particle) => {
    ctx.fillStyle = particle.tone;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
    ctx.fill();

    if (!prefersReducedMotion) {
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x > width + 20) particle.x = -20;
      if (particle.y > height + 20) particle.y = -20;
      if (particle.x < -20) particle.x = width + 20;
      if (particle.y < -20) particle.y = height + 20;
    }
  });

  if (!prefersReducedMotion) {
    requestAnimationFrame(drawNetwork);
  }
}

resizeCanvas();
drawNetwork();
window.addEventListener("resize", () => {
  resizeCanvas();
  if (prefersReducedMotion) drawNetwork();
});
