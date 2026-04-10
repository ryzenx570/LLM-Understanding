// Ensure GSAP and ScrollTrigger are loaded before executing
document.addEventListener('DOMContentLoaded', () => {
  gsap.registerPlugin(ScrollTrigger);

  // Setup the visual tracker from existing layers
  const tracker = document.createElement('div');
  tracker.className = 'scroll-tracker';
  document.body.appendChild(tracker);

  const panels = document.querySelectorAll('.panel');
  
  // Parallax: Drive the Three.js camera deeper into the particle field along the Z-axis
  // The moment the page scrolls, the camera flies flawlessly over the entire document height
  ScrollTrigger.create({
    trigger: document.documentElement,
    start: "top top",
    end: "bottom bottom",
    onUpdate: (self) => {
      // Progress ranges from 0.0 (top) to 1.0 (bottom)
      // Map this to a -4500 deep flight
      if (window.threeCamera) {
          window.threeCamera.position.z = -4500 * self.progress;
      }
    }
  });

  panels.forEach((panel, index) => {
    // Determine the short label for the tracker
    let labelText = `Layer ${index}`;
    if(index === 0) labelText = "Overview";
    // We can also extract title text for tracker
    const titleElement = panel.querySelector('.panel-title');
    if(titleElement) {
        // Just use layer number or Overview
        labelText = titleElement.innerText.split('—')[0].trim();
    }

    const dot = document.createElement('div');
    dot.className = 'tracker-dot';
    dot.innerHTML = `<span class="label">${labelText}</span>`;
    tracker.appendChild(dot);

    // Initial state
    gsap.set(panel, { opacity: 0, y: 50 });

    // ScrollTrigger for each panel
    ScrollTrigger.create({
      trigger: panel,
      start: "top 60%",     // When the top of the panel hits 60% of viewport
      end: "bottom 40%",    // When bottom hits 40%
      onEnter: () => {
        gsap.to(panel, { opacity: 1, y: 0, duration: 1, ease: "power3.out" });
        updateTracker(index);
        animateBackground(index);
        triggerAudio(panel);
      },
      onEnterBack: () => {
        gsap.to(panel, { opacity: 1, y: 0, duration: 1, ease: "power3.out" });
        updateTracker(index);
        animateBackground(index);
        triggerAudio(panel);
      },
      onLeave: () => {
        gsap.to(panel, { opacity: 0, y: -50, duration: 0.8, ease: "power3.in" });
      },
      onLeaveBack: () => {
        gsap.to(panel, { opacity: 0, y: 50, duration: 0.8, ease: "power3.in" });
      }
    });
    
    function triggerAudio(panelElement) {
        if (!window.Narrator) return;
        const rawId = panelElement.id.replace('panel-', '');
        const trackId = rawId === 'overview' ? 'layer_overview' : 'layer_' + rawId;
        window.Narrator.play(trackId);
    }

    // Sub-elements parallax (topics)
    const topics = panel.querySelectorAll('.topic, .paper');
    if(topics.length > 0) {
      gsap.fromTo(topics, 
        { y: 50, opacity: 0 },
        {
          y: 0, opacity: 1, duration: 0.8, stagger: 0.1,
          scrollTrigger: {
            trigger: panel,
            start: "top 70%",
            toggleActions: "play none none reverse"
          }
        }
      );
    }
  });

  function updateTracker(activeIndex) {
    const dots = document.querySelectorAll('.tracker-dot');
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === activeIndex);
    });
  }

  // Connect GSAP dynamically to the Three.js Engine Material
  function animateBackground(index) {
    // 22 Unique Deep-Space Colors mapped exactly 1-to-1 with the Curriculum Panels
    const colors = [
      '#051525', // 0: Overview (Deep Space Blue)
      '#1a0f05', // 1: L0 (Burnt Amber)
      '#2a1040', // 2: L1 (Royal Purple)
      '#02261a', // 3: L2 (Deep Emerald)
      '#300d11', // 4: L3 (Crimson)
      '#152e4d', // 5: L4 (Slate Blue)
      '#1c260b', // 6: L5 (Olive Gold)
      '#381b0a', // 7: L6 (Rust)
      '#1c0c24', // 8: L7 (Dark Violet)
      '#0b292e', // 9: L8 (Teal Abyss)
      '#36112c', // 10: L9 (Wine Red)
      '#172e12', // 11: L10 (Forest Night)
      '#2b1836', // 12: L11 (Plum)
      '#38240f', // 13: L12 (Bronze)
      '#071933', // 14: L13 (Navy)
      '#20362c', // 15: L14 (Jade)
      '#3b1111', // 16: L15 (Dark Blood)
      '#2c203b', // 17: L16 (Amethyst)
      '#0b3017', // 18: L17 (Pine)
      '#382b13', // 19: L18 (Antique Gold)
      '#0b1626', // 20: L19 (Abyssal Void)
      '#1a1012'  // 21: Finale
    ];
    const c1 = colors[index % colors.length];

    // Check if the Three.js webgl engine successfully hooked the custom material
    if (window.threeMaterial && window.THREE) {
      const targetColor = new THREE.Color(c1);
      
      // We directly instruct GSAP to actively tween the internal r, g, b floats of the WebGL material
      gsap.to(window.threeMaterial.color, {
        r: targetColor.r,
        g: targetColor.g,
        b: targetColor.b,
        duration: 1.5,
        ease: "power2.out"
      });
    }
  }

  // Smooth scroll click handler for tracker dots
  const dots = document.querySelectorAll('.tracker-dot');
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      gsap.to(window, {
        duration: 1, 
        scrollTo: { y: panels[i], offsetY: 0 }, 
        ease: "power3.inOut"
      });
    });
  });

});
