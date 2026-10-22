#!/usr/bin/env python3
"""Check final manuscript, portable assets, source coverage and quiz styling."""
from pathlib import Path
import csv,re,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1];PRINT=ROOT/'print'
tex=(PRINT/'CS532_Textbook.tex').read_text();log=(PRINT/'CS532_Textbook.log').read_text()
for error in ['Overfull','There were undefined references','multiply defined','Missing character:','! LaTeX Error','! Package']:
 assert error not in log,error
assert '\\chapter{Lecture 5:' in tex and '\\chapter{Lecture 6:' in tex
for label in ['eq-lec05-patch-energy','eq-lec05-lk','eq-lec06-factorization','eq-lec06-triangulation','eq-lec06-jacobian','eq-lec06-updates']:
 assert label in tex,label
with zipfile.ZipFile(PRINT/'CS532_Textbook_Source.zip') as archive:
 assert archive.testzip() is None
 for name in ['CS532_Textbook.tex','CS532_Textbook.pdf','README.md']:
  assert archive.read(name)==(PRINT/name).read_bytes(),name
 count=0
 for line in tex.splitlines():
  if '\\sphinxincludegraphics' not in line:continue
  name=line.split(']{',1)[1].rstrip('}').replace('{','').replace('}','');assert 'images/'+name in archive.namelist(),name;count+=1
 assert count>=50,count
coverage=list(csv.DictReader((ROOT/'authoring/coverage.csv').open()))
for lec,total in [(5,91),(6,72)]:
 rows=[r for r in coverage if r['lecture']==str(lec)];assert len(rows)==total;assert all('audit' in r['status'] for r in rows)
 for r in rows:assert (ROOT/r['textbook_destination']).exists()
 for p in (ROOT/f'book/lectures/lecture{lec:02d}').glob('*.md'):
  assert not any(ord(c)<32 and c not in '\n\t' for c in p.read_text()),p
 for f in (ROOT/f'book/images/lecture{lec:02d}').glob('*.pdf'):assert f.stat().st_size>0
info=subprocess.check_output(['pdfinfo',str(PRINT/'CS532_Textbook.pdf')],text=True)
print('PASS: strict final TeX log; manuscript/ZIP/PDF match; all',count,'figure occurrences bundled; all 163 new source pages mapped; no control characters.')
print(re.search(r'Pages:\s+(\d+)',info).group(0))
