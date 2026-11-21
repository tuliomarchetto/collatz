// Use Lacuna's unmodified parser/extractor without its JS-only discovery filter.
import { parseLcov } from '../lacuna/dist/lib/coverage/lcov.js';
import { extractGaps } from '../lacuna/dist/lib/coverage/gaps.js';
import { writeFile } from 'node:fs/promises';
const report = await parseLcov('coverage', process.cwd());
const gaps = extractGaps(report, 90);
const result = {
  tool: 'lacuna-cli 0.6.2 library API',
  caveat: 'CLI Python discovery is unsupported in this checkout; uses unmodified parseLcov and extractGaps directly. Line/function coverage only, not proof validation.',
  threshold: 90,
  lineCoveragePercent: report.totalLineRate * 100,
  functionCoveragePercent: report.totalFunctionRate * 100,
  files: report.files.map(f => ({path: f.path, lineCoveragePercent: f.lineRate*100, uncoveredLines: f.lines.filter(l=>l.hit===0).map(l=>l.line)})),
  gaps
};
await writeFile('lacuna-python-analysis.json', JSON.stringify(result, null, 2)+'\n');
console.log(JSON.stringify(result, null, 2));
