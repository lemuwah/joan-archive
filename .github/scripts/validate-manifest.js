// validate-manifest.js
const fs = require('fs');

const manifestPath = 'MANIFEST.md';
const imagesDir = 'images';

function readManifest() {
  const raw = fs.readFileSync(manifestPath, 'utf-8');
  return raw
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.endsWith('.jpg') || line.endsWith('.jfif'));
}

function readImages() {
  return fs.readdirSync(imagesDir);
}

function validate() {
  const manifestFiles = readManifest();
  const imageFiles = readImages();

  const missing = manifestFiles.filter(f => !imageFiles.includes(f));
  const extra = imageFiles.filter(f => !manifestFiles.includes(f));

  let report = '# Validation Report\n\n';

  if (missing.length > 0) {
    report += '## Missing files (listed in MANIFEST.md but not found in /images)\n';
    missing.forEach(f => report += `- ${f}\n`);
    report += '\n';
  }

  if (extra.length > 0) {
    report += '## Extra files (present in /images but not listed in MANIFEST.md)\n';
    extra.forEach(f => report += `- ${f}\n`);
    report += '\n';
  }

  if (missing.length === 0 && extra.length === 0) {
    report += 'All files match MANIFEST.md.\n';
  }

  fs.writeFileSync('.github/scripts/validation-report.md', report);

  if (missing.length > 0) process.exit(1);
  if (extra.length > 0) process.exit(1);
}

validate();
