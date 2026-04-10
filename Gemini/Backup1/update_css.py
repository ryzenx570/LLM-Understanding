import os
import re

files = [
    "02-pretraining-pipeline.html",
    "03-rlhf-reasoning.html",
    "04-vision-speech.html",
    "05-embedding-deepdive.html",
    "06-cbow-skipgram.html",
    "07-architecture-families.html",
    "08-llm-inference.html",
    "09-trl-grpo.html",
    "10-softmax-crossentropy.html",
    "11-next-token-emergence.html"
]

dark_vars = """
:root{
  --bg:#1e1e1c;--bg2:#252522;--bg3:#2c2c29;--text:#e8e6de;--text2:#a8a69e;--text3:#6e6c66;
  --border:rgba(255,255,255,0.1);--radius:10px;--radius-sm:6px;
  --amber-f:#412402;--amber-s:#BA7517;--amber-t:#FAC775;
  --purple-f:#26215C;--purple-s:#7F77DD;--purple-t:#CECBF6;
  --teal-f:#04342C;--teal-s:#1D9E75;--teal-t:#9FE1CB;
  --green-f:#173404;--green-s:#639922;--green-t:#C0DD97;
  --coral-f:#4A1B0C;--coral-s:#D85A30;--coral-t:#F5C4B3;
  --red-f:#501313;--red-s:#E24B4A;--red-t:#F7C1C1;
  --blue-f:#042C53;--blue-s:#378ADD;--blue-t:#B5D4F4;
  --pink-f:#4B1528;--pink-s:#D4537E;--pink-t:#F4C0D1;
}
"""

new_tab_css = """.tab-bar{display:flex;background:var(--bg3);border-bottom:1px solid var(--border);overflow-x:auto;padding:10px 20px 0;}
.tab{padding:12px 20px;font-size:14px;font-weight:600;cursor:pointer;border:1px solid transparent;border-bottom:none;background:transparent;color:var(--text2);transition:all .2s;white-space:nowrap;border-radius:var(--radius-sm) var(--radius-sm) 0 0;margin-right:5px;}
.tab:hover{color:var(--text);background:var(--bg2);}
.tab.on{color:var(--text);background:var(--bg);border-color:var(--border);}
.panel{display:none;padding:30px;max-width:900px;margin:0 auto}
.panel.on{display:flex;flex-direction:column;gap:20px;}
.card{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:0px;box-shadow:0 4px 20px rgba(0,0,0,0.15);}
.card-title{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--text);}
.card-body{font-size:14px;color:var(--text2);line-height:1.7;}
"""

for f in files:
    if not os.path.exists(f): 
        print(f"Skipping {f}, not found.")
        continue
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 1. Replace variable blocks with the dark_vars only
    pattern_vars = r':root\s*\{.*?\}(?:\s*@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{.*?\n\s*\}\s*\})?'
    content = re.sub(pattern_vars, dark_vars.strip(), content, count=1, flags=re.DOTALL)
    
    # 2. Replace tab and card styles
    chunk_pattern = r'\.tab-bar\s*\{.*?\.card-body\s*\{[^}]*\}'
    content = re.sub(chunk_pattern, new_tab_css.strip(), content, count=1, flags=re.DOTALL)
    
    with open(f, "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"Updated {f}")
