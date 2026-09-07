#!/usr/bin/env python3
"""
Generate Jekyll _talks markdown files from JSON event data.
Reads events from _events/*.json and creates corresponding .md files in _talks/
"""

import json
import os
import glob
from datetime import datetime

# Map room names to our room collection
ROOM_MAP = {
    "Boardroom": "Room A",
    "Main Atrium": "Room A",
    "Main Hall": "Room A",
    "Lecture Theatre": "Room A",
    "Seminar Room 2": "Room B",
    "Cinema": "Room C",
    "Gallery 1": "Room A",
    "The Crown Pub": "Room B",
    "null": "Room A",
    None: "Room A"
}

# Map categories to tags
CATEGORY_TAGS = {
    "academic": ["academic", "panel"],
    "workshop": ["workshop"],
    "keynote": ["keynote"],
    "meeting": ["meeting"],
    "social": ["social"],
    "film": ["film", "screening"],
    "registration": ["registration"],
    "welcome": ["welcome"],
    "other": ["other"]
}

def slugify(title):
    """Convert title to slug for filename"""
    return title.lower().replace(' ', '-').replace('+', '-').replace('#', '').strip('-')

def generate_talk_markdown(event):
    """Generate markdown content for a talk file"""
    name = event.get('title', '')
    subtitle = event.get('subtitle', '')
    description = event.get('description', '')
    
    # Build description with subtitle if available
    if subtitle:
        description = f"{subtitle}. {description}"
    
    date = event.get('date', '')
    start_time = event.get('start_time', '')
    end_time = event.get('end_time', '')
    
    # Parse times into hour/minute format
    if start_time:
        start_hour, start_minute = start_time.split(':')
        start_hour = int(start_hour)
        start_minute = int(start_minute)
    else:
        start_hour = 9
        start_minute = 0
    
    if end_time:
        end_hour, end_minute = end_time.split(':')
        end_hour = int(end_hour)
        end_minute = int(end_minute)
    else:
        end_hour = start_hour + 1
        end_minute = start_minute
    
    # Map room
    room_key = event.get('room')
    room = ROOM_MAP.get(room_key, "Room A")
    
    # Get tags from category
    category = event.get('category', 'other')
    tags = CATEGORY_TAGS.get(category, ["other"])
    
    # Build front matter
    front_matter = f"""---
name: "{name}"
description: >
  {description}
date: {date}
hour: {start_hour}
minute: {start_minute}
end_hour: {end_hour}
end_minute: {end_minute}
room: {room}
tags:
"""
    for tag in tags:
        front_matter += f"  - {tag}\n"
    
    front_matter += "---\n"
    
    # Add body content
    body = ""
    if subtitle:
        body += f"\n{subtitle}\n"
    
    # Add panel information if it exists
    if 'panels' in event and event['panels']:
        body += "\n## Panels\n"
        for panel in event['panels']:
            panel_title = panel.get('panel_title', '')
            chair = panel.get('chair', '')
            body += f"\n### {panel_title}\n"
            if chair:
                body += f"\nChair: {chair}\n"
            if 'papers' in panel:
                body += "\n#### Papers\n"
                for paper in panel['papers']:
                    paper_title = paper.get('title', '')
                    author = paper.get('author', '')
                    affiliation = paper.get('affiliation', '')
                    body += f"\n- **{paper_title}**\n"
                    body += f"  - {author}"
                    if affiliation:
                        body += f", {affiliation}"
                    body += "\n"
    
    return front_matter + body

def main():
    """Main function to process all event JSON files"""
    # Create _talks directory if it doesn't exist
    os.makedirs('_talks', exist_ok=True)
    
    # Get all event JSON files
    event_files = glob.glob('_events/*.json')
    event_files.sort()
    
    generated = []
    
    for event_file in event_files:
        with open(event_file, 'r') as f:
            event = json.load(f)
        
        # Generate markdown
        markdown = generate_talk_markdown(event)
        
        # Create filename
        title = event.get('title', '')
        slug = slugify(title)
        output_file = f'_talks/{slug}.md'
        
        # Write file
        with open(output_file, 'w') as f:
            f.write(markdown)
        
        generated.append({
            'input': event_file,
            'output': output_file,
            'title': title
        })
    
    # Print summary
    print(f"Generated {len(generated)} talk files:")
    for item in generated:
        print(f"  {item['input']} -> {item['output']}")

if __name__ == '__main__':
    main()
