import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's adjust the Hero text elements to have GSAP parallax
parallax_script = """
            // GSAP Parallax for Hero Elements
            if (typeof gsap !== 'undefined') {
                const heroSection = document.querySelector('.hero-bg');
                
                // Text layers
                const textFront = document.querySelector('.hero-bg .text-left h1');
                const textMid = document.querySelector('.hero-bg .text-left p');
                const buttons = document.querySelector('.hero-bg .text-left .flex');
                
                // 3D Mockup
                const heroMockup = document.querySelector('.hero-bg .floating');
                
                if (heroSection) {
                    heroSection.addEventListener('mousemove', (e) => {
                        const rect = heroSection.getBoundingClientRect();
                        const x = (e.clientX - rect.left) / rect.width - 0.5;
                        const y = (e.clientY - rect.top) / rect.height - 0.5;
                        
                        // Text moves slightly opposite to mouse
                        if (textFront) gsap.to(textFront, { x: x * -30, y: y * -30, duration: 1.5, ease: 'power2.out' });
                        if (textMid) gsap.to(textMid, { x: x * -15, y: y * -15, duration: 1.5, ease: 'power2.out' });
                        if (buttons) gsap.to(buttons, { x: x * -5, y: y * -5, duration: 1.5, ease: 'power2.out' });
                        
                        // Mockup rotates and moves with mouse
                        if (heroMockup) gsap.to(heroMockup, {
                            x: x * 40,
                            y: y * 40,
                            rotationY: x * 15,
                            rotationX: y * -15,
                            duration: 1.5,
                            ease: 'power2.out'
                        });
                    });
                    
                    // Reset on mouse leave
                    heroSection.addEventListener('mouseleave', () => {
                        if (textFront) gsap.to(textFront, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (textMid) gsap.to(textMid, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (buttons) gsap.to(buttons, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (heroMockup) gsap.to(heroMockup, { x: 0, y: 0, rotationY: 0, rotationX: 0, duration: 1.5, ease: 'power2.out' });
                    });
                }
            }
"""

# Replace old GSAP parallax
old_gsap_start = html.find('// GSAP Parallax for Hero')
if old_gsap_start != -1:
    old_gsap_end = html.find('            setTimeout(() => {', old_gsap_start)
    html = html[:old_gsap_start] + parallax_script + html[old_gsap_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Parallax enhanced.")
