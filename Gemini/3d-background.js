document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('webgl-container');
    if (!container) return;

    // 1. Setup Scene
    const scene = new THREE.Scene();
    
    // Add a subtle depth fog so far-away particles fade beautifully into the dark background
    scene.fog = new THREE.FogExp2(0x03080c, 0.0008);

    // 2. Setup Camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 4000);
    camera.position.z = 0;
    
    // Expose camera globally for GSAP ScrollTrigger to hook into
    window.threeCamera = camera;

    // 3. Setup Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // limit pixel ratio for performance
    container.appendChild(renderer.domElement);

    // 4. Generate Quantum Token Field (Particles)
    const particleCount = 15000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    
    // Distribute randomly across a massive corridor
    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 3000;     // x
        positions[i+1] = (Math.random() - 0.5) * 2000;   // y
        positions[i+2] = (Math.random() * -6000) + 500;  // z (deep space stretching back to -5500)
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    // Create the glowing material
    const material = new THREE.PointsMaterial({
        size: 3.5,
        color: 0x378ADD, // Initial Gemini Blue
        transparent: true,
        opacity: 0.6,
        sizeAttenuation: true,
        blending: THREE.AdditiveBlending, // Enables the intense overlapping glow effect
        depthWrite: false
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Expose material globally so GSAP can dynamically shift its UI color index
    window.threeMaterial = material;
    
    // 5. Ambient Auto-Rotation Loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        
        const delta = clock.getDelta();
        // Slowly rotate the entire universe galaxy slightly allowing it to "breathe" constantly
        particles.rotation.z += delta * 0.03;
        particles.rotation.y += delta * 0.015;

        renderer.render(scene, camera);
    }
    
    animate();

    // 6. Handle Window Resizing
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
