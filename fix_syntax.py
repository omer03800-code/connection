import re

with open('exhibition/public/index.html', 'r') as f:
    html = f.read()

# Let's fix the broken strings
html = html.replace("'Mevo\\',", "'Mevo\\'ot Iron High School (Mevoot Iron)',")
html = html.replace("'Psychotechnical Examiner (Me\\',", "'Psychotechnical Examiner (Me\\'avchenet Psychotechnit)',")

# Actually, the python script earlier probably produced these fragments:
# 'Mevo\', 'ot Iron High School (Mevoot Iron)'
html = html.replace("'Mevo\\', 'ot Iron High School (Mevoot Iron)',", "'Mevo\\'ot Iron High School (Mevoot Iron)',")
html = html.replace("'Psychotechnical Examiner (Me\\', 'avchenet Psychotechnit)',", "'Psychotechnical Examiner (Me\\'avchenet Psychotechnit)',")
html = html.replace("'Zikhron Ya\\', 'akov',", "'Zikhron Ya\\'akov',")

with open('exhibition/public/index.html', 'w') as f:
    f.write(html)
print("fixed")
