import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

grids = re.findall(r'<div class="topic-grid">(.*?)</div>', html, flags=re.DOTALL)
print(f"Total grids: {len(grids)}")

for i, grid in enumerate(grids):
    matches = re.findall(r'<div class="topic"\s*style="--accent:[^"]*">\s*<span class="badge"\s*style="[^"]*">', grid)
    print(f"Grid {i} matches: {len(matches)}")
