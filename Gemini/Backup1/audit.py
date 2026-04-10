import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("--- Checking Links to CSS/JS ---")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        has_css = "sub-clone-style.css" in content
        has_old_css = "alireza" in content.lower()
        if not has_css and not has_old_css and "<style" not in content:
            print(f"[MISSING CSS] {f}")
        if has_old_css:
            print(f"[OLD REF] {f} still contains 'alireza'")

print("\n--- Checking course file consistency in index.html ---")
with open("index.html", "r", encoding="utf-8") as file:
    content = file.read()
    links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>', content)
    for link in links:
        if link.endswith('.html'):
            if not os.path.exists(link):
                print(f"[BROKEN LINK] {link} in index.html does not exist!")
            else:
                print(f"[OK linked] {link}")
