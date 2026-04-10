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

def process_grid(match):
    grid_content = match.group(1)
    
    # We will split by <div class="topic" and re-assemble.
    parts = grid_content.split('<div class="topic"')
    
    new_parts = [parts[0]] # the leading text before the first <div class="topic"
    
    palette_offset = hash(grid_content[:20]) % len(palettes)
    valid_count = 0
    
    for part in parts[1:]:
        # if the part starts immediately with ` fluid-box"` or something else, 
        # it might have already been processed or it's a different class.
        # Original: `<div class="topic" style="--accent:...">` -> part starts with ` style="--accent:...">`
        
        if part.startswith(' style="--accent:'):
            # This is a match!
            # We need to replace `--accent:XYZ"` with our new accent and animation config.
            # And modify the badge color inside the part.
            
            # Find the end of the div tag
            end_div_idx = part.find('>')
            
            # Find the span badge
            badge_start_idx = part.find('<span class="badge"')
            if badge_start_idx != -1:
                badge_end_idx = part.find('>', badge_start_idx)
                
                pal = palettes[(palette_offset + valid_count) % len(palettes)]
                delay = valid_count * 1.5
                
                # Replace the div tag portion
                # Note: `part` starts with ` style="--accent:`
                # We want to change the class to `topic fluid-box` but the split consumed `<div class="topic"`.
                new_div = f' fluid-box" style="--accent:{pal["accent"]}; animation-delay: {delay}s;"'
                
                # Now reconstruct the part string.
                # Find the badge style
                # Original badge: `<span class="badge" style="background:var(--purple-f);color:var(--purple-t)">`
                badge_str = f'<span class="badge" style="background:{pal["f"]};color:{pal["t"]}">'
                
                # Slicing reconstruction
                new_part = new_div + part[end_div_idx:badge_start_idx] + badge_str + part[badge_end_idx+1:]
                
                new_parts.append(new_part)
                valid_count += 1
            else:
                new_parts.append('"' + part) # Re-add the quote since split consumed `<div class="topic"` and part started with ` ` or `"`
        else:
            # Maybe it was already processed: `<div class="topic fluid-box"` -> part starts with ` fluid-box"`
            # If so, just reconstruct it.
            # Wait, if we split by `<div class="topic"`, the part will start with ` fluid-box" style="...`
            if part.startswith(' fluid-box"'):
                # it's already fluid-box, but we want to recolor them to match the new rotating palette just in case, 
                # OR just leave it alone. The prompt says "that don't have your changes", so leaving Layer 2 alone is fine.
                new_parts.append(part)
            else:
                new_parts.append(part)
            
    return '<div class="topic-grid">' + '<div class="topic"'.join(new_parts) + '</div>'

grid_pattern = re.compile(r'<div class="topic-grid">(.*?)</div>', re.DOTALL)
new_html = grid_pattern.sub(process_grid, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Batch update complete")
