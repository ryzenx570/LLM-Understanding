with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
grid_pattern = re.compile(r'<div class="topic-grid">(.*?)</div>', re.DOTALL)
grids = grid_pattern.findall(html)

print("GRID 1 START:")
print(grids[1][:100])
print("------------")
parts = grids[1].split('<div class="topic"')
print(repr(parts[1][:50]))
