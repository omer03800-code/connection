const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replace <div class="tags-wrapper" ...> with <label class="tags-wrapper" ...>
html = html.replace(/<div class="tags-wrapper" id="([^"]+)" onclick="document\.getElementById\('([^']+)'\)\.focus\(\)">([\s\S]*?)<\/div>\s*<div class="autocomplete-dropdown"/g, (match, twId, inputId, inner) => {
    return `<label class="tags-wrapper" id="${twId}" for="${inputId}" style="display:flex; cursor:text;">${inner}</label>\n                        <div class="autocomplete-dropdown"`;
});

// Since the regex might not catch all (like prev_work which doesn't have autocomplete-dropdown), let's just do it manually for all occurrences
const pattern = /<div class="tags-wrapper" id="([^"]+)" onclick="document\.getElementById\('([^']+)'\)\.focus\(\)">/g;

html = html.replace(pattern, (match, twId, inputId) => {
    return `<label class="tags-wrapper" id="${twId}" for="${inputId}" style="display:flex; cursor:text;">`;
});

// Now we need to replace the closing </div> of the tags-wrapper with </label>
// The structure is ALWAYS:
// <label class="tags-wrapper" id="..." for="..." style="...">
//      <input type="text" ...>
// </div>
// So we can replace `<input ...>\n                        </div>` with `</label>`
// Or just match:
// <label class="tags-wrapper" [^>]+>
//    <input type="text" [^>]+>
// </div>
html = html.replace(/(<label class="tags-wrapper"[^>]+>\s*<input[^>]+>)\s*<\/div>/g, '$1\n                        </label>');

// Let's also fix the edit form inputs which have `style="border:none;"`
html = html.replace(/(<label class="tags-wrapper"[^>]+>\s*<input[^>]+style="border:none;"[^>]*>)\s*<\/div>/g, '$1\n                    </label>');

fs.writeFileSync('index.html', html);
console.log('Fixed tags-wrapper elements');
