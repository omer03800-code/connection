import json

with open('extracted_numbers.json', 'r') as f:
    data = json.load(f)

# The data has multiple tables from the numbers file. Each table is just concatenated.
# The table headers are "ID", "Value_EN", "Type_or_Notes", None
categories = []
current_category = None

for row in data:
    if not row or not any(row): continue
    if row[0] == "ID":
        current_category = []
        categories.append(current_category)
        continue
    
    if isinstance(row[0], float) and len(row) >= 2 and row[1]:
        if current_category is not None:
            val = str(row[1]).strip()
            if val:
                current_category.append(val)

names = ["Roles", "Companies", "High Schools", "Military Roles", "Military Units", "Military Bases", "Universities", "Degrees", "Youth Programs", "Moshavim Kibbutzim", "Cities"]

result = {}
for idx, cat in enumerate(categories):
    name = names[idx] if idx < len(names) else f"Category_{idx}"
    result[name] = cat

with open('parsed_categories.json', 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
