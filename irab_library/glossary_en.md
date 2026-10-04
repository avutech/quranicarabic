# I'rab Library — English Reading Guide and Glossary

Binding for everyone preparing English readings of the classical i'rab books.
Goal: students learning i'rab. The translation must be **faithful**,
**terminologically consistent** and keep the Arabic **traceable**.

## Style rules

1. **Faithful, complete translation.** Do not summarise, add or comment. Long
   discussions are translated in full.
2. **Quranic words** (inside ﴿…﴾, {…}, «…» or the parsed words in (…)) stay in
   Arabic script, never transliterated: «(بسم): a preposition and its genitive noun,
   attached to an omitted predicate…».
3. **Poetry** stays in Arabic, followed by a short English gloss in parentheses; keep
   the verse number.
4. **Variant readings:** "X read it as …"; readers' names in standard
   transliteration (ʿĀṣim, Nāfiʿ, Ibn Kathīr, Ḥamza, al-Kisāʾī, Abū ʿAmr, Ibn ʿĀmir).
5. **Scholars and schools:** Sībawayh, al-Khalīl, al-Kisāʾī, al-Farrāʾ, al-Akhfash,
   al-Zajjāj, al-Mubarrad; the Basrans, the Kufans.
6. **Technical terms:** use the transliterated Arabic term with an English gloss the
   first time in an entry ("ḥāl (circumstantial)"), then the Arabic term alone.
   Follow the table below.
7. **Formulae:** "Allah the Exalted", "the Prophet ﷺ", "may Allah be pleased with him".
8. **Footnotes:** [[…]] becomes «[Note: …]».
9. **Never correct the source silently.** Translate what is written and flag it as
   «[Translator's note: …]». Anything you add for clarity is marked the same way.
10. **Section headings:** Derviş and Sâfî headings become «* Vocabulary:», «* I'rab:»,
    «* Rhetoric:», «* Morphology:» and «* Benefits:», each on its own line.

## Glossary

| Arabic | English |
|---|---|
| مبتدأ / خبر | mubtadaʾ (subject) / khabar (predicate) |
| فاعل / نائب فاعل | fāʿil (agent) / nāʾib fāʿil (deputy agent) |
| مفعول به | mafʿūl bihi (direct object) |
| مفعول مطلق / لأجله / فيه / معه | mafʿūl muṭlaq (absolute object) / mafʿūl li-ajlihi (object of purpose) / mafʿūl fīhi (adverbial) / mafʿūl maʿahu (object of accompaniment) |
| حال / تمييز | ḥāl (circumstantial) / tamyīz (specification) |
| نعت (صفة) | naʿt (adjective) |
| بدل / عطف بيان / توكيد | badal (substitute) / ʿaṭf bayān (explicative apposition) / tawkīd (emphasis) |
| معطوف / حرف عطف | maʿṭūf (conjoined) / conjunction |
| مضاف / مضاف إليه | muḍāf / muḍāf ilayhi (genitive construct) |
| جار ومجرور / متعلق بـ | preposition and its genitive noun / attached to (mutaʿalliq) |
| مرفوع / منصوب / مجرور / مجزوم | nominative (marfūʿ) / accusative (manṣūb) / genitive (majrūr) / jussive (majzūm) |
| مبني على / في محل | indeclinable (mabnī) on … / in the position of … |
| مقدّر / ظاهر | implied (muqaddar) / overt |
| محذوف تقديره … | omitted, its implied form being "…" |
| ضمير متصل / منفصل / مستتر | attached / detached / latent (mustatir) pronoun |
| اسم موصول / صلة | relative noun / ṣila (relative clause) |
| اسم إشارة | demonstrative |
| فعل ماض / مضارع / أمر | past / imperfect / imperative verb |
| مبني للمجهول | passive |
| جملة لا محل لها من الإعراب | a clause with no grammatical position |
| استئنافية / اعتراضية / تفسيرية | resumptive / parenthetical / explicative |
| جواب الشرط / فعل الشرط | apodosis (jawāb al-sharṭ) / protasis (fiʿl al-sharṭ) |
| إنّ وأخواتها / كان وأخواتها | inna and its sisters / kāna and its sisters |
| لا النافية للجنس | the lā of generic negation |
| الاستثناء / المستثنى | exception / excepted |
| النداء / المنادى | vocative / the one addressed |
| زائدة | redundant (zāʾida) |
| مصدر / مصدر مؤول | maṣdar (verbal noun) / interpreted maṣdar |
| اسم فاعل / اسم مفعول | active / passive participle |
| ممنوع من الصرف | diptote |
| اللام المزحلقة | the shifted lām (al-lām al-muzaḥlaqa) |
| منصوب بنزع الخافض | accusative by removal of the preposition |
| البصريون / الكوفيون | the Basrans / the Kufans |

## Output (for translators)

```
venv/bin/python tr_tool.py --lang en list|show|put …
```

Readings are saved to `irab_library/en_parts/<book>/sNNN.json`, with the source
entry and the sha1 of its Arabic text recorded automatically.
