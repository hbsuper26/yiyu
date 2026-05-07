import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I see what happened. In tweak_giant.py, I did:
# old_end = html.find('if (textFront)', old_start)
# html = html[:old_start] + gsap_update[25:] + html[old_end:]
# But `if (textFront)` was part of the `mouseleave` event listener reset block!
# So I accidentally deleted the closing braces of the `mousemove` event listener and part of the reset!
# Let's fix the entire GSAP parallax script block.

parallax_script_correct = """
            // GSAP Parallax for Hero Elements
            if (typeof gsap !== 'undefined') {
                const heroSection = document.querySelector('.hero-bg');
                
                // Text layers
                const textFront = document.querySelector('.hero-bg .text-left h1');
                const textMid = document.querySelector('.hero-bg .text-left p');
                const buttons = document.querySelector('.hero-bg .text-left .flex');
                
                // 3D Mockup
                const heroMockup = document.querySelector('.hero-bg .floating');
                
                // Giant Text
                const giantTextBack = document.getElementById('giantTextBack');
                const giantTextFront = document.getElementById('giantTextFront');
                
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
                        
                        // Giant Text Parallax Depth
                        if (giantTextBack) gsap.to(giantTextBack, { x: x * 80, y: y * 40, duration: 2, ease: 'power2.out' });
                        if (giantTextFront) gsap.to(giantTextFront, { x: x * 150, y: y * 80, duration: 2, ease: 'power2.out' });
                    });
                    
                    // Reset on mouse leave
                    heroSection.addEventListener('mouseleave', () => {
                        if (textFront) gsap.to(textFront, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (textMid) gsap.to(textMid, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (buttons) gsap.to(buttons, { x: 0, y: 0, duration: 1.5, ease: 'power2.out' });
                        if (heroMockup) gsap.to(heroMockup, { x: 0, y: 0, rotationY: 0, rotationX: 0, duration: 1.5, ease: 'power2.out' });
                        if (giantTextBack) gsap.to(giantTextBack, { x: 0, y: 0, duration: 2, ease: 'power2.out' });
                        if (giantTextFront) gsap.to(giantTextFront, { x: 0, y: 0, duration: 2, ease: 'power2.out' });
                    });
                }
            }
"""

start_idx = html.find('// GSAP Parallax for Hero Elements')
end_idx = html.find('setTimeout(() => {', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + parallax_script_correct + "            " + html[end_idx:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
