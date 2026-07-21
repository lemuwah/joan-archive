const fs = require('fs');
const path = require('path');

const IMAGES_DIR = 'images';
const MANIFEST = 'MANIFEST.md';
const REPORT = '.github/scripts/validation-report.md';

// Normalize filenames (remove weird extensions, unify hyphens)
function normalize(name) {
  return name
    .replace(/\s+/g, '_')
    .replace(/\.jfif$/i, '.jpg')
    .replace(/\.jpeg$/i, '.jpg')
    .trim();
}

// Read images folder
const images = fs.readdirSync(IMAGES_DIR)
  .filter(f => !f.toLowerCase().includes('readme'))
  .map(normalize)
  .sort();

// Auto‑generate manifest content
const manifestContent = images.map(f => `- ${f}`).join('\n');

// Write manifest automatically
fs.writeFileSync(MANIFEST, manifestContent);

// Write report
fs.writeFileSync(REPORT, `
# Auto‑Fix Manifest Report

The manifest has been automatically regenerated based on the contents of /images.

## Total images: ${images.length}

### Updated MANIFEST.md:
${manifestContent}
`);

console.log('Manifest auto‑fixed.');
