with open('/Users/omerbarak/.gemini/antigravity/brain/ef399673-4424-4f65-9897-d28c4fe5a145/task.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('- `[ ]` **Merge Me/Someone Else**:', '- `[x]` **Merge Me/Someone Else**:')
text = text.replace('  - `[ ]` Delete Step 1 HTML.', '  - `[x]` Delete Step 1 HTML.')
text = text.replace('  - `[ ]` Add toggle to Basic Info step.', '  - `[x]` Add toggle to Basic Info step.')
text = text.replace('  - `[ ]` JS to dynamically update placeholders based on the toggle.', '  - `[x]` JS to dynamically update placeholders based on the toggle.')

text = text.replace('- `[ ]` **Location Defaults & Autocomplete**:', '- `[x]` **Location Defaults & Autocomplete**:')
text = text.replace("  - `[ ]` Set `f-country` value to 'Israel'.", "  - `[x]` Set `f-country` value to 'Israel'.")
text = text.replace("  - `[ ]` Update `setupAutocomplete` JS to normalize locations (e.g. merge Ilania variations) and reject invalid `/` values.", "  - `[x]` Update `setupAutocomplete` JS to normalize locations (e.g. merge Ilania variations) and reject invalid `/` values.")
text = text.replace("  - `[ ]` Update `.dynamic-stats` CSS for subtlety.", "  - `[x]` Update `.dynamic-stats` CSS for subtlety.")

text = text.replace('- `[ ]` **Spacing**:', '- `[x]` **Spacing**:')
text = text.replace("  - `[ ]` Increase vertical margins on `.chapter-block` and `.wizard-step`.", "  - `[x]` Increase vertical margins on `.chapter-block` and `.wizard-step`.")

text = text.replace('- `[ ]` **Life Chapters Order**:', '- `[x]` **Life Chapters Order**:')
text = text.replace("  - `[ ]` Move High School and Education out of `hidden-chapters` by default.", "  - `[x]` Move High School and Education out of `hidden-chapters` by default.")
text = text.replace("  - `[ ]` JS logic to conditionally move Military if country is Israel.", "  - `[x]` JS logic to conditionally move Military if country is Israel.")

text = text.replace('- `[ ]` **Navigation Buttons**:', '- `[x]` **Navigation Buttons**:')
text = text.replace("  - `[ ]` Anchor `[ BACK ]` and `[ NEXT ]` to the bottom of the modal.", "  - `[x]` Anchor `[ BACK ]` and `[ NEXT ]` to the bottom of the modal.")
text = text.replace("  - `[ ]` Fix button hover states to only affect text.", "  - `[x]` Fix button hover states to only affect text.")

text = text.replace('- `[ ]` **Person Card in Step 3**:', '- `[x]` **Person Card in Step 3**:')
text = text.replace("  - `[ ]` Update `#match-profile-card` to use the design system of a full profile card.", "  - `[x]` Update `#match-profile-card` to use the design system of a full profile card.")

with open('/Users/omerbarak/.gemini/antigravity/brain/ef399673-4424-4f65-9897-d28c4fe5a145/task.md', 'w', encoding='utf-8') as f:
    f.write(text)
