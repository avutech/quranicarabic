"""Mapping-only review queue and independent votes; never modifies library content.

queue [limit]     show entries lacking a current unanimous independent decision
case SURAH KEY   full source, translations, verses, meanings; no other judge votes
verses SURAH FROM-TO  full proposed-target Quran and meaning context
vote FILE.json   record an evidence-backed vote (see tasks/MAPPING_AUDIT_FRAMEWORK.md)
status           decision counts; unresolved means not certified

Vote: {surah,key,reviewer,model,verdict,tr_mapping,en_mapping,targets,evidence,hashes}.
verdict: MATCH / REMAP / INTRODUCTION / MIXED / UNSURE.
targets: [{surah,from,to}] or [{surah,kind:"introduction"}].
hashes: SHA256 of ar,tr,en from the case file. Two distinct reviewers must agree
on verdict AND targets; any disagreement or UNSURE escalates, never auto-applies.
"""
import collections
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

LIB = Path(__file__).resolve().parent.parent / 'irab_library'
OUT = LIB / 'mapping_audit'
VOTES = OUT / 'votes'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def case(surah, key):
    entries = read(LIB / f's{surah:03d}.json')['entries']
    found = [(i, e) for i, e in enumerate(entries) if f"{e['b']}:{e['s']}-{e['e']}" == key]
    if len(found) != 1:
        raise ValueError('Entry must have exactly one source record')
    source_index, e = found[0]
    texts = {'ar': e['t']}
    for lang in ('tr', 'en'):
        p = LIB / f'{lang}_parts' / e['b'] / f's{surah:03d}.json'
        texts[lang] = (read(p) if p.exists() else {}).get(key, {}).get('t', '')
    words = read(LIB / 'w' / f's{surah:03d}.json')
    context = {a: {'ar': ' '.join(w['ar'] for w in v['w']), 'meanings': v['m']}
               for a, v in words.items() if max(1, e['s'] - 2) <= int(a) <= e['e'] + 2}
    fingerprint = hashlib.sha256(json.dumps({'surah': surah, 'index': source_index, 'entry': e},
                                            ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {'surah': surah, 'key': key, 'book': e['b'], 'source_index': source_index, 'range': [e['s'], e['e']],
            'ref': e.get('ref'), 'texts': texts, 'context': context,
            'hashes': {**{k: hashlib.sha256(t.encode()).hexdigest() for k, t in texts.items()},
                       'association': fingerprint}}


def current_votes(c):
    folder = VOTES / f"s{c['surah']:03d}" / c['key'].replace(':', '_')
    out = []
    for path in sorted(folder.glob('*.json')):
        v = read(path)
        if v['hashes'] != c['hashes']:
            continue
        if any(hashlib.sha256((LIB / 'w' / name).read_bytes()).hexdigest() != sha
               for name, sha in v.get('context_file_hashes', {}).items()):
            continue
        out.append(v)
    return out


def decision(votes):
    if any(v['verdict'] == 'UNSURE' for v in votes):
        return 'ESCALATE'
    if any(v.get(k) == 'UNSURE' for v in votes for k in ('tr_mapping', 'en_mapping')):
        return 'ESCALATE'
    signatures = {json.dumps([v['verdict'], v.get('tr_mapping'), v.get('en_mapping'), v['targets']], sort_keys=True) for v in votes}
    if len(signatures) > 1:
        return 'ESCALATE'
    if len({v['reviewer'] for v in votes}) < 2:
        return 'NEEDS_INDEPENDENT_REVIEW'
    if any(votes[0].get(k) == 'DIFFERENT_ENTRY' for k in ('tr_mapping', 'en_mapping')):
        return 'AGREED_TRANSLATION_MISMATCH'
    return 'AGREED_PROPOSAL' if votes[0]['verdict'] != 'MATCH' else 'AGREED_MATCH'


def validate_vote(v, c):
    if v.get('hashes') != c['hashes']:
        raise ValueError('Hashes missing or stale: reread complete current case')
    if v.get('verdict') not in {'MATCH', 'REMAP', 'INTRODUCTION', 'MIXED', 'UNSURE'}:
        raise ValueError('Invalid verdict')
    for lang in ('tr_mapping', 'en_mapping'):
        if v.get(lang) not in {'FOLLOWS_SOURCE', 'DIFFERENT_ENTRY', 'UNSURE'}:
            raise ValueError(f'{lang} must explicitly assess whether the translation follows this source')
    for field in ('reviewer', 'model', 'evidence'):
        if not isinstance(v.get(field), str) or not v[field].strip():
            raise ValueError(f'Missing {field}')
    if len(v['evidence']) < 25:
        raise ValueError('Evidence must identify the Arabic anchor and translation mapping')
    targets = v.get('targets')
    if not isinstance(targets, list) or (not targets and v['verdict'] != 'UNSURE'):
        raise ValueError('Explicit target associations required')
    for target in targets:
        s = target.get('surah')
        if type(s) is not int or not 1 <= s <= 114:
            raise ValueError('Invalid target surah')
        if target.get('kind') == 'introduction':
            if set(target) != {'surah', 'kind'}:
                raise ValueError('Introduction must not invent an ayah')
        else:
            count = len(read(LIB / 'w' / f's{s:03d}.json'))
            a, z = target.get('from'), target.get('to')
            if type(a) is not int or type(z) is not int or not 1 <= a <= z <= count:
                raise ValueError('Invalid target ayah range')
    if v['verdict'] == 'MATCH' and targets != [{'surah': c['surah'], 'from': c['range'][0], 'to': c['range'][1]}]:
        raise ValueError('MATCH must retain original association')
    if v['verdict'] == 'INTRODUCTION' and any(t.get('kind') != 'introduction' for t in targets):
        raise ValueError('INTRODUCTION requires introduction targets')


def main(args):
    command = args[0]
    if command == 'case':
        print(json.dumps(case(int(args[1]), args[2]), ensure_ascii=False, indent=2))
    elif command == 'verses':
        s = int(args[1]); a, z = map(int, args[2].split('-'))
        rows = read(LIB / 'w' / f's{s:03d}.json')
        if not 1 <= a <= z <= len(rows):
            raise ValueError('Invalid verse range')
        print(json.dumps({str(i): {'ar': ' '.join(w['ar'] for w in rows[str(i)]['w']),
                                  'meanings': rows[str(i)]['m']} for i in range(a, z + 1)},
                         ensure_ascii=False, indent=2))
    elif command == 'vote':
        v = read(Path(args[1])); c = case(v['surah'], v['key'])
        validate_vote(v, c)
        context_surahs = {v['surah'], *(t['surah'] for t in v['targets'])}
        v['context_file_hashes'] = {f's{s:03d}.json': hashlib.sha256((LIB / 'w' / f's{s:03d}.json').read_bytes()).hexdigest()
                                    for s in context_surahs}
        v['recorded_at'] = datetime.now(ZoneInfo('America/New_York')).isoformat()
        token = hashlib.sha256(v['reviewer'].encode()).hexdigest()[:20]
        folder = VOTES / f"s{v['surah']:03d}" / v['key'].replace(':', '_')
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f'{token}-{c["hashes"]["ar"][:12]}-{c["hashes"]["tr"][:12]}-{c["hashes"]["en"][:12]}-{c["hashes"]["association"][:12]}.json'
        with path.open('x', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=2)
        print(decision(current_votes(c)))
    elif command in ('queue', 'status'):
        counts = collections.Counter(); emitted = 0
        limit = int(args[1]) if len(args) > 1 else 20
        for line in (OUT / 'entries.jsonl').open(encoding='utf-8'):
            row = json.loads(line)
            # The manifest lists current content. Reload voted cases to reject stale votes.
            c = {'surah': row['surah'], 'key': row['key'], 'hashes': row['hashes']}
            votes = current_votes(c)
            if votes:
                c = case(row['surah'], row['key']); votes = current_votes(c)
            status = decision(votes); counts[status] += 1
            if command == 'queue' and status not in ('AGREED_MATCH', 'AGREED_PROPOSAL'):
                print(json.dumps({**{k: row[k] for k in ('surah', 'book', 'key')}, 'status': status}))
                emitted += 1
                if emitted >= limit:
                    break
        if command == 'status':
            print(json.dumps(dict(counts), indent=2))
    else:
        raise ValueError('Use queue, case, vote, or status')


if __name__ == '__main__':
    main(sys.argv[1:])
