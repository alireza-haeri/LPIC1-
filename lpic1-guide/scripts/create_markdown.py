import json
import os
import re

# Load extracted content
with open("linux1st_full.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

output_dir = "content/linux1st"
os.makedirs(output_dir, exist_ok=True)

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

for article in articles:
    title = article["title"]
    content = article["content"]

    filename = slugify(title) + ".md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)

print(f"\n✅ Markdown files created at: {output_dir}")
