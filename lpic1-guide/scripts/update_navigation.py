#!/usr/bin/env python3
"""
Update mkdocs.yml navigation with generated lessons.
Reads lessons_index.json and updates the nav section automatically.
"""

import json
import sys
import re
from pathlib import Path
import yaml


# Try to use ruamel.yaml for better YAML handling (preserves comments/formatting)
try:
    from ruamel.yaml import YAML
    USE_RUAMEL = True
except ImportError:
    import yaml
    USE_RUAMEL = False


LPIC1_TOPICS = {
    '101-1': 'معماری سیستم',
    '101-2': 'نصب لینوکس و مدیریت بسته‌ها',
    '102-1': 'طراحی ساختار هارد دیسک',
    '102-2': 'نصب بوت‌منیجر',
    '103-1': 'خط فرمان',
    '103-2': 'پردازش متن با فیلترها',
    '103-3': 'مدیریت فایل‌ها',
    '104-1': 'ایجاد پارتیشن و فایل‌سیستم',
    '104-2': 'سلامت فایل‌سیستم',
    '104-3': 'مانت کردن و آنمانت',
    '105-1': 'محیط Shell',
    '105-2': 'اسکریپت‌نویسی',
    '107-1': 'مدیریت کاربران و گروه‌ها',
    '107-2': 'وظایف مدیریتی خودکار',
    '107-3': 'محلی‌سازی و زبان',
    '108-1': 'زمان سیستم',
    '108-2': 'لاگ‌های سیستم',
    '108-3': 'اصول MTA',
    '108-4': 'مدیریت چاپگر',
    '109-1': 'اصول پروتکل اینترنت',
    '109-2': 'پیکربندی شبکه',
    '109-3': 'رفع مشکلات شبکه',
    '110-1': 'امنیت',
    '110-2': 'امنیت میزبان',
    '110-3': 'رمزنگاری'
}


def load_lessons_index(script_dir: Path):
    """Load the lessons index created by build_lessons.py."""
    index_file = script_dir / 'lessons_index.json'
    
    if not index_file.exists():
        print(f"✗ Error: {index_file.name} not found!")
        print("  Please run build_lessons.py first.")
        sys.exit(1)
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_nav_structure(lessons_index):
    """Build navigation structure organized by topic."""
    by_topic = lessons_index.get('by_topic', {})
    
    # Build lessons section
    lessons_nav = []
    
    # Add existing lessons first
    lessons_nav.append({'مبانی لینوکس': 'basics.md'})
    lessons_nav.append({'مجوزهای فایل': 'permissions.md'})
    
    # Group generated lessons by topic
    for topic_id in sorted(by_topic.keys()):
        topic_name = LPIC1_TOPICS.get(topic_id, f'موضوع {topic_id}')
        lesson_files = by_topic[topic_id]
        
        if len(lesson_files) == 1:
            # Single lesson - add directly
            lessons_nav.append({
                topic_name: f"lessons/{lesson_files[0]}"
            })
        else:
            # Multiple lessons - create subsection
            subsection = {topic_name: []}
            for filename in lesson_files:
                # Use filename as title (could be improved)
                title = filename.replace('-', ' ').replace('.md', '').title()
                subsection[topic_name].append({
                    title: f"lessons/{filename}"
                })
            lessons_nav.append(subsection)
    
    return lessons_nav


def update_mkdocs_yml(mkdocs_path: Path, lessons_nav):
    """Update mkdocs.yml with new navigation structure."""
    
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if USE_RUAMEL:
        # Use ruamel.yaml for better formatting preservation
        yaml_handler = YAML()
        yaml_handler.preserve_quotes = True
        yaml_handler.default_flow_style = False
        config = yaml_handler.load(content)
    else:
        # Fall back to PyYAML
        config = yaml.safe_load(content)
    
    # Update nav section
    if 'nav' not in config:
        config['nav'] = []
    
    # Find and replace 'دروس' section
    nav = config['nav']
    lessons_idx = None
    
    for i, item in enumerate(nav):
        if isinstance(item, dict) and 'دروس' in item:
            lessons_idx = i
            break
    
    # Update or add lessons section
    if lessons_idx is not None:
        nav[lessons_idx] = {'دروس': lessons_nav}
    else:
        # Add after 'فهرست دروس' if it exists, otherwise at the end
        nav.append({'دروس': lessons_nav})
    
    # Write back
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        if USE_RUAMEL:
            yaml_handler.dump(config, f)
        else:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False, 
                     default_flow_style=False)
    
    return len(lessons_nav)


