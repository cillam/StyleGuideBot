import json
import numpy as np
import datetime


# Create metadata
def add_metadata(source, chunks_num):
    return {
        "source": source,
        "chunked_at": datetime.datetime.now().isoformat(),
        "total_chunks": chunks_num
    }


# Find parent heading for levels >= 3
def find_parent(section_list, level):
    if level > 2:
        parent_lvl = level - 1
        for section in reversed(section_list):
            if section["level"] == parent_lvl:
                return section['title']
    else:
        return ""


# Chunk the sections list
def get_chunks(data):
    sections = data["sections"]
    chunk_lst = []
    for section in sections:
        content = section["content"]
        index = sections.index(section)
        level = section["level"]
        if len(content) != 0:
            chunk = {
                "content": content,
                "metadata": {
                    "title": section["title"],
                    "level": level,
                    "parent": find_parent(sections[:index], level), 
                    "shortcuts": section["shortcuts"]
                }
            }
            chunk_lst.append(chunk)
    return chunk_lst


# Save the JSON file
def make_json(metadata, chunks):
    chunked_data = {
        "metadata": metadata,
        "chunks": chunks
    }
    filename = "./data/chunked_mos.json"
    try:
        with open(filename, 'w') as json_file:
            json.dump(chunked_data, json_file, indent=4) 
        return f"JSON data successfully written to {filename}"
    except Exception as e:
        return f"\n❌ Failed to save data: {e}"


if __name__ == "__main__":
    try:
        # Load data
        with open('./data/wikipedia_mos_raw.json', 'r') as file:
            style_guide = json.load(file)

        # Get chunks
        chunk_list = get_chunks(style_guide)

        # Save metadata
        style_guide_metadata = add_metadata(style_guide["metadata"]["source"], len(chunk_list))

        # Save JSON file
        print(make_json(style_guide_metadata, chunk_list))

    except Exception as e:
        print(f"\n❌ Failed to load data: {e}")
        exit(1)