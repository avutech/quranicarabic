"""Aggregate independent mapping review artifacts without promoting proposals to truth."""
import collections
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TASKS = BASE / 'tasks'
OUT = BASE / 'irab_library' / 'mapping_audit'


def rows(name):
    p = TASKS / name
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def run():
    census = [json.loads(line) for line in (OUT / 'entries.jsonl').read_text().splitlines()]
    identities = {(r['surah'], r['key']): r for r in census}
    grouped = collections.defaultdict(list)
    coverage = {}
    configs = [
        ('daas_mapping_review.jsonl', 'key', lambda r: True, 'fit'),
        ('semin_mapping_review.jsonl', 'entry_key', lambda r: r['review_status'] == 'FULL_AR_TR_EN_MAPPING_REVIEW', 'fit'),
        ('HISTORICAL_FIT_FLAGS_REVIEW.jsonl', 'source_key', lambda r: r['full_ar_tr_en_read'], 'mapping_status'),
    ]
    for filename, keyfield, completed, verdictfield in configs:
        records = rows(filename); counts = collections.Counter(); done = 0
        for record in records:
            if not completed(record):
                counts['PENDING'] += 1
                continue
            identity = (record['surah'], record[keyfield])
            source = identities.get(identity)
            if not source:
                counts['UNKNOWN_SOURCE'] += 1
                continue
            hashes = record.get('sha256', record.get('current_hashes'))
            current = all(source['hashes'][k] == value if len(value) == 64
                          else hashlib.sha1(_text(source, k).encode()).hexdigest()[:12] == value
                          for k, value in hashes.items())
            if not current:
                counts['STALE'] += 1
                continue
            done += 1; counts[record[verdictfield]] += 1
            grouped[identity].append({'artifact': str((TASKS / filename).relative_to(BASE)), 'review': record})
        coverage[filename] = {'records': len(records), 'current_full_reviews': done, 'verdicts': dict(counts)}
    register = []
    for identity, reviews in sorted(grouped.items()):
        source = identities[identity]
        register.append({'book': source['book'], 'surah': source['surah'], 'key': source['key'],
                         'source_index': source['source_index'], 'current_range': source['range'],
                         'hashes': source['hashes'], 'independent_reviews': reviews,
                         'decision_status': 'FIRST_REVIEW_EVIDENCE_ONLY', 'association_applied': False})
    manifest = json.loads((OUT / 'content_manifest.json').read_text())
    changed = [name for name, sha in manifest.items()
               if hashlib.sha256((BASE / 'irab_library' / name).read_bytes()).hexdigest() != sha]
    summary = {'independent_artifact_coverage': coverage,
               'unique_current_fully_read_entries': len(register), 'total_entries': len(census),
               'remaining_without_new_full_review': len(census) - len(register),
               'protected_content_changes': changed, 'semantic_audit_complete': False,
               'note': 'Includes source scope findings, not automatically proven misplacements; no proposed association applied.'}
    (OUT / 'independent_reviews.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in register))
    (OUT / 'progress.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def _text(source, lang):
    s, key, book = source['surah'], source['key'], source['book']
    if lang != 'ar':
        return json.loads((BASE / 'irab_library' / f'{lang}_parts' / book / f's{s:03d}.json').read_text())[key]['t']
    entries = json.loads((BASE / 'irab_library' / f's{s:03d}.json').read_text())['entries']
    return entries[source['source_index']]['t']


if __name__ == '__main__':
    run()
