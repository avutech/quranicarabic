"""Compare every library mapping/text with the original local extracted book data.

This proves preservation of extracted labels and text, not correctness of those
labels against the printed book or Quran. No content is modified.
"""
import collections
import hashlib
import json

import build_irab_library as builder


def run():
    current = collections.Counter()
    for surah in range(1, 115):
        entries = json.loads((builder.OUT_DIR / f's{surah:03d}.json').read_text())['entries']
        for e in entries:
            current[(e['b'], surah, int(e['s']), int(e['e']),
                     hashlib.sha256(e['t'].encode()).hexdigest())] += 1
    summary, issues = {}, []
    for book in builder.CATALOG:
        try:
            if book.get('loader'):
                data = builder.LOADERS[book['loader']]()
            else:
                path = builder.SRC_DIR / f"irab_kutuphane_{book['source']}.json"
                data = json.loads(path.read_text())
        except (FileNotFoundError, KeyError) as error:
            summary[book['id']] = {'available': False, 'reason': str(error)}
            continue
        expected = collections.Counter()
        for e in data['girdiler']:
            s, a, z = int(e['sure']), int(e['ayet_bas']), int(e['ayet_son'])
            text = builder.clean(e['metin'])
            if text and 1 <= s <= 114 and z >= a:
                expected[(book['id'], s, a, z, hashlib.sha256(text.encode()).hexdigest())] += 1
        actual = collections.Counter({k: v for k, v in current.items() if k[0] == book['id']})
        missing, extra = expected - actual, actual - expected
        summary[book['id']] = {'available': True, 'original_indexed_entries': sum(expected.values()),
                               'library_entries': sum(actual.values()), 'missing_or_changed': sum(missing.values()),
                               'extra_or_changed': sum(extra.values())}
        for label, rows in [('MISSING_OR_CHANGED', missing), ('EXTRA_OR_CHANGED', extra)]:
            for key, count in rows.items():
                issues.append({'kind': label, 'book': key[0], 'surah': key[1], 'from': key[2],
                               'to': key[3], 'sha256': key[4], 'count': count})
    out = builder.OUT_DIR / 'mapping_audit'
    out.mkdir(exist_ok=True)
    result = {'by_book': summary, 'issues': issues,
              'limitation': 'Extracted source-label agreement does not establish semantic or printed-source correctness.'}
    (out / 'original_source_comparison.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({'books': len(summary), 'issues': len(issues),
                      'entries_compared': sum(v.get('library_entries', 0) for v in summary.values())}))


if __name__ == '__main__':
    run()
