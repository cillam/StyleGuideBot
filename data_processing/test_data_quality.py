import json
import numpy as np

with open('../data/wikipedia_mos_raw.json', 'r') as file:
    data = json.load(file)


print("Total Section Count")
print(f"Number of sections stated in metadata: {data['metadata']['total_sections']}")
print(f"Total number of sections: {len(data['sections'])}")


print("\nCount by Section")
sections = data['sections']
section_counts = {}
for level in range(1,5):
    matching_items = [item for item in sections if item["level"] == level]
    section_counts[f"Level {level}"] = len(matching_items)
print(section_counts)


print("\nContent Length")
content_lengths = [len(item['content']) for item in sections]
print(f"Content min: {min(content_lengths)}")
print(f"Content max: {max(content_lengths)}")
print(f"Content average length: {np.mean(content_lengths)}")
print(f"Number of sections with no content: {content_lengths.count(0)}")


print("\nShortcut Check")
shortcuts = [item['shortcuts'] for item in sections]
shortcut_lengths = [len(item['shortcuts']) for item in sections]
print(f"Number of sections with no shortcuts: {shortcut_lengths.count(0)}")
for shortcut in shortcuts[0:5]:
    if len(shortcut) != 0:
        print(f"Example: {shortcut}")


print("\n" + "="*80)
print("TOPIC HIERARCHY (excluding Introduction)")
print("="*80)

# Indented structure
print("\nIndented Structure:")

for section in sections[1:]:  # Skip Introduction
    level = section['level']
    title = section['title']
    
    if level == 2:
        print(f"\n• {title}")
    elif level == 3:
        print(f"  - {title}")
    elif level == 4:
        print(f"    · {title}")

# Tree visualization
print("\n" + "="*80)
print("TREE VISUALIZATION (excluding Introduction)")
print("="*80)

def print_tree(sections, start_idx=0):
    """Print tree structure with connecting lines, handling all 4 levels"""
    
    i = start_idx
    while i < len(sections):
        section = sections[i]
        level = section['level']
        title = section['title']
        
        if level == 2:
            print(f"\n{title}")
            i += 1
        elif level == 3:
            # Look ahead to see if this is the last level 3 under current level 2
            is_last_l3 = True
            for j in range(i + 1, len(sections)):
                if sections[j]['level'] == 2:
                    break
                if sections[j]['level'] == 3:
                    is_last_l3 = False
                    break
            
            connector = "└── " if is_last_l3 else "├── "
            print(f"  {connector}{title}")
            i += 1
        elif level == 4:
            # Look ahead to see if this is the last level 4 under current level 3
            is_last_l4 = True
            for j in range(i + 1, len(sections)):
                if sections[j]['level'] <= 3:
                    break
                if sections[j]['level'] == 4:
                    is_last_l4 = False
                    break
            
            connector = "└── " if is_last_l4 else "├── "
            
            # Determine prefix based on parent level 3's position
            # Check if parent level 3 was last
            parent_was_last = True
            for j in range(i, len(sections)):
                if sections[j]['level'] == 2:
                    break
                if sections[j]['level'] == 3:
                    parent_was_last = False
                    break
            
            prefix = "      " if parent_was_last else "  │   "
            print(f"{prefix}{connector}{title}")
            i += 1
        else:
            i += 1

print("\nFull Document Structure:")
print_tree(sections, start_idx=1)  # Start at index 1 to skip Introduction

