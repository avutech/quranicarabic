"""Exhaustive audit census: every entry, meaning cell and book/ayah lookup.

build creates a complete unsampled work manifest with two mandatory passes.
packet KIND SURAH [BOOK_OR_RESOURCE] emits full cases in that whole partition.
status validates EXHAUSTIVE review receipts against current complete packets.
No content is changed and no unit is automatically marked semantically reviewed.
Large partitions must be broken into consecutive units by the orchestrator,
with every unit retained in the manifest. No representative/random selection.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

import mapping_review as review

LIB = review.LIB
OUT = LIB / 'mapping_audit' / 'full_coverage'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def conclusion(record, unit):
    """Normalize receipt conventions for comparison, never certify their truth."""
    verdict = record.get('fit', record.get('meaning_verdict', record.get('verdict')))
    targets = record.get('proposed_associations', [])
    if not targets and verdict == 'MATCH':
        targets = ([{'surah': unit['surah'], 'from': unit['range'][0], 'to': unit['range'][1]}]
                   if unit['kind'] == 'entry' else [{'surah': unit['surah'], 'from': unit['ayah'], 'to': unit['ayah']}])
    normalized = []
    for target in targets:
        if isinstance(target, str):
            match = re.fullmatch(r'(\d+):(\d+)(?:-(\d+))?', target)
            if not match:
                return None
            s, a, z = match.groups(); target = {'surah': int(s), 'from': int(a), 'to': int(z or a)}
        if target.get('kind') == 'introduction':
            normalized.append((target['surah'], 'introduction'))
        else:
            a = target.get('from', target.get('start', target.get('ayah_start')))
            z = target.get('to', target.get('end', target.get('ayah_end')))
            if any(type(v) is not int for v in (target.get('surah'), a, z)):
                return None
            normalized.append((target['surah'], a, z))
    languages = tuple('FOLLOWS_SOURCE' if record.get(k) == 'MATCH' else record.get(k)
                      for k in ('tr_mapping', 'en_mapping')) if unit['kind'] == 'entry' else ()
    return verdict, languages, tuple(sorted(normalized, key=str))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = read(LIB / 'books.json')
    books = [b['id'] for b in catalog['books'] if b.get('status') == 'ready']
    resources = [str(m['id']) for m in catalog['meals']]
    counts = collections.Counter(); no_entries = 0
    for s in range(1, 115):
        entries = read(LIB / f's{s:03d}.json')['entries']
        words = read(LIB / 'w' / f's{s:03d}.json')
        cover = collections.defaultdict(list); units = []
        for index, e in enumerate(entries):
            key = f"{e['b']}:{e['s']}-{e['e']}"
            units.append({'id': f'entry:{s}:{index}', 'kind': 'entry', 'surah': s,
                          'book': e['b'], 'key': key, 'source_index': index,
                          'range': [e['s'], e['e']], 'required_passes': [1, 2]})
            for a in range(e['s'], e['e'] + 1):
                cover[e['b'], a].append(index)
        for a, row in words.items():
            for resource in resources:
                units.append({'id': f'meaning:{s}:{a}:{resource}', 'kind': 'meaning',
                              'surah': s, 'ayah': int(a), 'resource': resource,
                              'present': resource in row['m'], 'required_passes': [1, 2]})
            for book in books:
                indexes = cover[book, int(a)]
                no_entries += not indexes
                units.append({'id': f'lookup:{s}:{a}:{book}', 'kind': 'lookup',
                              'surah': s, 'ayah': int(a), 'book': book,
                              'source_indexes': indexes, 'required_passes': [1, 2]})
        counts.update(u['kind'] for u in units)
        (OUT / f's{s:03d}.json').write_text(json.dumps(units, ensure_ascii=False, separators=(',', ':')))
    summary = {'sampling': False, 'required_passes_per_unit': 2, 'selected_model': 'gpt-6-astra',
               'reasoning_effort': 'max', 'books': len(books), 'surahs': 114,
               'unit_counts': dict(counts), 'total_units': sum(counts.values()),
               'required_review_decisions': 2 * sum(counts.values()),
               'lookups_with_no_source_entry': no_entries,
               'semantic_completion': False,
               'note': 'No-entry lookups remain explicit units; cache equality and historical samples do not close units.'}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def packet(kind, surah, selector=None):
    units = read(OUT / f's{surah:03d}.json')
    words = read(LIB / 'w' / f's{surah:03d}.json')
    entries = read(LIB / f's{surah:03d}.json')['entries']
    for unit in units:
        if unit['kind'] != kind or (selector and selector != unit.get('book', unit.get('resource'))):
            continue
        if kind == 'entry':
            payload = review.case(surah, unit['key'])
        elif kind == 'meaning':
            a = unit['ayah']; row = words[str(a)]
            payload = {'ar': ' '.join(w['ar'] for w in row['w']),
                       'meaning': row['m'].get(unit['resource']),
                       'context': {str(i): {'ar': ' '.join(w['ar'] for w in words[str(i)]['w']),
                                           'meanings': words[str(i)]['m']}
                                   for i in range(max(1, a - 2), min(len(words), a + 2) + 1)}}
        else:
            merged = {lang: read(LIB / lang / f's{surah:03d}.json') for lang in ('tr', 'en')}
            displayed = []
            for index in unit['source_indexes']:
                e = entries[index]; key = f"{e['b']}:{e['s']}-{e['e']}"
                displayed.append({'source': e, 'key': key,
                                  'readings': {lang: merged[lang].get(key) for lang in ('tr', 'en')}})
            payload = {'ar': ' '.join(w['ar'] for w in words[str(unit['ayah'])]['w']),
                       'source_entries': [entries[i] for i in unit['source_indexes']],
                       'current_local_displayed_entries': displayed,
                       'context': words[str(unit['ayah'])],
                       'staging_display_verified': False,
                       'original_source_verification_required': True}
        yield {**unit, 'payload': payload, 'packet_sha256': sha({'unit': unit, 'payload': payload})}


def status():
    """Count every manifest unit. Review receipts never automatically certify accuracy."""
    manifests = {}; indexes = {}
    for s in range(1, 115):
        manifests[s] = read(OUT / f's{s:03d}.json')
        indexes.update({u['id']: u for u in manifests[s]})
    reviews = collections.defaultdict(dict); problems = []; cached = {}
    tasks = LIB.parent / 'tasks'
    for file in sorted(tasks.glob('EXHAUSTIVE_*.jsonl')):
        for number, line in enumerate(file.read_text().splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line); uid = record.get('unit_id'); pas = record.get('pass')
            unit = indexes.get(uid)
            if not unit or type(pas) is not int or pas not in (1, 2) or not record.get('reviewer_session'):
                problems.append({'file': file.name, 'line': number, 'issue': 'INVALID_ID_PASS_OR_REVIEWER'})
                continue
            verdict = record.get('fit') if unit['kind'] == 'entry' else record.get('meaning_verdict', record.get('verdict'))
            evidence = record.get('evidence', record.get('semantic_evidence'))
            if verdict not in {'MATCH', 'MISMATCH', 'UNSURE'} or not evidence:
                problems.append({'unit_id': uid, 'pass': pas, 'issue': 'MISSING_VALID_VERDICT_OR_EVIDENCE'})
                continue
            runtime = record.get('reviewer_runtime', {})
            effort = record.get('requested_reasoning_effort', record.get('requested_effort', runtime.get('requested_reasoning_effort')))
            model = record.get('requested_model', runtime.get('requested_model'))
            if model != 'gpt-6-astra' or effort != 'max':
                problems.append({'unit_id': uid, 'pass': pas, 'issue': 'MODEL_REQUEST_NOT_RECORDED_AS_REQUIRED'})
                continue
            if unit['kind'] == 'entry' and any(record.get(k) not in {'MATCH', 'MISMATCH', 'UNSURE', 'FOLLOWS_SOURCE', 'DIFFERENT_ENTRY'}
                                              for k in ('tr_mapping', 'en_mapping')):
                problems.append({'unit_id': uid, 'pass': pas, 'issue': 'MISSING_TRANSLATION_MAPPING_VERDICTS'})
                continue
            selector = unit.get('book', unit.get('resource'))
            cache_key = (unit['kind'], unit['surah'], selector)
            if cache_key not in cached:
                cached[cache_key] = {p['id']: p for p in packet(*cache_key)}
            current = cached[cache_key][uid]
            if record.get('packet_sha256') != current['packet_sha256']:
                problems.append({'unit_id': uid, 'pass': pas, 'issue': 'STALE_PACKET'})
                continue
            if pas in reviews[uid]:
                problems.append({'unit_id': uid, 'pass': pas, 'issue': 'DUPLICATE_PASS_RECEIPT'})
                continue
            reviews[uid][pas] = record
    counts = collections.Counter(); by_kind = collections.defaultdict(collections.Counter)
    for uid, unit in indexes.items():
        recs = reviews[uid]; kind = unit['kind']
        by_kind[kind]['units'] += 1
        for pas in (1, 2):
            if pas in recs:
                counts[f'pass{pas}_current_receipts'] += 1
                by_kind[kind][f'pass{pas}_current_receipts'] += 1
        if len(recs) < 2:
            counts['units_missing_one_or_both_reviews'] += 1
        elif recs[1]['reviewer_session'] == recs[2]['reviewer_session']:
            problems.append({'unit_id': uid, 'issue': 'SECOND_REVIEW_NOT_INDEPENDENT'})
            counts['units_missing_independent_second_review'] += 1
        else:
            counts['units_with_two_distinct_reviewers'] += 1
            first, second = conclusion(recs[1], unit), conclusion(recs[2], unit)
            if not first or not second or first != second or first[0] == 'UNSURE' or 'UNSURE' in first[1]:
                counts['units_requiring_adjudication'] += 1
            else:
                counts['units_with_agreeing_review_evidence'] += 1
    result = {'sampling': False, 'total_units': len(indexes), 'required_review_decisions': 2 * len(indexes),
              'counts': dict(counts), 'by_kind': dict(by_kind), 'receipt_problems': problems,
              'semantic_audit_complete': False,
              'note': 'Receipts prove current review coverage only. Agreement, original-source verification and resolution remain separate gates.'}
    (OUT / 'progress.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    if sys.argv[1] == 'build':
        build()
    elif sys.argv[1] == 'packet':
        for row in packet(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None):
            print(json.dumps(row, ensure_ascii=False))
    elif sys.argv[1] == 'status':
        status()
    else:
        raise ValueError('Use build or packet KIND SURAH [BOOK_OR_RESOURCE]')
