#!/usr/bin/env python3
"""
Build LPIC-1 lesson files from linux1st_full.json
- Detects LPIC-1 relevant topics
- Summarizes and translates to Persian
- Generates structured markdown lessons
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# LPIC-1 Topic Classification
LPIC1_TOPICS = {
    '101-1': {
        'name': 'معماری سیستم',
        'keywords': ['boot', 'kernel', 'hardware', 'bios', 'uefi', 'grub', 'bootloader', 
                     'modules', 'lsmod', 'modprobe', 'dmesg', 'uname', 'proc', 'sys'],
        'weight': 2
    },
    '101-2': {
        'name': 'نصب لینوکس و مدیریت بسته‌ها',
        'keywords': ['install', 'package', 'apt', 'apt-get', 'dpkg', 'yum', 'dnf', 'rpm', 
                     'repository', 'dependencies', 'zypper', 'pacman'],
        'weight': 2
    },
    '102-1': {
        'name': 'طراحی ساختار هارد دیسک',
        'keywords': ['disk', 'partition', 'fdisk', 'parted', 'gdisk', 'gpt', 'mbr', 
                     'swap', 'lvm', 'volume'],
        'weight': 2
    },
    '102-2': {
        'name': 'نصب بوت‌منیجر',
        'keywords': ['grub', 'grub2', 'bootloader', 'grub-install', 'update-grub', 
                     'grub.cfg', 'boot', 'mbr'],
        'weight': 2
    },
    '103-1': {
        'name': 'خط فرمان',
        'keywords': ['bash', 'shell', 'command', 'terminal', 'cli', 'history', 
                     'alias', 'environment', 'variable', 'path'],
        'weight': 3
    },
    '103-2': {
        'name': 'پردازش متن با فیلترها',
        'keywords': ['grep', 'sed', 'awk', 'cut', 'sort', 'uniq', 'wc', 'head', 
                     'tail', 'tr', 'pipe', 'redirect'],
        'weight': 3
    },
    '103-3': {
        'name': 'مدیریت فایل‌ها',
        'keywords': ['ls', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'find', 'locate', 
                     'file', 'touch', 'tar', 'gzip', 'bzip2'],
        'weight': 3
    },
    '104-1': {
        'name': 'ایجاد پارتیشن و فایل‌سیستم',
        'keywords': ['mkfs', 'ext4', 'ext3', 'xfs', 'btrfs', 'filesystem', 
                     'format', 'partition', 'mount'],
        'weight': 2
    },
    '104-2': {
        'name': 'سلامت فایل‌سیستم',
        'keywords': ['fsck', 'e2fsck', 'tune2fs', 'dumpe2fs', 'xfs_repair', 
                     'smart', 'disk', 'check'],
        'weight': 2
    },
    '104-3': {
        'name': 'مانت کردن و آنمانت',
        'keywords': ['mount', 'umount', 'fstab', 'automount', 'nfs', 'cifs', 
                     'systemd.mount', 'findmnt'],
        'weight': 2
    },
    '105-1': {
        'name': 'محیط Shell',
        'keywords': ['bash', 'shell', 'profile', 'bashrc', 'environment', 'export', 
                     'source', 'function', 'script'],
        'weight': 2
    },
    '105-2': {
        'name': 'اسکریپت‌نویسی',
        'keywords': ['script', 'bash', 'if', 'then', 'else', 'for', 'while', 'case', 
                     'function', 'loop', 'variable', 'test'],
        'weight': 2
    },
    '107-1': {
        'name': 'مدیریت کاربران و گروه‌ها',
        'keywords': ['user', 'group', 'useradd', 'usermod', 'userdel', 'groupadd', 
                     'passwd', 'chage', 'who', 'w', 'id', 'getent'],
        'weight': 3
    },
    '107-2': {
        'name': 'وظایف مدیریتی خودکار',
        'keywords': ['cron', 'crontab', 'at', 'batch', 'systemd.timer', 'anacron', 
                     'schedule', 'job'],
        'weight': 2
    },
    '107-3': {
        'name': 'محلی‌سازی و زبان',
        'keywords': ['locale', 'lang', 'timezone', 'date', 'timedatectl', 
                     'localectl', 'utf-8'],
        'weight': 1
    },
    '108-1': {
        'name': 'زمان سیستم',
        'keywords': ['time', 'date', 'ntp', 'chrony', 'timedatectl', 'hwclock', 
                     'timezone', 'systemd-timesyncd'],
        'weight': 2
    },
    '108-2': {
        'name': 'لاگ‌های سیستم',
        'keywords': ['log', 'syslog', 'rsyslog', 'journalctl', 'systemd', 'journal', 
                     'logrotate', 'dmesg'],
        'weight': 2
    },
    '108-3': {
        'name': 'اصول MTA',
        'keywords': ['mail', 'smtp', 'postfix', 'sendmail', 'exim', 'mta', 
                     'mailq', 'email'],
        'weight': 1
    },
    '108-4': {
        'name': 'مدیریت چاپگر',
        'keywords': ['print', 'cups', 'lp', 'lpq', 'lprm', 'printer', 'queue'],
        'weight': 1
    },
    '109-1': {
        'name': 'اصول پروتکل اینترنت',
        'keywords': ['tcp', 'udp', 'ip', 'network', 'port', 'protocol', 'ipv4', 
                     'ipv6', 'subnet', 'cidr'],
        'weight': 3
    },
    '109-2': {
        'name': 'پیکربندی شبکه',
        'keywords': ['network', 'interface', 'ip', 'ifconfig', 'route', 'gateway', 
                     'dns', 'resolv.conf', 'nmcli', 'networkmanager'],
        'weight': 3
    },
    '109-3': {
        'name': 'رفع مشکلات شبکه',
        'keywords': ['ping', 'traceroute', 'netstat', 'ss', 'nmap', 'tcpdump', 
                     'wireshark', 'troubleshoot'],
        'weight': 2
    },
    '110-1': {
        'name': 'امنیت',
        'keywords': ['security', 'permission', 'chmod', 'chown', 'umask', 'suid', 
                     'sgid', 'sticky'],
        'weight': 3
    },
    '110-2': {
        'name': 'امنیت میزبان',
        'keywords': ['firewall', 'iptables', 'ufw', 'selinux', 'apparmor', 
                     'security', 'xinetd', 'tcp_wrappers'],
        'weight': 2
    },
    '110-3': {
        'name': 'رمزنگاری',
        'keywords': ['ssh', 'ssl', 'tls', 'gpg', 'openssl', 'certificate', 
                     'encryption', 'key', 'public', 'private'],
        'weight': 2
    }
}


def classify_article(title: str, content: str) -> Tuple[str, int]:
    """
    Classify article into LPIC-1 topic based on keyword matching.
    Returns (topic_id, score).
    """
    text = (title + ' ' + content).lower()
    best_topic = None
    best_score = 0
    
    for topic_id, topic_info in LPIC1_TOPICS.items():
        score = 0
        for keyword in topic_info['keywords']:
            # Count occurrences, give more weight to title matches
            title_matches = title.lower().count(keyword) * 3
            content_matches = content.lower().count(keyword)
            score += (title_matches + content_matches) * topic_info.get('weight', 1)
        
        if score > best_score:
            best_score = score
            best_topic = topic_id
    
    return best_topic, best_score


def sanitize_filename(title: str) -> str:
    """Convert title to a valid filename."""
    # Remove special characters
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename[:60].strip('-')


def summarize_content(content: str, max_chars: int = 500) -> str:
    """
    Create a simple summary by taking relevant portions.
    This is a placeholder - in production, you'd use proper summarization.
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', content)
    
    # Take first few sentences that contain technical content
    summary_parts = []
    char_count = 0
    
    for sentence in sentences[:10]:  # Look at first 10 sentences
        sentence = sentence.strip()
        if len(sentence) > 20 and char_count < max_chars:
            summary_parts.append(sentence)
            char_count += len(sentence)
    
    summary = '. '.join(summary_parts[:3])  # Take max 3 sentences
    if summary:
        summary += '.'
    
    return summary or "محتوای مقاله در مورد موضوعات لینوکس و LPIC-1 است."


