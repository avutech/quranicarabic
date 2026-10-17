# Independent review of previously reported misplaced entries

Review date: 2026-10-10. Scope: all 20 unique entries in the existing report’s “Source entries that belong to another ayah” section. Current local Arabic entries were read in full and compared with current local `irab_library/w/sNNN.json` Quran words. This independently checks those cases only; it does not certify all 51,211 entries, translations, original print editions, or the accuracy of the Quran reference dataset itself. No source or translation content was changed.

The older summary counts 27 SOURCE_MISPLACED verdicts, while this rendered section has 20 unique entries. Counts are not interchangeable. Proposed associations are review evidence, not applied corrections.

## Decision summary

| Current entry | Proposed association | Decision |
|---|---|---|
| 2:142 `akhfash` | 2:143 | CONFIRMED_REMAP |
| 4:176 `nahhas-meani` | Unresolved general prefatory material | ESCALATE |
| 5:68 `mekki-muskil` | 5:64 and potentially 5:68 | MIXED_AMBIGUOUS |
| 5:120 `nahhas-meani` | Surah 6 introduction | INTRODUCTION |
| 15:99 `nahhas-meani` | Surah 16 introduction; cited 16:126–128 | INTRODUCTION |
| 19:1 `mekki-muskil` | 19:2 primary; 19:1 grammatical relationship | CONFIRMED_REMAP |
| 21:112 `nahhas-meani` | Surah 22 introduction; cited 22:19–21 | INTRODUCTION |
| 25:33 `nahhas-irab` | 25:32 | CONFIRMED_REMAP |
| 32:17 `mekki-muskil` | 32:{17,23} | MIXED |
| 37:93 `mekki-muskil` | 37:{93,96} | MIXED |
| 38:88 `nahhas-meani` | Surah39 introduction; cited39:53–55 | INTRODUCTION |
| 38:24 `ukberi-tibyan` | 38:26 | CONFIRMED_REMAP |
| 40:45 `zajjaj` | 40:45–46 | RANGE_TOO_NARROW |
| 47:38 `nahhas-meani` | Surah48 introduction | INTRODUCTION |
| 62:9 `akhfash` | 62:{5,9} | MIXED |
| 62:5 `mekki-muskil` | 62:{5,8} | MIXED |
| 65:9 `zajjaj` | 65:9–12 | RANGE_TOO_NARROW |
| 68:17 `mekki-muskil` | 68:{6,15,17} | MIXED |
| 70:9 `semin-durr` | 70:10 | CONFIRMED_REMAP |
| 91:8 `semin-durr` | 91:{6,9,10}; relationship91:8 | MIXED |

Discontiguous sets must not become broad contiguous ranges: e.g. 32:{17,23} does not assert coverage of18–22. Preserve whole source entries and use multiple association metadata if needed. Introductions require a separate introduction destination. Higher-model review is useful for disputed genre and primary-vs-parallel decisions, but it cannot recover missing original-book layout without evidence.

## Entry evidence

### 2:142 — akhfash

Proposed: **2:143**. Status: `CONFIRMED_REMAP`.

Entire short entry analyzes وإن كانت لكبيرة; matches 2:143.

Arabic content SHA-256: `54b548799186b8da79a1c11a758f341315915c8452d39ce1df71f6a1774ef0dc`. Source: `irab_library/s002.json`, `akhfash:142-142`.

Opening source evidence (unaltered excerpt):

> قال ﴿وَإِن كَانَتْ لَكَبِيرَةً﴾ يعني "القِبْلَةَ" ولذلك أنث.

### 4:176 — nahhas-meani

Proposed: **Unresolved general prefatory material**. Status: `ESCALATE`.

Generic report on يا أيها الذين آمنوا / يا أيها الناس is not a unique verse anchor. 4:1 and 4:170 share an address; neither can be selected from this passage alone. Could be next-surah introduction. Require original book layout.

Arabic content SHA-256: `61ef88bb8b5bb7722e0f19b6464a7a7d2d5a4512e0e1f0d0f77b4588155c1f33`. Source: `irab_library/s004.json`, `nahhas-meani:176-176`.

Opening source evidence (unaltered excerpt):

> رُوى عن عَلْقمة أنه قال: "كلُّ ما كان في القرآن ﴿يَا أَيُّهَا ٱلَّذِينَ آمَنُواْ﴾ فنزل بالمدينة، وكلُّ ما كان في القرآن ﴿يَا أَيُّهَا ٱلنَّاسُ﴾ فنزل بمكة".

### 5:68 — mekki-muskil

