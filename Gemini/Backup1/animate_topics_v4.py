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

parts = html.split('<div class="topic"')

new_parts = [parts[0]]
valid_count = 0

for part in parts[1:]:
    # In earlier scripts, I modified the first items to `<div class="topic fluid-box"` so they won't 
    # start with ` style="--accent:` when splitting by `<div class="topic"`. 
    # Let's handle both ` style="--accent:` and ` fluid-box" style="--accent:` uniformly!
    
    # Let's reconstruct the part so we can parse from the root of the "topic" tag contents.
    if part.startswith(' fluid-box"'):
        content = part.split(' fluid-box"', 1)[1]
    else:
        content = part
        
    if content.startswith(' style="--accent:'):
        # We want to replace the style="--accent..." and badge for EVERYTHING
        
        end_div_idx = content.find('>')
        badge_start_idx = content.find('<span class="badge"')
        
        if badge_start_idx != -1:
            badge_end_idx = content.find('>', badge_start_idx)
            
            pal = palettes[valid_count % len(palettes)]
            delay = (valid_count % 4) * 1.5
            
            new_div = f' fluid-box" style="--accent:{pal["accent"]}; animation-delay: {delay}s;"'
            badge_str = f'<span class="badge" style="background:{pal["f"]};color:{pal["t"]}">'
            
            new_part = new_div + content[end_div_idx:badge_start_idx] + badge_str + content[badge_end_idx+1:]
            new_parts.append(new_part)
            valid_count += 1
            continue

    # If it falls through, just append it untouched
    # We must prepend the exact part prefix depending on whether it started with fluid-box
    if part.startswith(' fluid-box"'):
        new_parts.append(' fluid-box"' + content)
    else:
        new_parts.append(part)

final_html = '<div class="topic"'.join(new_parts)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Batch update complete: Updated {valid_count} topics globally!")