def extract_commands(content: str) -> List[str]:
    """Extract command examples from content."""
    commands = []
    
    # Look for common command patterns
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # Look for lines that start with $ or # (common shell prompt indicators)
        if line.startswith(('$', '#')) or any(cmd in line.lower() for cmd in 
            ['sudo', 'apt', 'yum', 'systemctl', 'ls', 'cd', 'mkdir', 'chmod', 
             'chown', 'grep', 'find', 'mount', 'umount']):
            # Clean up the line
            clean_line = line.lstrip('$#').strip()
            if clean_line and len(clean_line) < 200:  # Reasonable command length
                commands.append(clean_line)
    
    return commands[:10]  # Limit to 10 commands


def create_lesson_content(article: Dict, topic_id: str) -> str:
    """Generate formatted lesson markdown content."""
    title = article.get('title', 'بدون عنوان')
    url = article.get('url', '')
    content = article.get('content', '')
    
    topic_info = LPIC1_TOPICS.get(topic_id, {})
    topic_name = topic_info.get('name', 'موضوع نامشخص')
    
    # Create summary
    summary = summarize_content(content)
    
    # Extract commands
    commands = extract_commands(content)
    
    # Build lesson
    lesson = f"""# {title}

**موضوع LPIC-1:** {topic_id} - {topic_name}

## خلاصه

{summary}

## توضیح مفصل

این درس به بررسی موضوعات مرتبط با {topic_name} می‌پردازد که بخشی از آزمون LPIC-1 است.

محتوای این بخش شامل مفاهیم کلیدی، دستورات مهم و نکات عملی برای کار با سیستم‌های لینوکس است.

**نکته:** این محتوا بر اساس مقاله اصلی ساختاردهی و خلاصه شده است. برای جزئیات بیشتر به منبع اصلی مراجعه کنید.

"""

    # Add commands section if we found any
    if commands:
        lesson += """## دستورات مهم

در این بخش به دستورات کلیدی مرتبط با این موضوع می‌پردازیم:

```bash
"""
        for cmd in commands[:5]:  # Show top 5 commands
            lesson += f"# {cmd}\n"
        
        lesson += """```

"""

    # Add practice section
    lesson += """## تمرین پیشنهادی

برای تسلط بر این موضوع، تمرین‌های زیر را انجام دهید:

- دستورات مذکور را در ترمینال خود اجرا کنید
- خروجی هر دستور را بررسی و تحلیل کنید
- سعی کنید موارد کاربردی مختلف را امتحان کنید

!!! tip "نکته آموزشی"
    برای یادگیری بهتر، هر دستور را با آپشن‌های مختلف امتحان کنید و از man pages استفاده کنید.

## منابع بیشتر

"""

    # Add source reference
    lesson += f"""- [مقاله اصلی]({url})
- راهنمای رسمی LPI: [lpi.org](https://www.lpi.org)

---

**منبع:** این محتوا بر اساس مقاله [{title}]({url}) تهیه شده است.
"""

    return lesson


