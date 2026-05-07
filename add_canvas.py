import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the canvas element in the Hero section
# Add id="heroCanvas" to the section and absolute canvas inside it.
hero_pattern = r'(<section[^>]*class="[^"]*hero-bg[^"]*"[^>]*>)'
canvas_html = '\n        <canvas id="heroCanvas" class="absolute inset-0 z-0"></canvas>'

if '<canvas id="heroCanvas"' not in html:
    html = re.sub(hero_pattern, r'\1' + canvas_html, html)

# 2. Add the JavaScript for the particle animation right before </body>
script_content = """
    <script>
        // Hero Background Particle Animation
        (function() {
            const canvas = document.getElementById('heroCanvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let width, height;
            let particles = [];
            const mouse = { x: null, y: null, radius: 150 };

            function resize() {
                const parent = canvas.parentElement;
                width = canvas.width = parent.offsetWidth;
                height = canvas.height = parent.offsetHeight;
            }

            window.addEventListener('resize', resize);
            
            canvas.parentElement.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                mouse.x = e.clientX - rect.left;
                mouse.y = e.clientY - rect.top;
            });
            
            canvas.parentElement.addEventListener('mouseout', () => {
                mouse.x = null;
                mouse.y = null;
            });

            class Particle {
                constructor() {
                    this.x = Math.random() * width;
                    this.y = Math.random() * height;
                    this.size = Math.random() * 2 + 1;
                    this.baseX = this.x;
                    this.baseY = this.y;
                    this.density = (Math.random() * 30) + 1;
                    this.vx = (Math.random() - 0.5) * 1;
                    this.vy = (Math.random() - 0.5) * 1;
                }

                draw() {
                    ctx.fillStyle = 'rgba(59, 130, 246, 0.5)';
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                }

                update() {
                    this.x += this.vx;
                    this.y += this.vy;

                    if (this.x < 0 || this.x > width) this.vx = -this.vx;
                    if (this.y < 0 || this.y > height) this.vy = -this.vy;

                    if (mouse.x != null) {
                        let dx = mouse.x - this.x;
                        let dy = mouse.y - this.y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        let forceDirectionX = dx / distance;
                        let forceDirectionY = dy / distance;
                        let maxDistance = mouse.radius;
                        let force = (maxDistance - distance) / maxDistance;
                        let directionX = forceDirectionX * force * this.density;
                        let directionY = forceDirectionY * force * this.density;

                        if (distance < mouse.radius) {
                            this.x -= directionX;
                            this.y -= directionY;
                        } else {
                            if (this.x !== this.baseX) {
                                let dx = this.x - this.baseX;
                                this.x -= dx / 50;
                            }
                            if (this.y !== this.baseY) {
                                let dy = this.y - this.baseY;
                                this.y -= dy / 50;
                            }
                        }
                    }
                }
            }

            function initParticles() {
                resize();
                particles = [];
                let numberOfParticles = (width * height) / 9000;
                for (let i = 0; i < numberOfParticles; i++) {
                    particles.push(new Particle());
                }
            }

            function animateParticles() {
                ctx.clearRect(0, 0, width, height);
                for (let i = 0; i < particles.length; i++) {
                    particles[i].update();
                    particles[i].draw();
                    
                    for (let j = i; j < particles.length; j++) {
                        let dx = particles[i].x - particles[j].x;
                        let dy = particles[i].y - particles[j].y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < 120) {
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(59, 130, 246, ${0.4 - distance/300})`;
                            ctx.lineWidth = 1;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                            ctx.closePath();
                        }
                    }
                }
                requestAnimationFrame(animateParticles);
            }

            // Initialize after a short delay to ensure DOM is ready
            setTimeout(() => {
                initParticles();
                animateParticles();
            }, 100);
        })();
    </script>
"""

if 'heroCanvas' not in html or 'animateParticles' not in html:
    html = html.replace('</body>', script_content + '</body>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Canvas added.")