Proposed: **5:64 and potentially 5:68**. Status: `MIXED_AMBIGUOUS`.

ما أنزل governed by وليزيدن occurs in BOTH 64 and 68. كلما أوقدوا / أطفأها identifies 64. Reject exclusive remap on common first phrase alone; associate 64 and retain 68 pending book-layout adjudication.

Arabic content SHA-256: `e4699f4313a6900597e1a7b6261db106c82a7783d5fd820507e5e08894d9fde5`. Source: `irab_library/s005.json`, `mekki-muskil:68-68`.

Opening source evidence (unaltered excerpt):

> قَوْله {مَا أنزل} مَا فِي مَوضِع رفع بِفِعْلِهِ وَهُوَ وليزيدن وَكلما ظرف وَالْعَامِل فِيهِ أوقدوا وَفِيه معنى الشَّرْط فَلَا بُد لَهُ من جَوَاب وَجَوَابه أطفأها

### 5:120 — nahhas-meani

Proposed: **Surah 6 introduction**. Status: `INTRODUCTION`.

Explicit نزلت سورة الأنعام; no unique ayah 6:1 commentary. Store surah introduction metadata, not invented ayah mapping.

Arabic content SHA-256: `d32b943e9274ec5ae17de7efb15293f5fc4b7ac10365e6df165ddfd3d3f9c119`. Source: `irab_library/s005.json`, `nahhas-meani:120-120`.

Opening source evidence (unaltered excerpt):

> قال: أخبرنا أبو جعفر أحمد بن محمّد بن إسماعيل النَحَّاسُ، قال: حدثنا محمدُّ بنُ أحمدَ بن يحيى، حدّثنا "أبو حاتم" روح بن الفرج، مولى الحَضارِمة قال: حدَّثنا أحمد بن محمَّد "أبو بكر العُمَريّ" قال: حدّثنا ابن أبي فُدَيْك، قال: حدّثني عُمر بن 

### 15:99 — nahhas-meani

Proposed: **Surah 16 introduction; cited 16:126–128**. Status: `INTRODUCTION`.

Explicit quoted وإن عاقبتم فعاقبوا belongs to126; says إلى آخر ثلاث آيات. Genre is revelation history, rather than three detailed ayah commentaries.

Arabic content SHA-256: `c88cd50333442709032a7b161f30cf70faf7789bdbc2bbcad092a1d6033bd82e`. Source: `irab_library/s015.json`, `nahhas-meani:99-99`.

Opening source evidence (unaltered excerpt):

> قال عبدالله بن عباس: إلاَّ ثلاث آيات، نزلْنَ بين مكة والمدينة، حين رجع النبيُّ ﷺ من أحُد ـ وقد قُتِل حمزةُ ومُثِّل به ـ فقال النبي "لأُمثلنَّ بثلاثين منهم، وقال المسلمون: لنمثِّلنَّ بهم" فأنزل الله ﴿وَإِنْ عَاقَبْتُم فعَاقِبُوا بِمِثْلِ مَا

### 19:1 — mekki-muskil

Proposed: **19:2 primary; 19:1 grammatical relationship**. Status: `CONFIRMED_REMAP`.

Opening ذكر رحمة ربك is 19:2; كهيعص is cited as alleged governor from19:1. Primary mapping2 with legitimate relationship1.

Arabic content SHA-256: `467249711d360df6734636fc10bf5cdc8e691da4ad39ae7e8ca7b3d8aa3fab2f`. Source: `irab_library/s019.json`, `mekki-muskil:1-1`.

Opening source evidence (unaltered excerpt):

> قَوْله تَعَالَى {ذكر رَحْمَة رَبك} قَالَ الْفراء هُوَ مَرْفُوع بكهيعص وَأنكر ذَلِك عَلَيْهِ الزّجاج وَقَالَ الْأَخْفَش هُوَ مُبْتَدأ مَحْذُوف الْخَبَر تَقْدِيره فِيمَا يقص عَلَيْك ذكر رَحْمَة رَبك
> وَقيل تَقْدِيره هَذَا الَّذِي يُتْلَى ذكر ر

### 21:112 — nahhas-meani

Proposed: **Surah 22 introduction; cited 22:19–21**. Status: `INTRODUCTION`.

Explicit سورة الحج and هذان خصمان with three ayahs. Do not file arbitrarily as22:1.

Arabic content SHA-256: `eadd5524e01d5387c01445636b9d6556086ad80d3c80e26555f59a0e37f07ebd`. Source: `irab_library/s021.json`, `nahhas-meani:112-112`.

Opening source evidence (unaltered excerpt):

