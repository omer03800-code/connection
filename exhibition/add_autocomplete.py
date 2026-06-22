import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fields that need autocomplete setup in JS
# workplace, education, military, community, other
setup_js = """
        setupAutocomplete('f-city', 'city');
        setupAutocomplete('f-origin-city', 'origin_city');
        setupAutocomplete('f-role', 'role');
        setupAutocomplete('f-highschool', 'highschool');
        setupAutocomplete('f-workplace', 'workplace');
        setupAutocomplete('f-education', 'education');
        setupAutocomplete('f-military', 'military');
        setupAutocomplete('f-community', 'community');
        setupAutocomplete('f-other', 'other');
"""
old_setup_js = """
        setupAutocomplete('f-city', 'city');
        setupAutocomplete('f-origin-city', 'origin_city');
        setupAutocomplete('f-role', 'role');
        setupAutocomplete('f-highschool', 'highschool');
"""
if "setupAutocomplete('f-workplace', 'workplace');" not in html:
    html = html.replace(old_setup_js.strip(), setup_js.strip())

# Add dropdown and stats divs to HTML for fields that miss them
def ensure_autocomplete_divs(html, input_id):
    if f'id="dropdown-{input_id}"' not in html:
        # find the input and add the divs after it
        input_pattern = rf'(<input[^>]+id="{input_id}"[^>]*>)'
        replacement = rf'\1\n                        <div class="autocomplete-dropdown" id="dropdown-{input_id}"></div>\n                        <div class="dynamic-stats" id="stats-{input_id}"></div>'
        html = re.sub(input_pattern, replacement, html)
    return html

html = ensure_autocomplete_divs(html, 'f-workplace')
html = ensure_autocomplete_divs(html, 'f-military')
html = ensure_autocomplete_divs(html, 'f-education')
html = ensure_autocomplete_divs(html, 'f-prev-work')
html = ensure_autocomplete_divs(html, 'f-youth')
html = ensure_autocomplete_divs(html, 'f-community')
html = ensure_autocomplete_divs(html, 'f-other')

# Update class="chapter-block" to "chapter-block autocomplete-wrapper" for those inputs
def ensure_wrapper_class(html, input_id):
    # Find the containing div.chapter-block and add autocomplete-wrapper if needed
    # This is trickier with regex, I'll just find the label and input and check context
    pass

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
