import os
import re

dir_path = "."
old_word_lower = "alireza"
new_word_lower = "sub-clone"
old_word_capital = "Alireza"
new_word_capital = "Sub-clone"

# First, replace inside files
for root, dirs, files in os.walk(dir_path):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.css', '.md')):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace
            new_content = content.replace(old_word_lower, new_word_lower)
            new_content = new_content.replace(old_word_capital, new_word_capital)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated content in {file}")

# Second, rename files
for root, dirs, files in os.walk(dir_path):
    if '.git' in root:
        continue
    for file in files:
        if old_word_lower in file.lower():
            old_name = file
            new_name = re.sub(old_word_lower, new_word_lower, file, flags=re.IGNORECASE)
            
            # Make sure we don't mess up case completely, but 'alireza' is mostly lower in filenames
            os.rename(os.path.join(root, old_name), os.path.join(root, new_name))
            print(f"Renamed {old_name} -> {new_name}")

print("Replacement and renaming complete!")
