import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's adjust the canvas to be even more striking, adding a "snow" or "data particles" effect 
# to mimic the dynamic nature of the GIF.
enhanced_particle_script = """
    <script>
        // Immersive 3D Data Particle Network Animation
        (function() {
            const canvas = document.getElementById('heroCanvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let width, height;
            let particles = [];
            let time = 0;
            const mouse = { x: window.innerWidth/2, y: window.innerHeight/2, radius: 300, targetX: window.innerWidth/2, targetY: window.innerHeight/2 };

            function resize() {
                const parent = canvas.parentElement;
                width = canvas.width = parent.offsetWidth;
                height = canvas.height = parent.offsetHeight;
            }

            window.addEventListener('resize', resize);
            
            canvas.parentElement.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                mouse.targetX = e.clientX - rect.left;
                mouse.targetY = e.clientY - rect.top;
            });
            
            class Particle {
                constructor(isForeground) {
                    this.x = Math.random() * width;
                    this.y = Math.random() * height;
                    this.z = Math.random() * 100; // Fake 3D depth
                    this.isForeground = isForeground;
                    this.size = isForeground ? (Math.random() * 3 + 2) : (Math.random() * 1.5 + 0.5);
                    this.baseX = this.x;
                    this.baseY = this.y;
                    this.density = (Math.random() * 40) + 10;
                    this.vx = (Math.random() - 0.5) * (isForeground ? 1 : 0.5);
                    this.vy = (Math.random() - 0.5) * (isForeground ? 1 : 0.5);
                    this.color = isForeground ? `rgba(96, 165, 250, ${Math.random() * 0.8 + 0.2})` : `rgba(167, 139, 250, ${Math.random() * 0.5 + 0.1})`;
                }

                draw() {
                    let scale = 100 / (100 + this.z);
                    let x2d = (this.x - width/2) * scale + width/2;
                    let y2d = (this.y - height/2) * scale + height/2;
                    let r2d = this.size * scale;

                    ctx.shadowBlur = this.isForeground ? 15 : 5;
                    ctx.shadowColor = this.isForeground ? '#3b82f6' : '#a855f7';
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.arc(x2d, y2d, Math.max(r2d, 0.1), 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                    ctx.shadowBlur = 0; // reset
                }

                update() {
                    // Smooth mouse follow
                    mouse.x += (mouse.targetX - mouse.x) * 0.05;
                    mouse.y += (mouse.targetY - mouse.y) * 0.05;

                    this.x += this.vx + Math.sin(time * 0.001 + this.y * 0.01) * 0.5;
                    this.y += this.vy + Math.cos(time * 0.001 + this.x * 0.01) * 0.5;
                    this.z += Math.sin(time * 0.002) * 0.1;

                    // Wrap around
                    if (this.x < -100) this.x = width + 100;
                    if (this.x > width + 100) this.x = -100;
                    if (this.y < -100) this.y = height + 100;
                    if (this.y > height + 100) this.y = -100;

                    // Mouse interaction
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
                        this.x -= directionX * (this.isForeground ? 1.5 : 0.5);
                        this.y -= directionY * (this.isForeground ? 1.5 : 0.5);
                    }
                }
            }

            function initParticles() {
                resize();
                particles = [];
                let numberOfParticles = Math.min((width * height) / 4000, 250);
                for (let i = 0; i < numberOfParticles; i++) {
                    particles.push(new Particle(i < numberOfParticles * 0.3)); // 30% foreground
                }
            }

            function animateParticles() {
                time++;
                // Dark background with slight trail
                ctx.fillStyle = 'rgba(15, 23, 42, 0.4)';
                ctx.fillRect(0, 0, width, height);
                
                // Draw background gradient to mimic deep space
                let bgGradient = ctx.createRadialGradient(mouse.x, mouse.y, 0, width/2, height/2, width);
                bgGradient.addColorStop(0, 'rgba(59, 130, 246, 0.05)');
                bgGradient.addColorStop(1, 'rgba(15, 23, 42, 0)');
                ctx.fillStyle = bgGradient;
                ctx.fillRect(0, 0, width, height);
                
                for (let i = 0; i < particles.length; i++) {
                    particles[i].update();
                    particles[i].draw();
                    
                    // Connect nodes if they are close in 2D space
                    if(particles[i].isForeground) {
                        for (let j = i + 1; j < particles.length; j++) {
                            if(!particles[j].isForeground) continue;
                            
                            let dx = particles[i].x - particles[j].x;
                            let dy = particles[i].y - particles[j].y;
                            let distance = Math.sqrt(dx * dx + dy * dy);
                            
                            if (distance < 120) {
                                ctx.beginPath();
                                let gradient = ctx.createLinearGradient(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
                                gradient.addColorStop(0, `rgba(96, 165, 250, ${0.5 - distance/240})`);
                                gradient.addColorStop(1, `rgba(167, 139, 250, ${0.5 - distance/240})`);
                                
                                ctx.strokeStyle = gradient;
                                ctx.lineWidth = 1.5;
                                ctx.moveTo(particles[i].x, particles[i].y);
                                ctx.lineTo(particles[j].x, particles[j].y);
                                ctx.stroke();
                                ctx.closePath();
                            }
                        }
                    }
                }

                // Draw some abstract floating words
                if(time % 60 === 0) {
                    ctx.fillStyle = `rgba(255, 255, 255, 0.05)`;
                    ctx.font = `bold ${Math.random() * 20 + 20}px sans-serif`;
                    let text = ["FUNDS", "GLOBAL", "ADS", "ROI", "SPEED", "SECURE"][Math.floor(Math.random()*6)];
                    ctx.fillText(text, Math.random() * width, Math.random() * height);
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

old_script_start = html.find('// Enhanced Hero Background Particle & Data Flow Animation')
if old_script_start != -1:
    old_script_end = html.find('</script>', old_script_start) + 9
    html = html[:old_script_start-15] + enhanced_particle_script + html[old_script_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Canvas 3D depth added.")
