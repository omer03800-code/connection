import sqlite3

conn = sqlite3.connect('db/six-degrees.sqlite')
c = conn.cursor()

c.execute("SELECT id, tags FROM people WHERE tags IS NOT NULL")
rows = c.fetchall()

for row in rows:
    pid, tags = row
    if not tags: continue
    
    t_list = [t.strip() for t in tags.split(',')]
    new_tags = []
    for t in t_list:
        if t.lower() == '#kadoorieschool':
            new_tags.append('highschool:Kadoorie School')
        elif t.lower() == '#hakfarhayarok':
            new_tags.append('highschool:HaKfar HaYarok')
        elif t.lower() in ['#militaryintelligence', '#8200']:
            new_tags.append('military:Military Intelligence')
        elif t.lower() == '#haifauniversity':
            new_tags.append('education:Haifa University')
        elif t.lower() == '#visualcommunication':
            new_tags.append('education:Visual Communication')
        else:
            new_tags.append(t)
            
    if new_tags != t_list:
        c.execute("UPDATE people SET tags = ? WHERE id = ?", (','.join(new_tags), pid))
        
conn.commit()
conn.close()
print("DB tags updated!")
