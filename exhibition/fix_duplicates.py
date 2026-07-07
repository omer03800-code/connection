import sqlite3

db_path = 'db/six-degrees.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

names = [
    "Omer Barak", "Mai Mishli", "Shani Libner", "Shaked Klett", "Shaked Hogi",
    "Yoel Zajdner", "Shachar Liz Ben Or", "Ravid Dar", "Noya Ma'or", "Hila Lustig",
    "Sharon Greenberg", "Almog Aspaler", "Hila Ben Shabbat", "Oral Shafsha", "Re'ut Birkenstein"
]

for name in names:
    cursor.execute("SELECT id, description, tags FROM people WHERE name = ?", (name,))
    row = cursor.fetchone()
    if not row:
        continue
    p_id, desc, tags = row
    tags = tags or ''
    desc = desc or ''

    # Clean tags
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    filtered_tags = []
    
    for t in tags_list:
        tl = t.lower()
        
        # 1. Remove duplicated education fields
        if tl.startswith('education:'):
            continue
            
        # 2. Map old military tags to appropriate sections if needed
        elif tl.startswith('military:'):
            val = t[9:].strip()
            # Try to map them correctly based on content
            if val.lower() in ['military intelligence', 'idf spokesperson', 'combat engineering corps']:
                filtered_tags.append(f'armybase:{val}')
            elif val.lower() == 'military intelligence graphic designer':
                filtered_tags.append('armyrole:Graphic Designer') # Remove duplicate "Military Intelligence" from the name
            elif val.lower() == 'unit 81':
                filtered_tags.append(f'armyrole:{val}')
            elif ' / ' in val:
                # Re'ut: Nahal Nucleus / Soldier-teacher
                parts = val.split(' / ')
                filtered_tags.append(f'armybase:{parts[0].strip()}')
                filtered_tags.append(f'armyrole:{parts[1].strip()}')
            else:
                # Default to armyrole for things like 'Sambatzit', 'Sky Rider simulator instructor'
                filtered_tags.append(f'armyrole:{val}')
        else:
            filtered_tags.append(t)
            
    new_tags = ', '.join(filtered_tags)

    # Do the same for description if they exist there
    desc_lines = [l.strip() for l in desc.split('\n') if l.strip()]
    filtered_desc = []
    for l in desc_lines:
        ll = l.lower()
        if ll.startswith('education:'):
            continue
        elif ll.startswith('military:'):
            val = l[9:].strip()
            if val.lower() in ['military intelligence', 'idf spokesperson', 'combat engineering corps']:
                filtered_desc.append(f'armybase: {val}')
            elif val.lower() == 'military intelligence graphic designer':
                filtered_desc.append('armyrole: Graphic Designer')
            elif val.lower() == 'unit 81':
                filtered_desc.append(f'armyrole: {val}')
            elif ' / ' in val:
                parts = val.split(' / ')
                filtered_desc.append(f'armybase: {parts[0].strip()}')
                filtered_desc.append(f'armyrole: {parts[1].strip()}')
            else:
                filtered_desc.append(f'armyrole: {val}')
        else:
            filtered_desc.append(l)
    new_desc = '\n'.join(filtered_desc)
    
    cursor.execute("UPDATE people SET tags = ?, description = ? WHERE id = ?", (new_tags, new_desc, p_id))

conn.commit()
conn.close()
print("Done mapping duplicates.")
