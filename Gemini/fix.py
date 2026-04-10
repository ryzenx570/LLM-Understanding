with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<div class="topic" fluid-box"', '<div class="topic fluid-box"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Fixed quotes!")
