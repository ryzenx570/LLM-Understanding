/**
 * Audio Narrator Controller
 * Injected globally to handle local MP3 playback without overlap.
 */

class AudioNarrator {
    constructor() {
        this.audio = new Audio();
        this.enabled = false;
        this.currentTrack = null;
        
        this.initUI();
    }

    initUI() {
        // Inject dynamic keyframes for the flare effect
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes flareAmber {
                0% { box-shadow: 0 0 5px rgba(250, 199, 117, 0.2); transform: scale(1); }
                50% { box-shadow: 0 0 25px rgba(250, 199, 117, 0.6); transform: scale(1.03); }
                100% { box-shadow: 0 0 5px rgba(250, 199, 117, 0.2); transform: scale(1); }
            }
            @keyframes flareTeal {
                0% { box-shadow: 0 0 10px rgba(159, 225, 203, 0.3); transform: scale(1); }
                50% { box-shadow: 0 0 35px rgba(159, 225, 203, 0.9); transform: scale(1.05); }
                100% { box-shadow: 0 0 10px rgba(159, 225, 203, 0.3); transform: scale(1); }
            }
            #narrator-toggle {
                transition: all 0.4s ease;
            }
            #narrator-toggle.n-off {
                animation: flareAmber 3s infinite ease-in-out;
                background: var(--amber-f, #412402) !important;
                border-color: var(--amber-t, #FAC775) !important;
                color: #fff !important;
            }
            #narrator-toggle.n-on {
                animation: flareTeal 2s infinite ease-in-out;
                background: var(--teal-f, #04342C) !important;
                border-color: var(--teal-t, #9FE1CB) !important;
                color: #fff !important;
            }
            #narrator-toggle:hover {
                filter: brightness(1.3);
            }
        `;
        document.head.appendChild(style);

        // Build floating toggle button
        const btn = document.createElement('button');
        btn.id = 'narrator-toggle';
        btn.className = 'n-off';
        btn.innerHTML = '🔈 Enable Narration';
        
        // Basic fixed styles placing it at top right
        Object.assign(btn.style, {
            position: 'fixed',
            top: '30px',
            right: '40px',
            padding: '12px 24px',
            border: '1px solid',
            borderRadius: '30px',
            fontSize: '13px',
            fontWeight: '700',
            cursor: 'pointer',
            zIndex: '9999',
            fontFamily: "'Inter', 'Outfit', sans-serif",
            textTransform: 'uppercase',
            letterSpacing: '1px'
        });

        btn.onclick = () => {
            this.enabled = !this.enabled;
            if (this.enabled) {
                btn.innerHTML = '🔊 Narration ON';
                btn.className = 'n-on';
                
                // If a track was queued, play it now
                if(this.currentTrack) {
                    this.play(this.currentTrack);
                }
            } else {
                btn.innerHTML = '🔈 Narration OFF';
                btn.className = 'n-off';
                this.stop();
            }
        };

        document.body.appendChild(btn);
    }

    play(trackId) {
        this.currentTrack = trackId;
        
        // Never auto-play if user explicitly didn't allow it
        if (!this.enabled) return;

        this.stop(); // Stop anything playing
        
        // Build relative path
        this.audio.src = `audio/${trackId}.mp3`;
        
        this.audio.play().catch(e => {
            console.warn("Audio play blocked by browser. User must interact first: ", e);
        });
    }

    stop() {
        if(!this.audio.paused) {
            this.audio.pause();
            this.audio.currentTime = 0;
        }
    }
}

// Instantiate globally
window.Narrator = new AudioNarrator();
