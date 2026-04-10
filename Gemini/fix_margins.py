import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any margin-bottom or margin-top settings in the inline style of course-file links
# We will just standardize the style string for .course-file

def standardize_margin(match):
    full_string = match.group(0)
    # Remove existing margin-top and margin-bottom
    full_string = re.sub(r'margin-top:\s*\d+px;?', '', full_string)
    full_string = re.sub(r'margin-bottom:\s*\d+px;?', '', full_string)
    # Inject standard margin: 32px top, 15px bottom
    # We can inject it right before the closing quote of the style attribute
    # Since we don't know exactly where, we just append it before the >
    # Actually, the easiest is to replace `style="` with `style="margin-top: 32px; margin-bottom: 24px; `
    # But some might not have style="? All of them have style="--accent..."
    
    # Let's do a strict replacement
    return full_string.replace('style="', 'style="margin-top: 32px; margin-bottom: 24px; ')

# Regex to match course-file opening tags
html = re.sub(r'<a class="topic course-file"[^>]+>', standardize_margin, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Standardized course-file spacing!")