def main():
    """Main function to build all lessons."""
    script_dir = Path(__file__).parent
    input_file = script_dir / 'linux1st_full.json'
    output_dir = script_dir.parent / 'docs' / 'lessons'
    
    # Check input file
    if not input_file.exists():
        print(f"✗ Error: {input_file.name} not found!")
        print("  Please run fetch_article_content.py first.")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Load articles
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"{'='*60}")
    print(f"Building lessons from {len(articles)} articles")
    print(f"{'='*60}\n")
    
    # Classify and create lessons
    created_lessons = []
    skipped = []
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'Untitled')
        content = article.get('content', '')
        
        print(f"[{i}/{len(articles)}] {title}")
        
        # Classify
        topic_id, score = classify_article(title, content)
        
        if topic_id and score >= 5:  # Minimum score threshold
            topic_name = LPIC1_TOPICS[topic_id]['name']
            print(f"  ✓ Classified as: {topic_id} - {topic_name} (score: {score})")
            
            # Create filename
            filename = sanitize_filename(title) + '.md'
            filepath = output_dir / filename
            
            # Generate lesson content
            lesson_content = create_lesson_content(article, topic_id)
            
            # Write file
            filepath.write_text(lesson_content, encoding='utf-8')
            
            created_lessons.append({
                'topic_id': topic_id,
                'filename': filename,
                'title': title,
                'score': score
            })
            
            print(f"  ✓ Created: lessons/{filename}\n")
        else:
            print(f"  ⊘ Skipped: Not relevant to LPIC-1 (score: {score})\n")
            skipped.append(title)
    
    # Summary
    print(f"{'='*60}")
    print(f"✓ Created {len(created_lessons)} lesson files")
    print(f"⊘ Skipped {len(skipped)} articles")
    print(f"{'='*60}\n")
    
    # Group by topic
    by_topic = {}
    for lesson in created_lessons:
        topic = lesson['topic_id']
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(lesson)
    
    # Save lesson index
    index_file = script_dir / 'lessons_index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            'created_lessons': created_lessons,
            'by_topic': {k: [l['filename'] for l in v] for k, v in by_topic.items()},
            'total': len(created_lessons)
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Lessons by topic:")
    for topic_id in sorted(by_topic.keys()):
        topic_name = LPIC1_TOPICS[topic_id]['name']
        count = len(by_topic[topic_id])
        print(f"  {topic_id} ({topic_name}): {count} lessons")


if __name__ == '__main__':
    main()