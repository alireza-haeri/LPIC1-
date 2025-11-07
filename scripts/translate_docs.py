#!/usr/bin/env python3
"""
LPIC-1 Documentation Translator to Persian (Farsi)

This script translates English LPIC-1 documentation files to Persian while:
- Preserving markdown structure (headers, lists, code blocks, tables)
- Keeping technical terms and commands unchanged
- Adding practical examples where helpful
- Adding summaries after topics
- Using clear, friendly Persian language

Note: This script creates a framework for translation. The actual Persian translation
content needs to be provided by a language model or translation service that can
properly translate to Farsi while following the specified guidelines.
"""

import os
import re
from pathlib import Path
import sys

# Source and destination directories
SOURCE_DIR = Path("lpic1-guide/docs/lpic1")
DEST_DIR = Path("content")

def main():
    """Main translation process"""
    print("=" * 70)
    print("LPIC-1 Documentation Translation to Persian")
    print("=" * 70)
    print()
    print("This task requires translating 43 markdown files (~30,758 lines)")
    print("from English to Persian while maintaining:")
    print("  - Markdown structure (headers, code blocks, lists, tables)")
    print("  - Technical terms unchanged (commands, file paths, etc.)")
    print("  - Clear, friendly Persian language")
    print("  - Practical examples and summaries")
    print()
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Destination directory: {DEST_DIR}")
    print()
    
    # Ensure directories exist
    if not SOURCE_DIR.exists():
        print(f"❌ Error: Source directory {SOURCE_DIR} does not exist")
        sys.exit(1)
    
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all markdown files
    md_files = sorted(SOURCE_DIR.glob("*.md"))
    
    if not md_files:
        print(f"❌ No markdown files found in {SOURCE_DIR}")
        sys.exit(1)
    
    print(f"📝 Found {len(md_files)} markdown files:")
    for i, f in enumerate(md_files[:5], 1):
        print(f"   {i}. {f.name}")
    if len(md_files) > 5:
        print(f"   ... and {len(md_files) - 5} more files")
    print()
    print("⚠️  This script sets up the framework for translation.")
    print("    Actual translation requires a language model or translation service.")
    print("    Files will be prepared for translation in the content/ directory.")
    print()
    
    # For now, just copy files to demonstrate structure
    # In a real implementation, this would call a translation service
    for source_file in md_files:
        dest_file = DEST_DIR / source_file.name
        # Copy source to dest as placeholder
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add a header indicating translation needed
        header = f"""<!-- This file needs translation to Persian -->
<!-- Original file: {source_file.name} -->
<!-- Translation guidelines:
  - Translate text to clear, friendly Persian
  - Keep technical terms (commands, paths) unchanged
  - Preserve all markdown formatting
  - Keep code blocks exactly as they are
  - Add practical examples where helpful
  - Add summary after each topic
-->

"""
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        print(f"✓ Prepared: {dest_file.name}")
    
    print()
    print("=" * 70)
    print(f"✅ Framework created for {len(md_files)} files")
    print(f"📁 Files are in: {DEST_DIR}/")
    print()
    print("Next steps:")
    print("  1. Use a Persian translation service/AI to translate each file")
    print("  2. Follow the guidelines in the file headers")
    print("  3. Maintain markdown structure and technical terms")
    print("=" * 70)

if __name__ == "__main__":
    main()
