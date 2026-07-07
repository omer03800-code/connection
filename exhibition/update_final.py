import sqlite3

db_path = 'db/six-degrees.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

names = [
    "Omer Barak",
    "Mai Mishli",
    "Shani Libner",
    "Shaked Klett",
    "Shaked Hogi",
    "Yoel Zajdner",
    "Shachar Liz Ben Or",
    "Ravid Dar",
    "Noya Ma'or",
    "Hila Lustig",
    "Sharon Greenberg",
    "Almog Aspaler",
    "Hila Ben Shabbat",
    "Oral Shafsha",
    "Re'ut Birkenstein"
]

for name in names:
    cursor.execute("SELECT id, description, tags FROM people WHERE name = ?", (name,))
    row = cursor.fetchone()
    if not row:
        print(f"Not found: {name}")
        continue
    
    p_id, desc, tags = row
    tags = tags or ''
    desc = desc or ''

    # Clean tags
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    filtered_tags = []
    for t in tags_list:
        tl = t.lower()
        # Remove old university, degree, and graduation year
        if not (tl.startswith('university:') or tl.startswith('degree:') or tl.startswith('graduation year:')):
            filtered_tags.append(t)
    
    # Add new university and degree tags (2026 goes into university)
    filtered_tags.extend([
        'university:University of Haifa',
        'university:2026',
        'degree:Visual Communication'
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
        'university: 2026',
        'degree: Visual Communication'
    ])
    new_desc = '\n'.join(filtered_desc)

    # Update role to '#Student', tags, and description
    cursor.execute("UPDATE people SET role = ?, tags = ?, description = ? WHERE id = ?", 
                   ('#Student', new_tags, new_desc, p_id))
    print(f"Updated: {name}")

conn.commit()
conn.close()
print("Done.")