> قال أبو عمرو بن العلاء عن مجاهد: سألتُ ابنَ عبَّاس فقال: سورةُ الحجِّ نزلتْ بمكة، سِوَى ثلاثِ آياتٍ منها، فإنهنّ نزلن بالمدينة، في ستَّةِ نفر من قريش: ثلاثةٌ منهم مؤمنون، وثلاثةٌ كافرون.
>  فأمَّا المؤمنون فهم "حمزةُ بن عبدالمطَّلب" و "عليُّ 

### 25:33 — nahhas-irab

Proposed: **25:32**. Status: `CONFIRMED_REMAP`.

جملة واحدة / كذلك / ورتلناه ترتيلا are32; continuation analysis about gradual revelation. No33 anchor.

Arabic content SHA-256: `9d02bd4f8b331fd2966f314c1867977e78d3421da07949a3278986eb0014bafe`. Source: `irab_library/s025.json`, `nahhas-irab:33-33`.

Opening source evidence (unaltered excerpt):

> ولو نزل جملة لكان قد سبق الحوادث التي كانت ينزل فيها القرآن، ولو نزل جملة بما فيه من الفرائض لثقل ذلك عليهم علم الله جلّ وعزّ. إنّ الصلاح في إنزاله متفرّقا لأنهم ينبّهون به مرّة بعد مرّة ولو نزل جملة لزال معنى التنبيه، وفيه ناسخ ومنسوخ فكان

### 32:17 — mekki-muskil

Proposed: **32:{17,23}**. Status: `MIXED`.

Separate قوله paragraphs analyze ما أخفي لهم and فلا تكن في مرية من لقائه. 38:24 بسؤال نعجتك and40:10 لمقت الله are grammatical parallels, not primary associations.

Arabic content SHA-256: `324588575b87b7c3f664e5edd04fb014e16124c01a6323ccea6aa5ab08dd6b8b`. Source: `irab_library/s032.json`, `mekki-muskil:17-17`.

Opening source evidence (unaltered excerpt):

> قَوْله مَا أُخْفِي لَهُم من أسكن الْيَاء جعل الْألف ألف الْمُتَكَلّم وَالْيَاء حَقّهَا الضَّم لِأَنَّهُ فعل مُسْتَقْبل لَكِن أسكنت اسْتِخْفَافًا وَمن فتح الْيَاء جعله فعلا مَاضِيا لم يسم فَاعله وَفِيه ضمير يقوم مقَام الْفَاعِل وَمَا ان جَعل

### 37:93 — mekki-muskil

Proposed: **37:{93,96}**. Status: `MIXED`.

ضربا identifies93; خلقكم وما تعملون identifies96. من شر ما خلق is a supporting theological parallel113:2, not a third principal commentary destination.

Arabic content SHA-256: `b161473b28f5ebb7dae7f301ca9b11b97b0a116d918e4a3e1f6a7b3db7ce5e88`. Source: `irab_library/s037.json`, `mekki-muskil:93-93`.

Opening source evidence (unaltered excerpt):