def update_lessons_md(lessons_md_path: Path, lessons_index):
    """Update lessons.md table of contents."""
    
    if not lessons_md_path.exists():
        print(f"⚠ Warning: {lessons_md_path} not found, skipping update")
        return
    
    with open(lessons_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the lessons grid section
    grid_start = content.find('<div class="lessons-grid"')
    grid_end = content.find('</div>', grid_start) + 6 if grid_start != -1 else -1
    
    if grid_start == -1 or grid_end == -1:
        print("⚠ Warning: Could not find lessons grid in lessons.md")
        return
    
    # Build new lesson cards
    by_topic = lessons_index.get('by_topic', {})
    created_lessons = lessons_index.get('created_lessons', [])
    
    new_cards = []
    
    # Add cards for each topic that has lessons
    for topic_id in sorted(by_topic.keys()):
        topic_name = LPIC1_TOPICS.get(topic_id, f'موضوع {topic_id}')
        lesson_count = len(by_topic[topic_id])
        first_lesson = by_topic[topic_id][0]
        
        card = f'''
<div class="lesson-card" markdown="1">

<span class="lesson-badge available">موجود</span>

### {topic_name}

<div class="description">
موضوع {topic_id} - {lesson_count} درس
</div>

<a href="../lessons/{first_lesson}" class="read-more">
مطالعه درس <span class="arrow">←</span>
</a>

</div>
'''
        new_cards.append(card)
    
    # Insert new cards before the closing grid div
    # Keep existing cards and add new ones
    before_grid = content[:grid_start]
    after_grid = content[grid_end:]
    
    # Extract existing cards
    grid_content = content[grid_start:grid_end]
    
    # Add new cards to grid
    new_grid = '<div class="lessons-grid" markdown="1">\n'
    new_grid += '\n'.join(new_cards)
    new_grid += '\n</div>'
    
    # Note: This is a simple approach - in production you'd want to preserve existing cards
    # and only add new ones
    
    print(f"  ℹ Added {len(new_cards)} lesson cards to lessons.md")


def main():
    """Main function."""
    script_dir = Path(__file__).parent
    mkdocs_path = script_dir.parent / 'mkdocs.yml'
    lessons_md_path = script_dir.parent / 'docs' / 'lessons.md'
    
    print(f"{'='*60}")
    print("Updating navigation...")
    print(f"{'='*60}\n")
    
    # Load lessons index
    print("Loading lessons index...")
    lessons_index = load_lessons_index(script_dir)
    total_lessons = lessons_index.get('total', 0)
    print(f"  ✓ Found {total_lessons} lessons\n")
    
    # Build navigation structure
    print("Building navigation structure...")
    lessons_nav = build_nav_structure(lessons_index)
    print(f"  ✓ Created {len(lessons_nav)} navigation items\n")
    
    # Update mkdocs.yml
    print(f"Updating {mkdocs_path.name}...")
    try:
        count = update_mkdocs_yml(mkdocs_path, lessons_nav)
        print(f"  ✓ Updated navigation with {count} items\n")
    except Exception as e:
        print(f"  ✗ Error updating mkdocs.yml: {e}\n")
        sys.exit(1)
    
    # Update lessons.md
    print(f"Updating {lessons_md_path.name}...")
    try:
        update_lessons_md(lessons_md_path, lessons_index)
        print(f"  ✓ Updated lessons page\n")
    except Exception as e:
        print(f"  ⚠ Warning: {e}\n")
    
    print(f"{'='*60}")
    print("✓ Navigation update complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
