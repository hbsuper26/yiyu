import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Enhance the canvas animation to make it more like a modern deep data network
new_script_content = """
    <script>
        // Enhanced Hero Background Particle & Data Flow Animation
        (function() {
            const canvas = document.getElementById('heroCanvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let width, height;
            let particles = [];
            const mouse = { x: null, y: null, radius: 300 };

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
                    this.size = Math.random() * 2 + 0.5;
                    this.baseX = this.x;
                    this.baseY = this.y;
                    this.density = (Math.random() * 30) + 1;
                    // Abstract data flow direction (mostly right and slightly up/down)
                    this.vx = (Math.random() * 0.8) + 0.2;
                    this.vy = (Math.random() - 0.5) * 0.5;
                }

                draw() {
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = 'rgba(59, 130, 246, 0.8)';
                    ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.3})`;
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                    ctx.shadowBlur = 0; // reset
                }

                update() {
                    this.x += this.vx;
                    this.y += this.vy;

                    // Wrap around
                    if (this.x < 0) this.x = width;
                    if (this.x > width) this.x = 0;
                    if (this.y < 0) this.y = height;
                    if (this.y > height) this.y = 0;

                    // Interactive repelling/attracting from mouse
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
                            // Create a vortex effect
                            this.x -= directionX * 1.5;
                            this.y -= directionY * 1.5;
                        }
                    }
                }
            }

            function initParticles() {
                resize();
                particles = [];
                // Calculate number of particles based on screen size for good performance
                let numberOfParticles = Math.min((width * height) / 6000, 200);
                for (let i = 0; i < numberOfParticles; i++) {
                    particles.push(new Particle());
                }
            }

            function animateParticles() {
                // Trail effect by filling with opacity
                ctx.fillStyle = 'rgba(15, 23, 42, 0.3)'; // Slate-900 with opacity for trails
                ctx.fillRect(0, 0, width, height);
                
                for (let i = 0; i < particles.length; i++) {
                    particles[i].update();
                    particles[i].draw();
                    
                    // Connect nodes
                    for (let j = i; j < particles.length; j++) {
                        let dx = particles[i].x - particles[j].x;
                        let dy = particles[i].y - particles[j].y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < 150) {
                            ctx.beginPath();
                            // Gradient line
                            let gradient = ctx.createLinearGradient(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                            gradient.addColorStop(0, `rgba(59, 130, 246, ${0.4 - distance/375})`); // Blue-500
                            gradient.addColorStop(1, `rgba(168, 85, 247, ${0.4 - distance/375})`); // Purple-500
                            
                            ctx.strokeStyle = gradient;
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

            setTimeout(() => {
                initParticles();
                animateParticles();
            }, 100);
        })();
    </script>
"""

# Replace old script with new one
old_script_start = html.find('// Enhanced Hero Background Particle & Data Flow Animation')
if old_script_start != -1:
    old_script_end = html.find('</script>', old_script_start) + 9
    html = html[:old_script_start-15] + new_script_content + html[old_script_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Canvas script enhanced further.")
