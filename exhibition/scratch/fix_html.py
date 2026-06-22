import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's extract all the wizard bodies and footers and reconstruct the form correctly!

# 1. Extract the whole form content
match = re.search(r'(<form id="add-form"[^>]*>)(.*?)(</form>)', content, re.DOTALL)
if not match:
    print("Could not find form")
    exit(1)

form_open = match.group(1)
form_inner = match.group(2)
form_close = match.group(3)

# 2. Extract all wizard-steps
steps = []
# We'll just manually fix it by string replacement because parsing HTML with regex is fragile.
# Let's just fix the mismatched </div> tags!

# Currently:
# wizard-step-1 ends with </div>
# then there is an extra </div> at line 625!
content = content.replace('                </div>\n            </div>\n            <div id="wizard-step-1-footer"', '                </div>\n            <div id="wizard-step-1-footer"')

# Now there's an extra </div> at line 682!
content = content.replace('                </div>\n            </div>\n            \n            <div id="wizard-step-4-footer"', '                </div>\n            <div id="wizard-step-4-footer"')

# Also remove inline style `padding: 20px; overflow-y: auto; flex: 1;` from steps 4b, 5, 6 
# because they are now INSIDE the wrapper!
content = content.replace('<div id="wizard-step-4b" class="wizard-step" style="padding: 20px; overflow-y: auto; flex: 1;">', '<div id="wizard-step-4b" class="wizard-step">')
content = content.replace('<div id="wizard-step-5" class="wizard-step" style="padding: 20px; overflow-y: auto; flex: 1;">', '<div id="wizard-step-5" class="wizard-step">')
content = content.replace('<div id="wizard-step-6" class="wizard-step" style="padding: 20px; overflow-y: auto; flex: 1;">', '<div id="wizard-step-6" class="wizard-step">')

# Wait, if I remove the extra </div> at 625, then wizard-step-1-footer, wizard-step-2, 3, 4, 4-footer, 4b, 4b-footer, 5, 5-footer, 6, 6-footer are ALL inside the wrapper!
# Then I need to close the wrapper before the form closes!
# The form closes with:
#             <div id="wizard-step-6-footer" ...> ... </div>
#         </form>
# So I need to add </div> before </form> ? NO, wait! 
# If I removed the two extra </div>s, the wrapper is NEVER closed!
# So I need to close it right before </form>? 
# NO, if the footers are INSIDE the wrapper, they will SCROLL. That is acceptable and actually easier!
# Apple style dialogs often scroll the whole content including buttons, OR the buttons are fixed at the bottom.
# If we want buttons fixed at the bottom, they MUST be outside the wrapper.
# To do that, I will just extract all footers and move them!

# Let's write a proper script to fix this.
