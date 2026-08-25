#!/usr/bin/env python3
"""Build TrailScript-standalone.html - the whole clinician tool as one file.

WHY THIS EXISTS
    index.html loads four sibling scripts. GitHub's per-file "Download raw file"
    button hands you one file, so index.html downloaded on its own has no ZIP
    table, no offline copy, no QR codes and no EHR launch - and then rejects
    every ZIP code while claiming a table of 42,555 entries it never loaded.
    One file that needs nothing beside it makes that failure impossible.

WHY IT RUNS IN CI RATHER THAN BY HAND
    A generated file committed by hand drifts from its source silently. This is
    run by .github/workflows/release.yml, and `--check` fails the build if the
    committed copy no longer matches what index.html would produce.
"""
import sys, os, re, hashlib

DEPS = ['zips.js', 'trailscript-fallback.js', 'qrcode.min.js', 'fhir-client.min.js']
OUT  = 'TrailScript-standalone.html'

def build():
    s = open('index.html', encoding='utf-8').read()
    inlined = []
    for d in DEPS:
        tag = '<script src="%s"></script>' % d
        if tag not in s:
            continue
        js = open(d, encoding='utf-8').read()
        # a literal </script> inside the inlined JS would end the block early
        js = js.replace('</script>', '<\\/script>')
        s = s.replace(tag, '<script>/* inlined: %s */\n%s\n</script>' % (d, js))
        inlined.append(d)
    s = s.replace('<head>', '<head>\n<!-- SINGLE-FILE BUILD: every dependency is '
                            'inlined; this file needs nothing beside it. -->', 1)
    if len(inlined) != len(DEPS):
        sys.exit('FAIL: inlined %d of %d dependencies (%s)'
                 % (len(inlined), len(DEPS), ', '.join(inlined)))
    return s

def check(s):
    """Verify the OUTPUT, not the inputs that made it. Each dependency is
    confirmed by a signature only that file contains - a filename proves
    nothing, since the filename is what we just removed."""
    problems = []
    leftover = re.findall(r'<script src="([^"]+)"></script>', s)
    if leftover:
        problems.append('external script tags survive: %s' % leftover)
    for dep, sig in (('zips.js', '"92354"'), ('trailscript-fallback.js', 'TS_FALLBACK'),
                     ('qrcode.min.js', 'qrcode'), ('fhir-client.min.js', 'FHIR')):
        if sig not in s:
            problems.append('%s did not make it in (signature %s absent)' % (dep, sig))
    if s.count('SINGLE-FILE BUILD') != 1:
        problems.append('build marker appears %d times' % s.count('SINGLE-FILE BUILD'))
    return problems

if __name__ == '__main__':
    built = build()
    problems = check(built)
    if problems:
        for p in problems: print('FAIL:', p)
        sys.exit(1)
    if '--check' in sys.argv:
        if not os.path.exists(OUT):
            sys.exit('FAIL: %s is missing' % OUT)
        have = open(OUT, encoding='utf-8').read()
        if have != built:
            sys.exit('FAIL: %s is stale. Rebuild it: python3 tools/build-standalone.py'
                     '\n  committed sha256 %s\n  rebuilt   sha256 %s'
                     % (OUT, hashlib.sha256(have.encode()).hexdigest()[:16],
                        hashlib.sha256(built.encode()).hexdigest()[:16]))
        print('OK: %s matches index.html (%d bytes)' % (OUT, len(have)))
    else:
        open(OUT, 'w', encoding='utf-8').write(built)
        print('built %s - %d bytes, %d dependencies inlined, all checks passed'
              % (OUT, len(built), len(DEPS)))
