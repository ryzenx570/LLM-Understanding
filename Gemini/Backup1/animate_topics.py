import re

palettes = [
    {"accent": "#1D9E75", "f": "var(--teal-f)", "t": "var(--teal-t)"},
    {"accent": "#BA7517", "f": "var(--amber-f)", "t": "var(--amber-t)"},
    {"accent": "#7F77DD", "f": "var(--purple-f)", "t": "var(--purple-t)"},
    {"accent": "#378ADD", "f": "var(--blue-f)", "t": "var(--blue-t)"},
    {"accent": "#D85A30", "f": "var(--coral-f)", "t": "var(--coral-t)"},
    {"accent": "#639922", "f": "var(--green-f)", "t": "var(--green-t)"},
    {"accent": "#D4537E", "f": "var(--pink-f)", "t": "var(--pink-t)"},
    {"accent": "#E24B4A", "f": "var(--red-f)", "t": "var(--red-t)"}
]

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to find each topic grid, and then process the topics inside it
# to stagger the delay and rotate colors.
grid_pattern = re.compile(r'<div class="topic-grid">(.*?)</div>', re.DOTALL)

def process_grid(match):
    grid_content = match.group(1)
    
    # Check if this grid already has fluid-box (like Layer 2). If so, skip or re-process?
    # To be safe, we'll re-process to ensure it's correct or leave it alone.
    # The prompt says "that don't have your changes", so if it has fluid-box, skip it?
    # Wait, the user said "do it for all layers that don't have your changes". 
    # It's fine to just process any topic that DOES NOT have fluid-box.
    
    topic_pattern = re.compile(r'<div class="topic"\s+style="--accent:[^>]+>\s*<span class="badge"\s+style="([^>]+)">')
    
    parts = []
    last_end = 0
    delay_idx = 0
    color_idx = 0 # We'll just rotate through the colors for variety
    
    # Wait, the regex `topic_pattern` above isn't robust for the whole div start.
    # Let's match just `<div class="topic" style="--accent:[#a-fA-F0-9]+">`
    # and the badge `<span class="badge" style="background:var(--...);color:var(--...)">`
    
    # Better approach:
    # Just find `<div class="topic"` and replace with color/delay
    boxes = re.split(r'(<div class="topic"\s+style="--accent:.*?>\s*<span class="badge"\s+style=".*?">)', grid_content)
    
    # Actually `re.split` with capture group returns interlaced list: text, match, text, match...
    # But wait, it's safer to use re.sub with a custom function.
    
    count = [0]
    palette_offset = hash(grid_content[:20]) % len(palettes) # give each layer a different starting color
    
    def replace_topic(m):
        # m.group(0) is like `<div class="topic" style="--accent:#AFA9EC"><span class="badge" style="background:var(--purple-f);color:var(--purple-t)">`
        full_match = m.group(0)
        
        # If it's already fluid-box, skip? The regex `class="topic"` won't match `class="topic fluid-box"` exactly.
        # But wait, my regex is `<div class="topic"` exact match, so `topic fluid-box` won't match. This naturally avoids Layer 2!
        
        c = count[0]
        count[0] += 1
        
        d = c * 1.5 
        pal = palettes[(palette_offset + c) % len(palettes)]
        
        return f'<div class="topic fluid-box" style="--accent:{pal["accent"]}; animation-delay: {d}s;"><span class="badge" style="background:{pal["f"]};color:{pal["t"]}">'

    # Pattern to match EXACTLY `class="topic"` to avoid modifying `class="topic fluid-box"` or `class="topic course-file"`
    pattern_to_replace = re.compile(r'<div class="topic"\s+style="--accent:[^"]+">\s*<span class="badge"\s+style="[^"]+">')
    new_grid_content = pattern_to_replace.sub(replace_topic, grid_content)
    
    return f'<div class="topic-grid">{new_grid_content}</div>'

new_html = grid_pattern.sub(process_grid, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Updated index.html topics")