> قَوْله {ضربا} مصدر لِأَن فرَاغ بِمَعْنى فَضرب قَوْله {خَلقكُم وَمَا تَعْمَلُونَ} مَا فِي مَوضِع نصب بِخلق عطف على الْكَاف وَالْمِيم فِي خَلقكُم وَهِي وَالْفِعْل مصدر أَي خَلقكُم وعملكم وَهَذَا أليق بهَا لِأَنَّهُ تَعَالَى قَالَ {من شَرّ مَا

### 38:88 — nahhas-meani

Proposed: **Surah39 introduction; cited39:53–55**. Status: `INTRODUCTION`.

سورة الغرف and قل يا عبادي الذين أسرفوا identify next-surah introductory/revelation material.

Arabic content SHA-256: `6a9ae8d687ddf373f9d8b39b90511be5ebea1490a23ab590d402f829e0484e6e`. Source: `irab_library/s038.json`, `nahhas-meani:88-88`.

Opening source evidence (unaltered excerpt):

> قال وهبُ بنُ منبِّه: "من أحبَّ أن يَعْرِفَ قضاءَ اللهِ جلَّ وعزَّ في خلْقِه، فليقرأ سورة الغُرَفِ".
> قال مجاهد عن ابن عباس: هي مكيةٌ إلاَّ ثلاثَ آياتٍ منها، فإنهنَّ نزلْنَ بالمدينةِ، في "وحشيٍّ" قاتلِ حمزة، صلواتُ اللهِ على حمزة. أسلم ودخل ا

### 38:24 — ukberi-tibyan

Proposed: **38:26**. Status: `CONFIRMED_REMAP`.

Full quote يا داود إنا جعلناك خليفة... يوم الحساب is26; source printed(٢٤) is retained as source text.

Arabic content SHA-256: `c348fe9e673a167719d0cd1049d09f64e94c3093625b950a9598ff0f356edd39`. Source: `irab_library/s038.json`, `ukberi-tibyan:24-24`.

Opening source evidence (unaltered excerpt):

> قَالَ تَعَالَى: (يَا دَاوُدُ إِنَّا جَعَلْنَاكَ خَلِيفَةً فِي الْأَرْضِ فَاحْكُمْ بَيْنَ النَّاسِ بِالْحَقِّ وَلَا تَتَّبِعِ الْهَوَى فَيُضِلَّكَ عَنْ سَبِيلِ اللَّهِ إِنَّ الَّذِينَ يَضِلُّونَ عَنْ سَبِيلِ اللَّهِ لَهُمْ عَذَابٌ شَدِيدٌ بِ

### 40:45 — zajjaj

Proposed: **40:45–46**. Status: `RANGE_TOO_NARROW`.

سوء العذاب is45 and explicitly parsed as antecedent of النار in46. Source engages both; exclusive move46 would lose45 association.

Arabic content SHA-256: `7c7220e5aea563fb30c76ed984a8bb1d43f76833fbd0ebb64c38389dfa8e3ba6`. Source: `irab_library/s040.json`, `zajjaj:45-45`.

Opening source evidence (unaltered excerpt):

> وَقَوْلُهُ - عَزَّ وجَلَّ -: ﴿سُوءُ العَذابِ﴾ ﴿النّارُ يُعْرَضُونَ عَلَيْها﴾ [غافر: ٤٦]، ”اَلنّارُ“، بَدَلٌ مِن قَوْلِهِ: ”سُوءُ العَذابِ“، وجائِزٌ أنْ تَكُونَ مُرْتَفِعَةً عَلى إضْمارِ تَفْسِيرِ ”سُوءُ العَذابِ“، كَأنَّ قائِلًا قالَ: ”ما ه

### 47:38 — nahhas-meani

Proposed: **Surah48 introduction**. Status: `INTRODUCTION`.

Explicit نزلت سورة الفتح... شأن الحديبية. Not verse48:1-specific exposition.

Arabic content SHA-256: `6cb008ec85b02c47a016a04430668716a148eafe6987c30bf39ecaef2fc12b7d`. Source: `irab_library/s047.json`, `nahhas-meani:38-38`.

Opening source evidence (unaltered excerpt):

> مدنيةٌ في رواية مجاهد عن ابن عباس.
> وروى الزُّهريُّ عن عُرْوَةَ بنِ الزُّبيرِ، عن المِسْوَرِ بنِ مَخْرمةَ، ومروانَ قالا: " نزلت سورةُ الفتح بين مكة والمدينة، كلُّها في شأن الحديبية".

### 62:9 — akhfash

Proposed: **62:{5,9}**. Status: `MIXED`.

من يوم الجمعة is9; separate lexical discussion الأسفار is5. أبابيل and أساطير are analogies.

Arabic content SHA-256: `cbc342e566dd5e5aea43b3619a7b26cbed259dc4cead5891aee2c07f3948f4a2`. Source: `irab_library/s062.json`, `akhfash:9-9`.

Opening source evidence (unaltered excerpt):

> وقال ﴿مِن يَوْمِ ٱلْجُمُعَةِ﴾ يقول - والله أعلم - مِنْ صَلاةِ يَوْمِ الجُمُعَةِ.
> وقال بعض النحويين لا يكون لـ"الأَسْفارِ" واحد كنحو "أَبابيل" و"أَساطِير"، ونحو قول العرب: "ثَوْبٌ أكْبَاشٌ" وهو الردىء الغزل، و"ثَوْبٌ مِزْقٌ" للمتمزّق.

### 62:5 — mekki-muskil

Proposed: **62:{5,8}**. Status: `MIXED`.

يحمل أسفارا / بئس مثل القوم identifies5; فإنه ملاقيكم identifies8.

Arabic content SHA-256: `3a26e994b9cfcae49d94019bbf4d299c7aba002afb29a73bf49f80c86b6d6bd3`. Source: `irab_library/s062.json`, `mekki-muskil:5-5`.

Opening source evidence (unaltered excerpt):

> قَوْله يحمل أسفارا يحمل حَال من الْحمار
> قَوْله بئس مثل الْقَوْم مثل مَرْفُوع ببئس وَالْجُمْلَة فِي مَوضِع الْبَيَان لجملة محذوفة تَقْدِيره بئس مثل الْقَوْم هَذَا الْمثل لَكِن حذف لدلَالَة الْكَلَام عَلَيْهِ
> قَوْله فانه ملاقيكم هَذَا خبر ان 

### 65:9 — zajjaj

Proposed: **65:9–12**. Status: `RANGE_TOO_NARROW`.

Distinct exposition of فذاقت9, أعد الله / فاتقوا / ذكرا10, رسولا11, الله الذي خلق سبع سماوات12. 26:193–194 quoted as supporting parallel.

Arabic content SHA-256: `2850d687b7a7972232b87eaab28f76978a10e8793c475e0bdc41758f4e95dd5e`. Source: `irab_library/s065.json`, `zajjaj:9-9`.

Opening source evidence (unaltered excerpt):

> وَقَوْلُهُ: ﴿فَذاقَتْ وبالَ أمْرِها وكانَ عاقِبَةُ أمْرِها خُسْرًا﴾، أيْ: ثِقْلُ عاقِبَةِ أمْرِها، ﴿وَكانَ عاقِبَةُ أمْرِها خُسْرًا﴾، يَعْنِي في الآخِرَةِ، وهو قَوْلُهُ: ﴿أعَدَّ اللَّهُ لَهم عَذابًا شَدِيدًا﴾ [الطلاق: ١٠]، يَعْنِي بَعْدَ ذَ

### 68:17 — mekki-muskil

Proposed: **68:{6,15,17}**. Status: `MIXED`.

مصبحين identifies17; separate بأيكم المفتون analysis6 and قال أساطير الأولين15. Orthography examples from other verses are supporting parallels.

Arabic content SHA-256: `f081abb902e10d4d515d37b2ef60accec20c14dcf9402a3f5b803e8b5bc65d62`. Source: `irab_library/s068.json`, `mekki-muskil:17-17`.

Opening source evidence (unaltered excerpt):

> قَوْله مصبحين حَال من الْمُضمر فِي ليصر مِنْهَا الْمَرْفُوع وَلَا خبر لأصبح فِي هَذَا لِأَنَّهَا بِمَعْنى داخلين فِي الاصباح
> قَوْله بأيكم الْمفْتُون الْبَاء وَالْمعْنَى أَيّكُم الْمفْتُون وَقيل الْبَاء غير زَائِدَة لَكِنَّهَا بِمَعْنى فِي و

### 70:9 — semin-durr

Proposed: **70:10**. Status: `CONFIRMED_REMAP`.

Entire entry analyzes ولا يسأل حميم / حميما;10, not mountains/wool9.

Arabic content SHA-256: `4a55ee0f71374d74e73e7279bed4018dcf7e47d93bb0cffe62b1f9c1c9b686d7`. Source: `irab_library/s070.json`, `semin-durr:9-9`.

Opening source evidence (unaltered excerpt):

> قوله: {وَلاَ يَسْأَلُ حَمِيمٌ} : قرأ العامَّةُ «يَسْأَلُ» مبنياً للفاعل. والمفعولُ الثاني محذوفٌ فقيل: تقديرُه لا يَسْألُه نَصْرَهُ ولا شفاعتَه لعِلْمِه أنَّ ذلك مفقودٌ. وقيل: لا يَسْأله شيئاً مِنْ حَمْل أَوْزارِه. وقيل: «حميماً» منصوبٌ على

### 91:8 — semin-durr

Proposed: **91:{6,9,10}; relationship91:8**. Status: `MIXED`.

Opening قد أفلح is9; dedicated طحاها lexicography is6 (source citation wrongly says3); زكاها/دساها discussion spans9–10. فألهمها8 is cited to explain syntactic relation, not primary heading. Exclusive move9 is insufficient.

Arabic content SHA-256: `997076ac35c33cbd99fc110e4aa6e73f3631887b8cd560a56da45bdc38644406`. Source: `irab_library/s091.json`, `semin-durr:8-8`.

Opening source evidence (unaltered excerpt):

> قوله: {قَدْ أَفْلَحَ} : فيه وجهان، أحدُهما: أنه جوابُ القسم، والأصل: لقد، وإنما حُذِفَتْ لطولِ الكلامِ. والثاني: أنه ليس بجوابٍ وإنما جيْءَ به تابعاً لقولِه {فَأَلْهَمَهَا فُجُورَهَا وَتَقْوَاهَا} على سبيل الاستطرادِ، وليس مِنْ جوابِ القسم 
