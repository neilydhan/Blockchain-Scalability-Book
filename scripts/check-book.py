#!/usr/bin/env python3
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
errors=[]
summary=(root/'SUMMARY.md').read_text()
summary_targets=[]
for target in re.findall(r'\]\(([^)]+\.md)\)',summary):
 p=root/target
 summary_targets.append(p.resolve())
 if not p.is_file(): errors.append(f'SUMMARY target missing: {target}')
chapter_files={p.resolve() for p in (root/'chapters').glob('*.md')}
listed=set(summary_targets)
for p in sorted(chapter_files-listed): errors.append(f'chapter not listed in SUMMARY: {p.relative_to(root)}')
for p in [root/'README.md',root/'SUMMARY.md',*sorted((root/'chapters').glob('*.md'))]:
 text=p.read_text()
 uses=set(re.findall(r'\[\^([^\]]+)\](?!:)',text))
 defs=set(re.findall(r'^\[\^([^\]]+)\]:',text,re.M))
 for n in sorted(uses-defs): errors.append(f'{p.relative_to(root)}: footnote {n} used but not defined')
 for n in sorted(defs-uses): errors.append(f'{p.relative_to(root)}: footnote {n} defined but not used')
 for link in re.findall(r'(?:src="|\]\()([^" )]+)',text):
  if link.startswith(('http://','https://','#','mailto:')): continue
  target=(p.parent/link).resolve()
  if not target.exists(): errors.append(f'{p.relative_to(root)}: local link missing: {link}')
figures={}
for p in sorted((root/'chapters').glob('*.md')):
 if p.name == '15_figure_credits.md': continue
 for number in re.findall(r'Figure (\d+\.\d+)',p.read_text()):
  if number in figures: errors.append(f'duplicate figure number {number}: {figures[number]} and {p.relative_to(root)}')
  figures[number]=p.relative_to(root)
if errors:
 print('\n'.join(f'ERROR: {x}' for x in errors),file=sys.stderr)
 sys.exit(1)
print(f'book checks passed: {len(summary_targets)} summary entries, {len(figures)} figures')
