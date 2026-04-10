// Ensure GSAP and ScrollTrigger are loaded before executing
document.addEventListener('DOMContentLoaded', () => {
  gsap.registerPlugin(ScrollTrigger);

  // Setup the visual tracker from existing layers
  const tracker = document.createElement('div');
  tracker.className = 'scroll-tracker';
  document.body.appendChild(tracker);

  const panels = document.querySelectorAll('.panel');
  const blobs = {
    b1: document.querySelector('.blob-1'),
    b2: document.querySelector('.blob-2')
  };

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

  // Abstract background animation per section
  function animateBackground(index) {
    const colors = [
      '#0c447c', '#4a1b0c', '#173404', '#26215C', '#BA7517', '#1D9E75'
    ];
    const c1 = colors[index % colors.length];
    const c2 = colors[(index + 2) % colors.length];

    if(blobs.b1 && blobs.b2) {
      gsap.to(blobs.b1, {
        background: c1,
        x: (Math.random() - 0.5) * 300,
        y: (Math.random() - 0.5) * 300,
        scale: 0.8 + Math.random() * 0.5,
        duration: 2,
        ease: "sine.inOut"
      });
      gsap.to(blobs.b2, {
        background: c2,
        x: (Math.random() - 0.5) * 300,
        y: (Math.random() - 0.5) * 300,
        scale: 0.8 + Math.random() * 0.5,
        duration: 2,
        ease: "sine.inOut"
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
