import json
import re

with open('parsed_categories.json', 'r') as f:
    data = json.load(f)

def clean_list(lst):
    # remove empty, strip
    return sorted(list(set([str(x).strip() for x in lst if x and str(x).strip()])))

roles = clean_list(data.get("Roles", []))
companies = clean_list(data.get("Companies", []))
high_schools = clean_list(data.get("High Schools", []))
military_roles = clean_list(data.get("Military Roles", []))
military_units = clean_list(data.get("Military Units", []))
military_bases = clean_list(data.get("Military Bases", []))
universities = clean_list(data.get("Universities", []))
degrees = clean_list(data.get("Degrees", []))
youth_programs = clean_list(data.get("Youth Programs", []))
moshavim = clean_list(data.get("Moshavim Kibbutzim", []))
cities = clean_list(data.get("Cities", []))

with open('exhibition/public/index.html', 'r') as f:
    html = f.read()

# We need to rewrite the PREDEFINED block
predefined_match = re.search(r'const PREDEFINED = \{(.*?)\};', html, re.DOTALL)
if not predefined_match:
    print("Could not find PREDEFINED")
    exit(1)

predefined_str = predefined_match.group(1)

# Function to extract array from JS block
def extract_js_array(js_str, key):
    m = re.search(rf"'{key}':\s*\[(.*?)\]", js_str, re.DOTALL)
    if not m: return []
    arr_str = m.group(1)
    # Extract string literals
    return [x.strip() for x in re.findall(r"'([^']*)'", arr_str)]

old_highschool = extract_js_array(predefined_str, 'highschool')
old_military = extract_js_array(predefined_str, 'military')
old_education = extract_js_array(predefined_str, 'education')
old_role = extract_js_array(predefined_str, 'role')

# Merge
new_highschool = clean_list(old_highschool + high_schools)
new_military = clean_list(old_military + military_roles + military_units + military_bases)
new_education = clean_list(old_education + universities + degrees)
new_role = clean_list(old_role + roles)
new_city = clean_list(moshavim + cities)
new_workplace = clean_list(companies)
new_other = clean_list(youth_programs)

# Build new PREDEFINED JS object string
def to_js_arr(lst):
    # format into lines of 10 items
    res = []
    line = []
    for x in lst:
        # escape quotes
        safe_x = x.replace("'", "\\'")
        line.append(f"'{safe_x}'")
        if len(line) == 8:
            res.append("                    " + ", ".join(line))
            line = []
    if line:
        res.append("                    " + ", ".join(line))
    return "[\n" + ",\n".join(res) + "\n                ]"

new_predefined_str = f"""{{
                'highschool': {to_js_arr(new_highschool)},
                'military': {to_js_arr(new_military)},
                'education': {to_js_arr(new_education)},
                'role': {to_js_arr(new_role)},
                'city': {to_js_arr(new_city)},
                'workplace': {to_js_arr(new_workplace)},
                'prevwork': {to_js_arr(new_workplace)},
                'dynamic:other-category': {to_js_arr(new_other)}
            }}"""

html = html.replace("const PREDEFINED = {" + predefined_str + "};", "const PREDEFINED = " + new_predefined_str + ";")

# Now update synonymGroups
synonym_match = re.search(r'const synonymGroups = \[(.*?)\];\n\s*const genericRoles =', html, re.DOTALL)
if not synonym_match:
    print("Could not find synonymGroups")
    exit(1)

synonym_str = synonym_match.group(1)

# For synonym groups, we just append the new items as individual groups if they don't already exist.
# Or better, we just append all new ones that we know.
# Wait, synonymGroups maps variations to a type. The type is used for scoring.
# Types: degree, uni, small_town, big_city, army_base, army_unit, high_school, mechina
# Let's add them as new groups where words = [item.lower()]
new_synonyms = []
def add_synonyms(lst, ttype):
    for item in lst:
        new_synonyms.append(f"{{ type: '{ttype}', words: ['{item.lower().replace(chr(39), chr(92)+chr(39))}'] }}")

add_synonyms(moshavim, 'small_town')
add_synonyms(cities, 'big_city')
add_synonyms(high_schools, 'high_school')
add_synonyms(military_units, 'army_unit')
add_synonyms(military_bases, 'army_base')
add_synonyms(universities, 'uni')
add_synonyms(degrees, 'degree')
add_synonyms(youth_programs, 'mechina')

# Also, companies and roles? The match score doesn't use synonymGroups for roles (it uses string includes) and companies (it checks exact string match usually). 
# Wait, let's see calculateMatchScore for companies. It uses p1.workplace == p2.workplace probably. 
# We'll just add the above.

new_synonym_block = synonym_str + ",\n                " + ",\n                ".join(new_synonyms)
html = html.replace("const synonymGroups = [" + synonym_str + "];", "const synonymGroups = [" + new_synonym_block + "];")

# Now update genericRoles?
# It's fine to leave it as is, or we can add new roles to genericRoles so they don't give 15 points, but the user explicitly requested we want matches to suggest friends. We probably shouldn't add all new roles to genericRoles, as they are specific.

with open('exhibition/public/index.html', 'w') as f:
    f.write(html)

print("Successfully merged data into index.html")
