import os
import re

dir_path = "e:\\Git Repository\\LLM-Understanding"

html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for file in html_files:
    filepath = os.path.join(dir_path, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already injected to avoid duplicating
    if 'audio-narrator.js' in content:
        continue
        
    # Inject into head
    content = content.replace('</head>', '<script src="audio-narrator.js" defer></script>\n</head>')
    
    # Inject auto-play logic based on file type
    if file == 'index.html':
        # Hook into index.html `show(id)`
        content = content.replace('function show(id){', "function show(id){\n  if(window.Narrator) window.Narrator.play(id === 'overview' ? 'layer_overview' : 'layer_' + id);")
    else:
        # For course files, grab the number prefix `12-attention-mechanism.html` -> `12`
        match = re.match(r'^(\d+[a-z]?)-', file)
        if match:
            course_id = match.group(1)
            # Add play trigger to body
            play_script = f"\n<script>\nwindow.addEventListener('DOMContentLoaded', () => {{\n  setTimeout(() => window.Narrator?.play('course_{course_id}'), 500);\n}});\n</script>\n</body>"
            content = content.replace('</body>', play_script)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print(f"Successfully injected audio narrator logic into {len(html_files)} HTML files.")
