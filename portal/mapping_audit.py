"""Content-preserving mapping inventory. Writes only audit artifacts, never library content.

Run: python3 portal/mapping_audit.py
Automated findings are candidates, not semantic verdicts. Existing review records
are counted only when all three reviewed text hashes match the current texts.
"""
import collections
import hashlib
import html
import json
from pathlib import Path

import audit_ayah_match as deterministic
import build_irab_library as builder

LIB = builder.OUT_DIR
OUT = LIB / 'mapping_audit'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def run():
    OUT.mkdir(exist_ok=True)
    protected = sorted({*LIB.glob('s*.json'), LIB / 'books.json',
                        *LIB.glob('tr_parts/*/s*.json'), *LIB.glob('en_parts/*/s*.json'),
                        *LIB.glob('tr/s*.json'), *LIB.glob('en/s*.json'),
                        *LIB.glob('w/s*.json'), *LIB.glob('words_tr/s*.json')})
    before = {str(p.relative_to(LIB)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    deterministic.OUT = OUT / 'deterministic'
    deterministic.OUT.mkdir(exist_ok=True)
    deterministic.main([])
    catalog = read(LIB / 'books.json')
    meals = {str(m['id']) for m in catalog['meals']}
    qc = read(builder.QURANCOM_FILE) if builder.QURANCOM_FILE.exists() else None
    counts = collections.Counter()
    by_book = collections.defaultdict(collections.Counter)
    issues, inventory = [], []
    def flag(kind, **detail):
        counts[kind] += 1
        issues.append({'kind': kind, **detail})
    for surah in range(1, 115):
        data = read(LIB / f's{surah:03d}.json')
        words = read(LIB / 'w' / f's{surah:03d}.json')
        if data.get('surah') != surah:
            flag('SOURCE_SURAH_HEADER', surah=surah, actual=data.get('surah'))
        merged = {lang: read(LIB / lang / f's{surah:03d}.json') for lang in ('tr', 'en')}
        parts, ledgers, seen = {}, {}, set()
        for source_index, entry in enumerate(data['entries']):
            book = entry['b']; key = f"{book}:{entry['s']}-{entry['e']}"
            identity = {'book': book, 'surah': surah, 'key': key}
            if key in seen:
                flag('DUPLICATE_ENTRY_KEY', **identity)
            seen.add(key)
            by_book[book]['entries'] += 1
            texts = {'ar': entry['t']}
            for lang in ('tr', 'en'):
                pair = (lang, book)
                if pair not in parts:
                    path = LIB / f'{lang}_parts' / book / f's{surah:03d}.json'
                    parts[pair] = read(path) if path.exists() else {}
                record = parts[pair].get(key)
                texts[lang] = record.get('t', '') if record else ''
                if not record:
                    flag('MISSING_TRANSLATION', lang=lang, **identity)
                    continue
                expected = {'book': book, 'sure': surah, 'ayet_bas': entry['s'],
                            'ayet_son': entry['e'], 'sha1': digest(entry['t'])}
                wrong = {k: {'expected': v, 'actual': record.get('src', {}).get(k)}
                         for k, v in expected.items() if str(record.get('src', {}).get(k)) != str(v)}
                if wrong:
                    flag('TRANSLATION_PROVENANCE', lang=lang, fields=wrong, **identity)
                if merged[lang].get(key, {}).get('t') != texts[lang]:
                    flag('MERGED_READING_DIFFERS', lang=lang, **identity)
            if book not in ledgers:
                path = LIB / 'audit_full' / 'ledger' / book / f's{surah:03d}.json'
                ledgers[book] = read(path) if path.exists() else {}
            hashes = {lang: digest(text)[:12] for lang, text in texts.items()}
            review = {}
            for pas in ('p1', 'p2'):
                rec = ledgers[book].get(key, {}).get(pas, {})
                current = bool(rec) and all(rec.get(k) == v for k, v in hashes.items())
                complete = current and all(rec.get(k) for k in ('fit', 'trv', 'env'))
                review[pas] = {'current': complete, 'fit': rec.get('fit') if complete else None}
                if complete:
                    by_book[book][f'{pas}_current'] += 1
                    if any(rec.get(k) != 'OK' for k in ('fit', 'trv', 'env')):
                        by_book[book][f'{pas}_flagged'] += 1
                elif rec:
                    by_book[book][f'{pas}_stale_or_incomplete'] += 1
            fingerprint = hashlib.sha256(json.dumps({'surah': surah, 'index': source_index, 'entry': entry},
                                                      ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            inventory.append({**identity, 'source_index': source_index,
                              'range': [entry['s'], entry['e']],
                              'hashes': {**{lang: hashlib.sha256(text.encode()).hexdigest() for lang, text in texts.items()},
                                         'association': fingerprint},
                              'ref': entry.get('ref'), 'reviews': review,
                              'mapping_status': 'AWAITING_INDEPENDENT_REVIEW'})
        for pair, records in parts.items():
            for key in records.keys() - seen:
                flag('ORPHAN_TRANSLATION', surah=surah, lang=pair[0], book=pair[1], key=key)
        for lang in ('tr', 'en'):
            for key in merged[lang].keys() - seen:
                flag('ORPHAN_MERGED_READING', surah=surah, lang=lang, key=key)
        for ayah, row in words.items():
            counts['ayahs'] += 1
            identity = {'surah': surah, 'ayah': int(ayah)}
            if set(row['m']) != meals:
                flag('MEAL_RESOURCE_COVERAGE', present=sorted(row['m']), **identity)
            original = qc['ayahs'].get(f'{surah}:{ayah}') if qc else None
            if qc and not original:
                flag('MISSING_CACHED_AYAH', **identity)
            for resource, text in row['m'].items():
                counts['meal_records'] += 1
                if not text.strip():
                    flag('EMPTY_MEAL', resource=resource, **identity)
                if original and text != html.unescape(original.get('t', {}).get(resource, '')):
                    flag('MEAL_CACHE_MAPPING_DIFFERS', resource=resource, **identity)
            if original and [(w['ar'], w['tl'], w['en']) for w in row['w']] != [tuple(w) for w in original['w']]:
                flag('WORD_CACHE_MAPPING_DIFFERS', **identity)
    after = {str(p.relative_to(LIB)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    if before != after:
        raise RuntimeError('Protected content changed during audit; investigate concurrent work.')
    for name, rows in [('entries.jsonl', inventory), ('issues.jsonl', issues)]:
        (OUT / name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    (OUT / 'content_manifest.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
    summary = {'entries': len(inventory), 'by_book': dict(by_book), 'counts': dict(counts),
               'protected_files_unchanged': len(protected), 'meal_cache_available': bool(qc),
               'semantic_audit_complete': False,
               'limitations': ['Cached meal equality verifies extraction, not independent semantic correctness.',
                              'Quote checks are candidates, not proof of correct mapping.',
                              'Current pass-1 reviews are not independent adjudications.']}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
