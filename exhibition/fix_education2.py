import sqlite3

db_path = 'db/six-degrees.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

names_mapping = {
    "May Mishli": "Mai Mishli",
    "Shaked Klettr": "Shaked Klett",
    "Re'ut Brikenstein": "Re'ut Birkenstein"
}

for old_name, new_name in names_mapping.items():
    cursor.execute("SELECT id, description, tags FROM people WHERE name = ?", (old_name,))
    row = cursor.fetchone()
    if not row:
        print(f"Not found: {old_name}")
        continue
    
    p_id, desc, tags = row
    tags = tags or ''
    desc = desc or ''

    # Clean tags
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    filtered_tags = []
    for t in tags_list:
        tl = t.lower()
        if not (tl.startswith('university:') or tl.startswith('degree:') or tl.startswith('graduation year:')):
            filtered_tags.append(t)
    
    filtered_tags.extend([
        'university:University of Haifa',
        'degree:Visual Communication',
        'Graduation Year:2026'
    ])
    new_tags = ', '.join(filtered_tags)

    # Clean desc
    desc_lines = [l.strip() for l in desc.split('\n') if l.strip()]
    filtered_desc = []
    for l in desc_lines:
        ll = l.lower()
        if not (ll.startswith('university:') or ll.startswith('degree:') or ll.startswith('graduation year:')):
            filtered_desc.append(l)
            
    filtered_desc.extend([
        'university: University of Haifa',
        'degree: Visual Communication',
        'Graduation Year: 2026'
    ])
    new_desc = '\n'.join(filtered_desc)

    cursor.execute("UPDATE people SET name = ?, tags = ?, description = ? WHERE id = ?", (new_name, new_tags, new_desc, p_id))
    print(f"Updated: {new_name}")

conn.commit()
conn.close()
print("Done.")
