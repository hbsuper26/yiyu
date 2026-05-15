import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()


    

# Make the elements inside hero section relative so they stay above the canvas
html = html.replace('<div class="grid lg:grid-cols-2 gap-12 items-center">', '<div class="grid lg:grid-cols-2 gap-12 items-center relative z-10 pointer-events-none">')

# Make sure buttons inside hero section have pointer-events-auto
html = html.replace('<div class="flex flex-col sm:flex-row gap-4">', '<div class="flex flex-col sm:flex-row gap-4 pointer-events-auto">')

# And the 3D dashboard mockup should be interactive or at least visible
html = html.replace('<div class="relative hidden lg:block floating">', '<div class="relative hidden lg:block floating pointer-events-auto">')

# Let's also add some GSAP parallax to the hero text to match the requested animation style
gsap_script = """
            // GSAP Parallax for Hero
            if (typeof gsap !== 'undefined') {
                const heroSection = document.querySelector('.hero-bg');
                const heroText = document.querySelector('.hero-bg .text-left');
                const heroMockup = document.querySelector('.hero-bg .floating');
                
                if (heroSection && heroText && heroMockup) {
                    heroSection.addEventListener('mousemove', (e) => {
                        const x = (e.clientX / window.innerWidth - 0.5) * 20;
                        const y = (e.clientY / window.innerHeight - 0.5) * 20;
                        
                        gsap.to(heroText, {
                            x: x * -1,
                            y: y * -1,
                            duration: 1,
                            ease: 'power2.out'
                        });
                        
                        gsap.to(heroMockup, {
                            x: x * 2,
                            y: y * 2,
                            rotationY: x * 0.5,
                            rotationX: y * -0.5,
                            duration: 1,
                            ease: 'power2.out'
                        });
                    });
                }
            }
"""

# Insert GSAP script after animateParticles
html = html.replace('setTimeout(() => {', gsap_script + '\n            setTimeout(() => {')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Parallax added.")
