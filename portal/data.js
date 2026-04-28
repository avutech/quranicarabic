const LEVELS = [
  {
    id: 'level1',
    title: { en: 'Level 1 — Beginner', tr: 'Seviye 1 — Başlangıç', ar: 'المستوى الأول — المبتدئ' },
    desc: { en: '150+ verse analyses · 500+ new words', tr: '150\'den fazla ayet tahlili · 500\'den fazla yeni kelime', ar: 'تحليل أكثر من ١٥٠ آية · أكثر من ٥٠٠ كلمة جديدة' },
    lessons: [
      {
        week: 1, pdf: 'Level-1/1st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Arabic Word Types: Noun (Ism), Verb (Fiʿl), and Particle (Ḥarf)', tr: 'Arapçada Kelime Çeşitleri: İsim, Fiil ve Harf', ar: 'أقسام الكلمة: الاسم والفعل والحرف' },
        questions: [
          { type: 'grammar', q: 'What are the three types of Arabic words (أقسام الكلمة)?', expected: 'Ism (اسم) = noun/name, Fi\'l (فعل) = verb, Harf (حرف) = particle/preposition' },
          { type: 'grammar', q: 'Is the word كَتَبَ an isim, fi\'l, or harf? How do you know?', expected: 'Fi\'l (verb) — it expresses an action (he wrote) and accepts tense conjugation' },
          { type: 'grammar', q: 'Is the word مِنْ an isim, fi\'l, or harf? How do you know?', expected: 'Harf (particle) — it does not independently carry full meaning, it connects words (from/of)' },
          { type: 'vocabulary', q: 'Give two examples each of an isim, a fi\'l, and a harf from the Quran.', expected: 'Isim: اللَّهُ، كِتَابٌ — Fi\'l: خَلَقَ، قَالَ — Harf: فِي، مِنْ، إِلَى' },
          { type: 'grammar', q: 'What characteristic makes an isim (noun) different from a fi\'l (verb)?', expected: 'An isim names a person, place, thing, or concept and can take tanwin/ال. A fi\'l expresses an action or state and changes with tense and person.' },
        ]
      },
      {
        week: 2, pdf: 'Level-1/2nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Definite and Indefinite Nouns, and Solar & Lunar Letters', tr: 'Belirli ve Belirsiz İsimler ile Şemsî ve Kamerî Harfler', ar: 'المعرفة والنكرة والحروف الشمسية والقمرية' },
        questions: [
          { type: 'grammar', q: 'How do you make an Arabic noun definite? Give an example.', expected: 'Add ال (al-) prefix and remove tanwin: كِتَابٌ (a book) → الْكِتَابُ (the book)' },
          { type: 'grammar', q: 'What is Tanwin (تنوين) and what does it indicate?', expected: 'Tanwin is a double vowel mark adding an "n" sound to the end of a noun, indicating it is indefinite (nakira): كِتَابٌ = a book' },
          { type: 'grammar', q: 'Is مُسْلِمٌ definite or indefinite? What is its definite form?', expected: 'Indefinite (has tanwin). Definite form: الْمُسْلِمُ (the Muslim)' },
          { type: 'translation', q: 'Translate: الْحَمْدُ لِلَّهِ — and explain why الْحَمْدُ is definite.', expected: 'All praise is for Allah. الْحَمْدُ is definite because it has the ال prefix and no tanwin.' },
          { type: 'grammar', q: 'Can a noun have both ال and tanwin at the same time? Why or why not?', expected: 'No. ال makes a noun definite; tanwin marks indefiniteness. They are mutually exclusive.' },
        ]
      },
      {
        week: 3, pdf: 'Level-1/3rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Masculine & Feminine Nouns and Demonstrative Pronouns', tr: 'Eril ve Dişil İsimler ve İşaret İsimleri', ar: 'الاسم المذكر والمؤنث وأسماء الإشارة' },
        questions: [
          { type: 'grammar', q: 'What suffix typically marks a feminine noun in Arabic?', expected: 'ة (ta marbuta), e.g. مُسْلِمَةٌ (a Muslim woman), مَدِينَةٌ (a city)' },
          { type: 'grammar', q: 'Is مَسْجِدٌ masculine or feminine? How can you tell?', expected: 'Masculine — it has no ta marbuta (ة) and refers to a place without natural gender' },
          { type: 'vocabulary', q: 'What are the demonstrative pronouns for "this" (masc.) and "this" (fem.)?', expected: 'هَذَا (this — masculine), هَذِهِ (this — feminine)' },
          { type: 'vocabulary', q: 'What are the demonstrative pronouns for "that" (masc.) and "that" (fem.)?', expected: 'ذَلِكَ (that — masculine), تِلْكَ (that — feminine)' },
          { type: 'grammar', q: 'Name two Arabic nouns that are feminine without having ta marbuta (ة).', expected: 'Any two of: أُمٌّ (mother), أَرْضٌ (earth), شَمْسٌ (sun), نَفْسٌ (soul), يَدٌ (hand), عَيْنٌ (eye)' },
        ]
      },
      {
        week: 4, pdf: 'Level-1/4th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Idafa (Genitive / Possessive Noun Construction)', tr: 'İsim Tamlaması (İzafet)', ar: 'الإضافة' },
        questions: [
          { type: 'grammar', q: 'What is the Idafa construction and what are its two parts?', expected: 'A genitive noun phrase: Mudaf (مضاف) + Mudaf ilayh (مضاف إليه). The mudaf loses tanwin and ال; the mudaf ilayh takes genitive (kasra).' },
          { type: 'translation', q: 'Translate: كِتَابُ اللَّهِ', expected: 'The Book of Allah / Allah\'s Book' },
          { type: 'grammar', q: 'Can the first noun (mudaf) in an idafa have ال? Why?', expected: 'No. The mudaf cannot have ال or tanwin because the idafa itself makes it specific.' },
          { type: 'translation', q: 'Translate: بَيْتُ الْمُسْلِمِ', expected: 'The Muslim\'s house / The house of the Muslim' },
          { type: 'grammar', q: 'What case does the second noun (mudaf ilayh) always take in idafa?', expected: 'Genitive case (مجرور), marked by kasra (ـِ) or kasratan (ـٍ)' },
        ]
      },
      {
        week: 5, pdf: 'Level-1/5th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Adjective and the Noun it Describes (Al-Sifa and Al-Mawsuf)', tr: 'Sıfat ve Mevsuf (Nitelenen İsim)', ar: 'الصِّفَةُ وَالْمَوْصُوف' },
        questions: [
          { type: 'grammar', q: 'In Arabic, does the adjective (na\'t) come before or after the noun it describes?', expected: 'After the noun: الطَّالِبُ الْمُجْتَهِدُ (the hardworking student)' },
          { type: 'grammar', q: 'In what four things must an adjective agree with its noun?', expected: 'Gender (masculine/feminine), number (singular/dual/plural), definiteness (definite/indefinite), and case (nominative/accusative/genitive)' },
          { type: 'grammar', q: 'What is the feminine form of the adjective كَبِيرٌ (big)?', expected: 'كَبِيرَةٌ' },
          { type: 'translation', q: 'Translate: الطَّالِبُ الْمُجْتَهِدُ', expected: 'The hardworking/diligent student' },
          { type: 'grammar', q: 'Make this phrase definite: طَالِبٌ مُجْتَهِدٌ', expected: 'الطَّالِبُ الْمُجْتَهِدُ — both the noun and adjective take ال' },
        ]
      },
      {
        week: 6, pdf: 'Level-1/6th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Pronouns (Detached/Separate Pronouns for Nominative and Accusative)', tr: 'Zamirler (Munfasıl Ref\' ve Nasb Zamirleri)', ar: 'الضمائر المنفصلة (ضمائر الرفع والنصب المنفصلة)' },
        questions: [
          { type: 'vocabulary', q: 'What are the detached pronouns for: he, she, they (masc. pl.)?', expected: 'هُوَ (he), هِيَ (she), هُمْ (they — masculine or mixed group)' },
          { type: 'vocabulary', q: 'When is هُمَا used?', expected: 'For "they two" (dual) — both masculine and feminine: those two people' },
          { type: 'translation', q: 'Translate: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ', expected: 'You alone we worship and You alone we ask for help (إِيَّاكَ = You — emphatic detached object pronoun)' },
          { type: 'vocabulary', q: 'What is the detached pronoun for "you" (feminine singular)?', expected: 'أَنْتِ' },
          { type: 'grammar', q: 'What is the difference between هُمْ and هُنَّ?', expected: 'هُمْ = they (masculine or mixed group); هُنَّ = they (exclusively feminine group)' },
        ]
      },
      {
        week: 7, pdf: 'Level-1/7th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Attached Pronouns (Damair Muttasila)', tr: 'Bitişik Zamirler (Muttasıl Zamirler)', ar: 'الضمائر المتصلة' },
        questions: [
          { type: 'vocabulary', q: 'What attached pronoun suffix means "his/him" in Arabic?', expected: 'ـهُ (after most letters): كِتَابُهُ = his book' },
          { type: 'translation', q: 'Translate: رَبُّهُمْ', expected: 'Their Lord (ـهُمْ = their/them, masculine plural)' },
          { type: 'grammar', q: 'What is the attached pronoun for "our/us" and give an example?', expected: 'ـنَا: رَبُّنَا = our Lord, هَدَانَا = He guided us' },
          { type: 'grammar', q: 'Attach the pronoun "her" (ـهَا) to the word بَيْتٌ.', expected: 'بَيْتُهَا = her house (tanwin drops when pronoun is added)' },
          { type: 'vocabulary', q: 'What pronoun suffix is used for "you" (masculine singular)?', expected: 'ـكَ: كِتَابُكَ = your book, رَبُّكَ = your Lord' },
        ]
      },
      {
        week: 8, pdf: 'Level-1/8th Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Prepositions (Huruf al-Jarr) and Adverbs of Place (Zarf al-Makan)', tr: 'Harf-i Cerler ve Yer Zarfları', ar: 'حروف الجرّ وظروف المكان' },
        questions: [
          { type: 'vocabulary', q: 'What does the preposition فِي mean and what case follows it?', expected: 'فِي = in/inside. The following noun takes genitive case (kasra): فِي الْبَيْتِ = in the house' },
          { type: 'vocabulary', q: 'What does عَلَى mean and give a Quranic example?', expected: 'عَلَى = on/upon. Example: عَلَى صِرَاطٍ مُسْتَقِيمٍ = on a straight path' },
          { type: 'vocabulary', q: 'What do إِلَى and مِنْ mean?', expected: 'إِلَى = to/towards; مِنْ = from/of' },
          { type: 'translation', q: 'Translate: الْكِتَابُ فِي الْبَيْتِ', expected: 'The book is in the house' },
          { type: 'grammar', q: 'What are ظروف المكان (adverbs of place)? Give two examples.', expected: 'Words expressing location: فَوْقَ (above), تَحْتَ (below), أَمَامَ (in front of), خَلْفَ (behind), بَيْنَ (between)' },
        ]
      },
      {
        week: 9, pdf: 'Level-1/9th Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Nominal Sentence (Jumlah Ismiyya): Mubtada and Khabar', tr: 'İsim Cümlesi: Mübteda ve Haber', ar: 'الجملة الاسمية: المبتدأ والخبر' },
        questions: [
          { type: 'grammar', q: 'What are the two parts of a nominal sentence (جملة اسمية)?', expected: 'Mubtada (مبتدأ) = subject and Khabar (خبر) = predicate. Together they make a complete statement.' },
          { type: 'grammar', q: 'What case does the Mubtada take and why is it usually definite?', expected: 'Nominative (مرفوع — damma). It is usually definite because it is the known topic of the sentence.' },
          { type: 'translation', q: 'Translate and identify mubtada and khabar: اللَّهُ غَفُورٌ', expected: 'Allah is All-Forgiving. Mubtada: اللَّهُ (definite); Khabar: غَفُورٌ (indefinite)' },
          { type: 'grammar', q: 'What is the difference between a nominal sentence (جملة اسمية) and a verbal sentence (جملة فعلية)?', expected: 'Nominal sentence begins with a noun (isim); verbal sentence begins with a verb (fi\'l)' },
          { type: 'translation', q: 'Translate: الْقُرْآنُ الْكَرِيمُ كِتَابُ اللَّهِ', expected: 'The Noble Quran is the Book of Allah' },
        ]
      },
      {
        week: 10, pdf: 'Level-1/10th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Singular, Dual, and Sound Masculine Plural', tr: 'Tekil, İkil ve Kurallı Eril Çoğul', ar: 'المفرد والمثنى وجمع المذكر السالم' },
        questions: [
          { type: 'grammar', q: 'How do you form the dual of a noun in Arabic?', expected: 'Add ـَانِ (nominative) or ـَيْنِ (genitive/accusative): كِتَابٌ → كِتَابَانِ / كِتَابَيْنِ' },
          { type: 'grammar', q: 'How do you form the Sound Masculine Plural (جمع مذكر سالم)?', expected: 'Add ـُونَ (nominative) or ـِينَ (genitive/accusative) to the singular: مُسْلِمٌ → مُسْلِمُونَ / مُسْلِمِينَ' },
          { type: 'grammar', q: 'What is the plural of مُؤْمِنٌ (believer) using the sound masculine plural?', expected: 'مُؤْمِنُونَ (nominative) / مُؤْمِنِينَ (genitive/accusative)' },
          { type: 'translation', q: 'Translate: وَالْمُؤْمِنُونَ وَالْمُؤْمِنَاتُ', expected: 'And the believing men and the believing women' },
          { type: 'grammar', q: 'What is the dual of رَجُلٌ (man)?', expected: 'رَجُلَانِ (two men — nominative) / رَجُلَيْنِ (genitive/accusative)' },
        ]
      },
      {
        week: 11, pdf: 'Level-1/11th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Sound Feminine Plural (Jam\' Mu\'annath Salim)', tr: 'Kurallı Müennes Çoğul (Cem\' Müennes Salim)', ar: 'جَمْعُ مُؤَنَّثٍ سَالِم' },
        questions: [
          { type: 'grammar', q: 'How do you form the Sound Feminine Plural (جمع مؤنث سالم)?', expected: 'Remove ة (ta marbuta) if present, then add ـَاتٌ (nominative) or ـَاتٍ (genitive/accusative): مُسْلِمَةٌ → مُسْلِمَاتٌ' },
          { type: 'grammar', q: 'What is the sound feminine plural of آيَةٌ (verse/sign)?', expected: 'آيَاتٌ (nominative) / آيَاتٍ (genitive/accusative)' },
          { type: 'grammar', q: 'What is the sound feminine plural of جَنَّةٌ (paradise)?', expected: 'جَنَّاتٌ' },
          { type: 'translation', q: 'Translate: وَبَشِّرِ الْمُؤْمِنِينَ بِأَنَّ لَهُمْ مِنَ اللَّهِ فَضْلًا كَبِيرًا', expected: 'And give good tidings to the believers that for them from Allah is great bounty' },
          { type: 'grammar', q: 'Can the sound feminine plural form apply to masculine nouns? Give an example.', expected: 'Yes, in some cases: صَلَاةٌ → صَلَوَاتٌ; also يَوْمٌ (masculine) has no sound fem. plural — but some masculine words borrowed the ـات ending' },
        ]
      },
      {
        week: 12, pdf: 'Level-1/12th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Broken Plural (Jam\' al-Taksir) — Patterns and Quranic Examples', tr: 'Kırık Çoğul (Cemü\'t-Teksir) — Kalıpları ve Kuran\'dan Örnekler', ar: 'جَمْعُ التَّكْسِيرِ — أوزانه وأمثلته القرآنية' },
        questions: [
          { type: 'grammar', q: 'What is a broken plural (جمع تكسير) and why is it called "broken"?', expected: 'A plural formed by changing the internal vowel pattern of the word — called "broken" because the word pattern is broken/rearranged, e.g. كِتَابٌ → كُتُبٌ' },
          { type: 'vocabulary', q: 'What is the broken plural of مَسْجِدٌ (mosque)?', expected: 'مَسَاجِدُ' },
          { type: 'vocabulary', q: 'What is the broken plural of رَجُلٌ (man)?', expected: 'رِجَالٌ' },
          { type: 'vocabulary', q: 'What is the broken plural of قَلْبٌ (heart)?', expected: 'قُلُوبٌ' },
          { type: 'grammar', q: 'Does a broken plural have a fixed pattern, or does each word need to be memorized?', expected: 'There are common patterns (e.g. فُعُولٌ, أَفْعَالٌ, فِعَالٌ) but broken plurals largely need to be memorized per word, unlike sound plurals.' },
        ]
      },
      {
        week: 13, pdf: 'Level-1/13th Lesson Line Spacing 2.0.pdf',
        title: { en: 'The Past Tense Verb (Al-Fi\'l Al-Madi) — Forms and Conjugations', tr: 'Geçmiş Zaman Fiili (El-Fi\'lu\'l-Mâdî) — Çekimleri', ar: 'الفعل الماضي — صيغه وتصريفاته' },
        questions: [
          { type: 'grammar', q: 'What is the base/dictionary form of an Arabic past tense verb?', expected: 'Third person masculine singular past tense: e.g. كَتَبَ (he wrote), ذَهَبَ (he went)' },
          { type: 'grammar', q: 'Conjugate كَتَبَ for "she wrote" and "they (masc. pl.) wrote."', expected: 'She wrote: كَتَبَتْ (add تْ) · They wrote: كَتَبُوا (add واo)' },
          { type: 'grammar', q: 'Conjugate كَتَبَ for "I wrote" and "you (masc. sing.) wrote."', expected: 'I wrote: كَتَبْتُ · You wrote: كَتَبْتَ' },
          { type: 'translation', q: 'Translate: خَلَقَ اللَّهُ السَّمَاوَاتِ وَالْأَرْضَ', expected: 'Allah created the heavens and the earth' },
          { type: 'grammar', q: 'In the past tense, what suffix is added for "you (fem. sing.)"?', expected: 'ـتِ: كَتَبْتِ (you, feminine singular, wrote)' },
        ]
      },
      {
        week: 14, pdf: 'Level-1/14th Lesson Line Spacing 2.0.pdf',
        title: { en: 'The Present Tense Verb (Al-Fi\'l Al-Mudari\')', tr: 'Geniş Zaman Fiili (Muzari\' Fiil)', ar: 'الفعل المضارع' },
        questions: [
          { type: 'grammar', q: 'How is the present tense formed? What letters are added?', expected: 'Add prefix letters (أ، ت، ي، ن) and adjust vowels: كَتَبَ → يَكْتُبُ (he writes)' },
          { type: 'grammar', q: 'What prefix indicates "he" and what prefix indicates "I" in the present tense?', expected: 'يَـ = he; أَ = I: يَكْتُبُ (he writes), أَكْتُبُ (I write)' },
          { type: 'grammar', q: 'Conjugate يَكْتُبُ for "they (masc. pl.) write" and "we write."', expected: 'They write: يَكْتُبُونَ · We write: نَكْتُبُ' },
          { type: 'translation', q: 'Translate: يَعْلَمُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ', expected: 'He knows what is in the heavens and what is in the earth' },
          { type: 'grammar', q: 'What prefix and suffix are used for "she writes" (3rd person fem. sing.)?', expected: 'تَكْتُبُ — prefix تَـ, no suffix (same prefix as "you" masculine singular)' },
        ]
      },
    ]
  },
  {
    id: 'level2',
    title: { en: 'Level 2 — Intermediate', tr: 'Seviye 2 — Orta Seviye', ar: 'المستوى الثاني — المتوسط' },
    desc: { en: '400+ verse analyses · 500+ new words', tr: '400\'den fazla ayet tahlili · 500\'den fazla yeni kelime', ar: 'تحليل أكثر من ٤٠٠ آية · أكثر من ٥٠٠ كلمة جديدة' },
    lessons: [
      {
        week: 1, pdf: 'Level-2/15th Lesson Line Spacing 2.0.pdf',
        title: { en: 'The Imperative: Direct Command (Amr), Lam al-Amr (Third-Person Command), Amma, and Lam al-Ibtida\'', tr: 'Emir Fiili: Doğrudan Emir (Emr-i Hâzır), Lâmu\'l-Emir (Emr-i Gâib), Emmâ ve Lâmu\'l-İbtidâ', ar: 'الأمر: فعل الأمر، لام الأمر، أمَّا، ولام الابتداء' },
        questions: [
          { type: 'grammar', q: 'How is the imperative (فعل أمر) formed from the present tense?', expected: 'Take the jussive form, remove the يَـ prefix, and add a helping hamza if needed: يَكْتُبُ → يَكْتُبْ → اُكْتُبْ (Write!)' },
          { type: 'translation', q: 'Translate: اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ', expected: 'Read in the name of your Lord who created (Surah Al-Alaq 96:1)' },
          { type: 'grammar', q: 'What is the difference between Emr-i Hazır (direct imperative) and Emr-i Gaib (3rd person command)?', expected: 'Emr-i Hazır directly addresses "you": اكْتُبْ (Write!). Emr-i Gaib uses لِـ + jussive: لِيَكْتُبْ (Let him write!)' },
          { type: 'grammar', q: 'What is لام الابتداء (Lam al-Ibtida) and what effect does it have?', expected: 'An emphatic لـ at the start of a sentence for emphasis — it does not change the case of the following word' },
          { type: 'translation', q: 'Give the imperative (command form) of the verb ذَهَبَ/يَذْهَبُ.', expected: 'اِذْهَبْ (Go!)' },
        ]
      },
      {
        week: 2, pdf: 'Level-2/16th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Prohibition (Nahiy) and Active Participle (Ism al-Fa\'il)', tr: 'Nehiy ve İsm-i Fâil', ar: 'النهي واسم الفاعل' },
        questions: [
          { type: 'grammar', q: 'How is prohibition (نهي) formed in Arabic?', expected: 'لَا + jussive present tense: لَا تَكْتُبْ (Don\'t write!), لَا تَقْرَبُوا (Don\'t approach — plural)' },
          { type: 'grammar', q: 'What is the pattern for the active participle (اسم الفاعل) of Form I verbs?', expected: 'Pattern: فَاعِلٌ — e.g. كَتَبَ → كَاتِبٌ (writer), قَرَأَ → قَارِئٌ (reader)' },
          { type: 'vocabulary', q: 'What is the active participle of عَلِمَ (to know)?', expected: 'عَالِمٌ (one who knows/scholar) — pattern فَاعِلٌ' },
          { type: 'translation', q: 'Translate: لَا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا', expected: 'Do not grieve — indeed Allah is with us (Surah At-Tawbah 9:40)' },
          { type: 'grammar', q: 'What is the active participle of رَحِمَ (to have mercy)?', expected: 'رَاحِمٌ (one who is merciful) — pattern فَاعِلٌ. Note: الرَّحِيمُ is an intensive form (صيغة مبالغة), not the regular participle.' },
        ]
      },
      {
        week: 3, pdf: 'Level-2/17th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Case Endings (I\'rab) for Nouns', tr: 'İsimlerde İ\'rab (Hâl Ekleri)', ar: 'عَلامات الإعراب في الأسماء' },
        questions: [
          { type: 'grammar', q: 'What are the three grammatical cases (إعراب) in Arabic and their vowel markers?', expected: 'Nominative (رفع) = ضمة (ـُ) · Accusative (نصب) = فتحة (ـَ) · Genitive (جر) = كسرة (ـِ)' },
          { type: 'grammar', q: 'What case does a noun take as subject of a nominal sentence (مبتدأ)?', expected: 'Nominative (مرفوع) — marked by damma (ـُ)' },
          { type: 'grammar', q: 'What is صيغة المبالغة (intensive/hyperbolic adjective)? Give two Quranic examples.', expected: 'A pattern expressing intensity beyond the regular active participle. Common patterns: فَعُولٌ, فَعَّالٌ, فَعِيلٌ. Examples: غَفُورٌ (very forgiving), عَلِيمٌ (all-knowing), رَحِيمٌ (especially merciful)' },
          { type: 'grammar', q: 'What case does the object (مفعول به) of a verb take?', expected: 'Accusative (منصوب) — marked by fatha (ـَ): كَتَبَ الطَّالِبُ الدَّرْسَ — الدَّرْسَ is accusative' },
          { type: 'vocabulary', q: 'What is the intensive form of كَثِيرٌ (many) seen in the Quran?', expected: 'كَثِيرٌ itself is already an intensive pattern. Related: the Quran uses كَثِيرٌ frequently to mean "a great many"' },
        ]
      },
      {
        week: 4, pdf: 'Level-2/18th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Verbal Sentence (Jumlah Fi\'liyya) and Intensive Adjective Forms (Siyagh al-Mubalaghah)', tr: 'Fiil Cümlesi ve Mübalağa Sıfatları', ar: 'الجملة الفعلية وصيغ المبالغة' },
        questions: [
          { type: 'grammar', q: 'What are the essential components of a verbal sentence (جملة فعلية)?', expected: 'Verb (فعل) + Subject/Doer (فاعل). The object (مفعول به) is optional.' },
          { type: 'grammar', q: 'In a verbal sentence, what case does the فاعل (subject/doer) take?', expected: 'Nominative (مرفوع)' },
          { type: 'grammar', q: 'When a verb comes before a plural subject in Arabic, does the verb agree in number?', expected: 'No — the verb stays singular (agrees only in gender) when it precedes the subject: كَتَبَ الطُّلَّابُ (The students wrote — verb is singular)' },
          { type: 'translation', q: 'Translate: خَلَقَ اللَّهُ الْإِنْسَانَ مِنْ عَلَقٍ', expected: 'Allah created mankind from a clinging clot (Surah Al-Alaq 96:2)' },
          { type: 'grammar', q: 'Identify verb, fa\'il, and maf\'ul in: عَلَّمَ اللَّهُ الْإِنْسَانَ مَا لَمْ يَعْلَمْ', expected: 'Verb: عَلَّمَ · Fa\'il: اللَّهُ (nominative) · Maf\'ul: الْإِنْسَانَ (accusative)' },
        ]
      },
      {
        week: 5, pdf: 'Level-2/19th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Types of مَا / Future Tense Particles (س and سوف)', tr: 'مَا\'nın Çeşitleri / Gelecek Zaman Edatları (س ve سوف)', ar: 'أنواع مَا / (س) و(سوف) للزمن المستقبل' },
        questions: [
          { type: 'grammar', q: 'What are the main types of لا in Arabic and their functions?', expected: 'لا النافية (negation of verbs): لا يَعْلَمُ · لا الناهية (prohibition) + jussive · لا النافية للجنس (total negation of nouns): لا إِلَهَ إِلَّا اللَّهُ' },
          { type: 'grammar', q: 'How do سَـ and سَوْفَ differ when indicating the future?', expected: 'Both mean "will/shall". سَـ is a short attached prefix for near future; سَوْفَ is a separate word, more emphatic, often for distant or certain future.' },
          { type: 'translation', q: 'Translate: سَيَقُولُ السُّفَهَاءُ', expected: 'The foolish ones will say (Surah Al-Baqarah 2:142 — سَ prefix = near future)' },
          { type: 'grammar', q: 'In لَا إِلَهَ إِلَّا اللَّهُ, what type of لا is used and what case does إِلَهَ take?', expected: 'لا النافية للجنس (total negation لا). إِلَهَ takes accusative/fatha (as اسم لا النافية للجنس).' },
          { type: 'translation', q: 'Translate: وَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَى', expected: 'And your Lord will give to you and you will be satisfied (Surah Ad-Duha 93:5)' },
        ]
      },
      {
        week: 6, pdf: 'Level-2/20th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Negation Particles: لَيْسَ, مَا, and لَا (Negating Verbal and Nominal Sentences)', tr: 'Olumsuzluk Edatları: لَيْسَ / مَا / لَا ile Fiil ve İsim Cümlelerinin Olumsuzlanması', ar: 'أدوات النفي: لَيْسَ وَمَا وَلَا في الجملة الفعلية والاسمية' },
        questions: [
          { type: 'grammar', q: 'How does لَيْسَ work grammatically?', expected: 'Like كَانَ: subject takes nominative (اسم ليس), predicate takes accusative (خبر ليس): لَيْسَ اللَّهُ غَافِلًا — اللَّهُ nominative, غَافِلًا accusative' },
          { type: 'translation', q: 'Translate: لَيْسَ كَمِثْلِهِ شَيْءٌ', expected: 'There is nothing like Him (Surah Ash-Shura 42:11)' },
          { type: 'grammar', q: 'How is مَا used for negation and what tense does it typically negate?', expected: 'مَا negates past or present: مَا كَتَبَ = he did not write · مَا يَعْلَمُ = he does not know' },
          { type: 'grammar', q: 'What is the difference between لَيْسَ and لَا for negation?', expected: 'لَيْسَ is a verb ("is not") affecting cases; لَا simply negates verbs or uses the lā-of-genus construction for nouns' },
          { type: 'translation', q: 'Translate: مَا هَذَا بَشَرًا', expected: 'This is not a human being (Surah Yusuf 12:31 — بَشَرًا accusative as خبر ما)' },
        ]
      },
      {
        week: 7, pdf: 'Level-2/21st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Particles That Put the Muḍāriʿ (Present/Future) Verb in the Subjunctive (Manṣūb) Case', tr: 'Geniş Zaman Fiilini Mansûb Yapan Edatlar (Nâsıblar)', ar: 'أدوات نصب الفعل المضارع' },
        questions: [
          { type: 'grammar', q: 'Which particles put the present tense in the subjunctive (منصوب) mood?', expected: 'أَنْ (to/that), لَنْ (will not), كَيْ (in order to), حَتَّى (until/so that), لِـ (in order to)' },
          { type: 'grammar', q: 'What happens to the final ن of يَكْتُبُونَ in the subjunctive?', expected: 'It is dropped: يَكْتُبُوا (this is one sign of subjunctive in plural forms)' },
          { type: 'translation', q: 'Translate: أُرِيدُ أَنْ أَتَعَلَّمَ الْعَرَبِيَّةَ', expected: 'I want to learn Arabic (أَنْ puts أَتَعَلَّمَ in subjunctive)' },
          { type: 'grammar', q: 'What does لَنْ express and how is it different from لَا?', expected: 'لَنْ = emphatic future negation (will absolutely not), takes subjunctive: لَنْ يَنْجَحَ = he will never succeed. لَا negates present without this emphasis.' },
          { type: 'translation', q: 'Translate: جِئْتُ لِأَتَعَلَّمَ', expected: 'I came in order to learn (لِـ = in order to, puts verb in subjunctive)' },
        ]
      },
      {
        week: 8, pdf: 'Level-2/22nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Jussive Mood (Majzum): Particles That Govern It and Their Effects on the Mudari\' Verb', tr: 'Cezm Eden Edatlar ve Muzari Fiilin Meczum Hali', ar: 'أدوات جزم الفعل المضارع وأحكامها' },
        questions: [
          { type: 'grammar', q: 'Which particles put the present tense in the jussive (مجزوم) mood?', expected: 'لَمْ (did not), لَمَّا (not yet), لَا الناهية (prohibitive don\'t), لِـ (let him — 3rd person command), and conditional particles like إِنْ' },
          { type: 'grammar', q: 'What does لَمْ do and what tense does it effectively create?', expected: 'لَمْ negates and converts the present to past: لَمْ يَكْتُبْ = he did not write (past negation)' },
          { type: 'translation', q: 'Translate: لَمْ يَلِدْ وَلَمْ يُولَدْ', expected: 'He did not beget nor was He begotten (Surah Al-Ikhlas 112:3)' },
          { type: 'grammar', q: 'What happens to the final vowel of يَكْتُبُ in the jussive?', expected: 'The damma drops: يَكْتُبْ (sukun on the last root letter)' },
          { type: 'translation', q: 'Translate: لَا تَحْزَنْ وَلَا تَخَفْ', expected: 'Do not grieve and do not fear' },
        ]
      },
      {
        week: 9, pdf: 'Level-2/23rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Passive Voice: Passive Verb (Fi\'l al-Mabni lil-Majhul) and Passive Participle (Ism al-Maf\'ul)', tr: 'Edilgen Çatı: Meçhul Fiil ve İsm-i Mef\'ul', ar: 'الفعل المبني للمجهول واسم المفعول' },
        questions: [
          { type: 'grammar', q: 'How do you form the passive voice of the past tense (Form I)?', expected: 'Change the vowel pattern to فُعِلَ: كَتَبَ → كُتِبَ (it was written), خَلَقَ → خُلِقَ (was created)' },
          { type: 'grammar', q: 'How do you form the passive of the present tense?', expected: 'Change to يُفْعَلُ pattern: يَكْتُبُ → يُكْتَبُ (it is written/being written)' },
          { type: 'grammar', q: 'What is the pattern for the passive participle (اسم المفعول) of Form I?', expected: 'Pattern: مَفْعُولٌ — e.g. كَتَبَ → مَكْتُوبٌ (written), خَلَقَ → مَخْلُوقٌ (created)' },
          { type: 'translation', q: 'Translate: خُلِقَ الْإِنْسَانُ مِنْ عَجَلٍ', expected: 'Man was created of haste (Surah Al-Anbiya 21:37)' },
          { type: 'vocabulary', q: 'What is the passive participle of فَتَحَ (to open)?', expected: 'مَفْتُوحٌ (opened) — pattern مَفْعُولٌ' },
        ]
      },
      {
        week: 10, pdf: 'Level-2/24th Lesson Line Spacing 2.0.pdf',
        title: { en: 'إِنَّ and its sisters, كَانَ and its sisters, إِذْ, إِذَا, and لَمَّا', tr: 'İnne ve kardeşleri, Kâne ve kardeşleri, İz, İzâ ve Lemmâ', ar: 'إِنَّ وأخواتها وكَانَ وأخواتها وإِذْ وإِذَا ولَمَّا' },
        questions: [
          { type: 'grammar', q: 'What is the difference between إِذْ and إِذَا?', expected: 'إِذْ = "when" referring to a definite past moment; إِذَا = "when/if" referring to the future or something expected' },
          { type: 'grammar', q: 'What does لَمَّا mean and how is it used?', expected: 'With past tense: "when" (at the moment that). With present: "not yet". لَمَّا يَقْضِ = he has not yet decided' },
          { type: 'grammar', q: 'What grammatical effect does كَانَ have on the following predicate?', expected: 'كَانَ takes a subject (nominative — اسم كان) and puts the predicate in accusative (خبر كان): كَانَ اللَّهُ غَفُورًا رَحِيمًا' },
          { type: 'translation', q: 'Translate: كَانَ اللَّهُ عَلِيمًا حَكِيمًا', expected: 'Allah has always been All-Knowing, All-Wise (كَانَ here indicates eternality of Allah\'s attribute)' },
          { type: 'translation', q: 'Translate: إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ', expected: 'When the victory of Allah comes and the conquest (Surah An-Nasr 110:1)' },
        ]
      },
      {
        week: 11, pdf: 'Level-2/25th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Inna and Its Sisters / Possessive Particles (Dhū and Its Forms) / Noun Declension', tr: 'İnne ve Kardeşleri / Sahiplik Edatları (Zū ve Çekimleri) / İsim Çekimi', ar: 'إِنَّ وأخواتها / أسماء الملكية (ذو وتصريفاتها) / إعراب الأسماء' },
        questions: [
          { type: 'grammar', q: 'What are the "sisters of إِنَّ" (إن وأخواتها) and their meanings?', expected: 'إِنَّ (indeed/verily), أَنَّ (that — subordinate), كَأَنَّ (as if), لَكِنَّ (but/however), لَيْتَ (I wish), لَعَلَّ (perhaps/hopefully)' },
          { type: 'grammar', q: 'What grammatical effect do إِنَّ and sisters have?', expected: 'They put the subject (اسم إن) in the accusative and keep the predicate (خبر إن) in the nominative: إِنَّ اللَّهَ (acc.) غَفُورٌ (nom.)' },
          { type: 'translation', q: 'Translate: إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ', expected: 'Indeed Allah is All-Forgiving, Most Merciful' },
          { type: 'grammar', q: 'What particles express possession in Arabic?', expected: 'لِـ (belonging to), عِنْدَ (with/at — physical possession), لَدَى (with — more literary), مَعَ (with — accompaniment)' },
          { type: 'translation', q: 'Translate: لَيْتَنِي كُنْتُ تُرَابًا', expected: 'I wish I were dust! (Surah An-Naba 78:40 — لَيْتَ expresses a wish)' },
        ]
      },
      {
        week: 12, pdf: 'Level-2/26th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Kāna and Its Sisters / Restriction with إِنْ...إِلَّا and مَا...إِلَّا / Conjunctions وَ، فَ، ثُمَّ', tr: 'Kâne ve Kardeşleri / İn...İllâ ve Mâ...İllâ ile Hasır / Bağlaçlar وَ، فَ، ثُمَّ', ar: 'كَانَ وَأَخَوَاتُهَا / الْحَصْرُ بِإِنْ...إِلَّا وَمَا...إِلَّا / حُرُوفُ الْعَطْفِ وَ، فَ، ثُمَّ' },
        questions: [
          { type: 'grammar', q: 'Name five sisters of كَانَ and their meanings.', expected: 'أَصْبَحَ (became in morning/became), أَمْسَى (became in evening), صَارَ (became), ظَلَّ (remained), لَيْسَ (is not), مَازَالَ (still is), بَاتَ (spent the night)' },
          { type: 'grammar', q: 'What is the grammatical rule of أَمَّا...فَـ?', expected: 'أَمَّا introduces a topic; فَـ is obligatory before the comment/result. Structure: أَمَّا [topic] فَـ [comment]: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ' },
          { type: 'translation', q: 'Translate: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ · وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ', expected: 'As for the orphan, do not oppress him · And as for the beggar, do not rebuke him (Surah Ad-Duha 93:9-10)' },
          { type: 'grammar', q: 'What does صَارَ indicate that is different from كَانَ?', expected: 'صَارَ indicates a transition/change of state (he became): صَارَ الطَّالِبُ عَالِمًا = The student became a scholar. كَانَ just describes a past state.' },
          { type: 'translation', q: 'Translate: وَكَانَ اللَّهُ بِكُلِّ شَيْءٍ عَلِيمًا', expected: 'And Allah is ever All-Knowing of everything (Surah Al-Ahzab 33:40)' },
        ]
      },
      {
        week: 13, pdf: 'Level-2/27th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Question Particles, Plural Idafa (Sound Masculine Plural in Genitive Construction), and Vocative Particles (Nida)', tr: 'Soru Edatları, Çoğul İsim Tamlamaları (Eril Çoğul İdafe) ve Nida (Seslenme) Edatları', ar: 'أدوات الاستفهام وإضافة جمع المذكر السالم وأسلوب النداء' },
        questions: [
          { type: 'grammar', q: 'What is the difference between هَلْ and أَ as question particles?', expected: 'Both ask yes/no questions. هَلْ is neutral; أَ can express rhetorical questions, surprise, or disbelief' },
          { type: 'vocabulary', q: 'What do the question words مَنْ, مَا, أَيْنَ, مَتَى, كَيْفَ, كَمْ mean?', expected: 'مَنْ = who · مَا = what · أَيْنَ = where · مَتَى = when · كَيْفَ = how · كَمْ = how many' },
          { type: 'grammar', q: 'What is the vocative particle (حرف النداء) and what case follows it?', expected: 'يَا (O!) — the addressed noun takes nominative with ال if it\'s a defined noun: يَا أَيُّهَا النَّاسُ (O Mankind!)' },
          { type: 'translation', q: 'Translate: يَا أَيُّهَا الَّذِينَ آمَنُوا', expected: 'O you who have believed! (common Quranic address to believers)' },
          { type: 'grammar', q: 'Translate this question and identify the question word: أَيْنَ تَذْهَبُونَ؟', expected: 'Where are you going? — أَيْنَ = where (adverb of place)' },
        ]
      },
      {
        week: 14, pdf: 'Level-2/28th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Comparative/Superlative (Ism al-Tafdil) and Exclamatory Expression (Uslub al-Ta\'ajjub)', tr: 'İsm-i Tafdil ve Ta\'accub Üslubu', ar: 'اسم التفضيل وأسلوب التعجب' },
        questions: [
          { type: 'grammar', q: 'What is the pattern for the comparative/superlative (اسم التفضيل)?', expected: 'Pattern: أَفْعَلُ — e.g. كَبِيرٌ → أَكْبَرُ (bigger/greatest), كَرِيمٌ → أَكْرَمُ (more/most generous)' },
          { type: 'translation', q: 'Translate: اللَّهُ أَكْبَرُ', expected: 'Allah is the Greatest (superlative — اسم التفضيل)' },
          { type: 'grammar', q: 'What are the two patterns for expressing astonishment (تعجب) in Arabic?', expected: '1) مَا أَفْعَلَهُ!: مَا أَجْمَلَ السَّمَاءَ! (How beautiful the sky is!) 2) أَفْعِلْ بِهِ!: أَكْرِمْ بِهِ! (How noble he is!)' },
          { type: 'translation', q: 'Translate: إِنَّ أَكْرَمَكُمْ عِنْدَ اللَّهِ أَتْقَاكُمْ', expected: 'Indeed the most noble of you in the sight of Allah is the most righteous of you (Surah Al-Hujurat 49:13)' },
          { type: 'grammar', q: 'What is the comparative/superlative of قَرِيبٌ (near)?', expected: 'أَقْرَبُ (nearer/nearest) — Quranic: وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ' },
        ]
      },
    ]
  },
  {
    id: 'level3',
    title: { en: 'Level 3 — Advanced', tr: 'Seviye 3 — İleri Seviye', ar: 'المستوى الثالث — المتقدم' },
    desc: { en: '450+ verse analyses · 500+ new words', tr: '450\'den fazla ayet tahlili · 500\'den fazla yeni kelime', ar: 'تحليل أكثر من ٤٥٠ آية · أكثر من ٥٠٠ كلمة جديدة' },
    lessons: [
      {
        week: 1, pdf: 'Level-3/29th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Types of Verbal Nouns (Masdar)', tr: 'Masdar Çeşitleri', ar: 'أنواع المصادر' },
        questions: [
          { type: 'grammar', q: 'What is a Masdar (مصدر) and what role does it play in Arabic grammar?', expected: 'A verbal noun expressing the action abstractly. It can be subject, object, or modifier: الضَّرْبُ حَرَامٌ (Hitting is forbidden)' },
          { type: 'grammar', q: 'What is the Masdar Mimi (مصدر ميمي) and what is its pattern?', expected: 'A verbal noun beginning with م: pattern مَفْعَلٌ or مَفْعِلٌ — e.g. مَكْتَبٌ (desk/office, from writing), مَذْهَبٌ (school of thought, from going)' },
          { type: 'vocabulary', q: 'What is the masdar of ذَهَبَ (to go)?', expected: 'ذَهَابٌ (going/departure)' },
          { type: 'grammar', q: 'What is أَنْ المصدرية and how does it function?', expected: 'أَنْ + subjunctive verb = verbal noun equivalent: أُرِيدُ أَنْ أَكْتُبَ = أُرِيدُ الْكِتَابَةَ (I want writing/to write)' },
          { type: 'translation', q: 'Translate: وَأَنْ تَصُومُوا خَيْرٌ لَكُمْ', expected: 'And that you fast is better for you (Surah Al-Baqarah 2:184 — أَنْ تَصُومُوا = a masdar-like clause = "your fasting")' },
        ]
      },
      {
        week: 2, pdf: 'Level-3/30th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Nouns of Time and Place, Instrument Nouns, Attributive Adjective (Nisba), Diminutive, and Similative Participle', tr: 'İsmi Zaman ve Mekân, İsmi Âlet, İsmi Mensûb, Tasgîr ve Sıfat-ı Müşebbehe', ar: 'اسم الزمان والمكان، اسم الآلة، الاسم المنسوب، التصغير، والصفة المشبهة' },
        questions: [
          { type: 'grammar', q: 'What are the patterns for the noun of time/place (اسم الزمان والمكان)?', expected: 'مَفْعَلٌ or مَفْعِلٌ: مَسْجِدٌ (place of prostration), مَطْلَعٌ (time of rising), مَدْخَلٌ (entrance)' },
          { type: 'grammar', q: 'What is the noun of instrument (اسم الآلة) and its patterns?', expected: 'A noun for the tool of an action. Patterns: مِفْعَلٌ, مِفْعَالٌ, مِفْعَلَةٌ — examples: مِفْتَاحٌ (key), مِيزَانٌ (scale), مِكْنَسَةٌ (broom)' },
          { type: 'grammar', q: 'What is a Nisba adjective (اسم المنسوب) and how is it formed?', expected: 'An adjective of relation/attribution: add ـِيٌّ to the noun: عَرَبٌ → عَرَبِيٌّ (Arabic), إِسْلَامٌ → إِسْلَامِيٌّ (Islamic)' },
          { type: 'grammar', q: 'What is the diminutive (تصغير) and what is its basic pattern?', expected: 'Expresses smallness or endearment. Basic pattern: فُعَيْلٌ — e.g. كَلْبٌ → كُلَيْبٌ (little dog), كِتَابٌ → كُتَيِّبٌ (booklet)' },
          { type: 'vocabulary', q: 'What does مَشْرِقٌ mean and what type of noun is it?', expected: 'مَشْرِقٌ = the East / place of sunrise — it is an اسم مكان (noun of place), from شَرَقَ (to rise/shine)' },
        ]
      },
      {
        week: 3, pdf: 'Level-3/31st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Introduction to Defective Verbs (Fi\'l Mu\'tall) — Classification of Sound and Weak Verbs', tr: 'İlletli Fiillere Giriş — Sahih ve Mu\'tell Fiillerin Sınıflandırılması', ar: 'مقدمة في الفعل المعتل — تصنيف الأفعال الصحيحة والمعتلة' },
        questions: [
          { type: 'grammar', q: 'What is the Sifat Mushabbaha (الصفة المشبهة) and how does it differ from the active participle?', expected: 'It expresses a permanent or inherent quality (not a temporary action). Pattern: فَعِيلٌ, فَعِلٌ, فَعْلَانٌ etc. — e.g. كَرِيمٌ (generous by nature), حَسَنٌ (beautiful/good)' },
          { type: 'grammar', q: 'What makes a verb "defective" (فعل معتل / illetli fiil)?', expected: 'Having a weak letter (حرف علة) — و، ا، ي — in one of the three root positions' },
          { type: 'grammar', q: 'What are the three types of defective verbs?', expected: 'Mithal (مثال): weak first letter — وَقَفَ · Ajwaf (أجوف): weak middle letter — قَالَ، بَاعَ · Naqis (ناقص): weak final letter — دَعَا، رَمَى' },
          { type: 'vocabulary', q: 'Is قَالَ a defective verb? What type and what is its root?', expected: 'Yes — Ajwaf (weak middle letter). Root: ق-و-ل. The و becomes ا in the past: قَالَ (he said)' },
          { type: 'grammar', q: 'Give two Quranic examples of Sifat Mushabbaha adjectives.', expected: 'كَرِيمٌ (noble/generous), عَظِيمٌ (great), حَكِيمٌ (wise), جَمِيلٌ (beautiful), قَوِيٌّ (strong)' },
        ]
      },
      {
        week: 4, pdf: 'Level-3/32nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Conjugation of Defective Verbs (Past Tense) — All Weak Verb Types', tr: 'İlletli Fiillerin Çekimi (Mazi) — Tüm Zayıf Fiil Türleri', ar: 'تصريف الأفعال المعتلة في الماضي — جميع الأنواع' },
        questions: [
          { type: 'grammar', q: 'In the Ajwaf verb قَالَ, what happens to the weak middle letter in the jussive?', expected: 'It drops: لَمْ يَقُلْ (the و drops and the ق gets a sukun)' },
          { type: 'grammar', q: 'Conjugate دَعَا (Naqis verb — he called/invited) for "she called."', expected: 'دَعَتْ (the final ا drops before تْ)' },
          { type: 'grammar', q: 'What is the jussive form of يَدْعُو (he calls)?', expected: 'يَدْعُ (the و drops in jussive): لَمْ يَدْعُ = he did not call' },
          { type: 'grammar', q: 'What happens to a Mithal verb like وَقَفَ in the imperative?', expected: 'The initial و drops: يَقِفُ → قِفْ (Stop!) — the hamzat al-wasl is also not needed since the word now starts with a consonant' },
          { type: 'translation', q: 'Translate: وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ', expected: 'And your Lord said: Call upon Me, I will respond to you (Surah Ghafir 40:60)' },
        ]
      },
      {
        week: 5, pdf: 'Level-3/33rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Defective Verbs: Full Conjugation Tables (Imperfect, Imperative, Negation with لَنْ and لا)', tr: 'İlletli Fiiller: Tam Çekim Tabloları (Muzari, Emir, لَنْ ve لا ile Olumsuzluk)', ar: 'الأفعال المعتلة: جداول التصريف الكاملة (مضارع، أمر، النفي بلَنْ ولا)' },
        questions: [
          { type: 'grammar', q: 'Conjugate جَاءَ (he came) for "they (masc. pl.) came."', expected: 'جَاؤُوا (the ء is retained, و added for plural)' },
          { type: 'grammar', q: 'What is the passive of قَالَ (he said)?', expected: 'قِيلَ (it was said) — the vowel pattern changes to فِيلَ for Ajwaf passives' },
          { type: 'grammar', q: 'What is the passive of بَاعَ (he sold)?', expected: 'بِيعَ (it was sold) — same فِيلَ pattern for Ajwaf' },
          { type: 'translation', q: 'Translate: وَقِيلَ يَا أَرْضُ ابْلَعِي مَاءَكِ', expected: 'And it was said: O earth, swallow your water (Surah Hud 11:44 — قِيلَ = passive of قَالَ)' },
          { type: 'grammar', q: 'What is the jussive of يَرَى (he sees — Naqis)?', expected: 'يَرَ (the final ى drops): لَمْ يَرَ = he did not see' },
        ]
      },
      {
        week: 6, pdf: 'Level-3/34th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Conditional Sentences and Conditional Particles in Arabic', tr: 'Şart Cümlesi ve Şart Edatları', ar: 'أسلوب الشرط وأدواته' },
        questions: [
          { type: 'grammar', q: 'What are the two parts of a conditional sentence in Arabic?', expected: 'Condition (شرط / protasis) and result (جواب الشرط / apodosis). Both verbs are typically jussive.' },
          { type: 'grammar', q: 'What is the difference between إِنْ and إِذَا in conditionals?', expected: 'إِنْ = for uncertain/hypothetical conditions · إِذَا = for expected/likely conditions. Both are followed by jussive or past verb.' },
          { type: 'vocabulary', q: 'What do the conditional particles مَنْ, مَا, أَيْنَمَا, مَتَى mean?', expected: 'مَنْ = whoever · مَا = whatever · أَيْنَمَا = wherever · مَتَى = whenever' },
          { type: 'translation', q: 'Translate: مَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ', expected: 'Whoever does an atom\'s weight of good will see it (Surah Az-Zalzalah 99:7)' },
          { type: 'grammar', q: 'When is فَـ required at the start of the result clause (جواب الشرط)?', expected: 'When the result clause is a nominal sentence, imperative, negative لا/لن/لم, or begins with قَدْ or سَـ/سَوْفَ' },
        ]
      },
      {
        week: 7, pdf: 'Level-3/35th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Circumstantial Accusative (Hal) and Specification (Tamyiz)', tr: 'Hal ve Temyiz', ar: 'الحال والتمييز' },
        questions: [
          { type: 'grammar', q: 'What is the Hal (الحال) and what case does it take?', expected: 'A noun/adjective/clause in the accusative describing the state of the doer or object when the action occurs. Takes accusative (منصوب).' },
          { type: 'translation', q: 'Translate and identify the Hal: جَاءَ زَيْدٌ رَاكِبًا', expected: 'Zayd came riding. رَاكِبًا = Hal (accusative) describing Zayd\'s state when he came.' },
          { type: 'grammar', q: 'What is the Tamyiz (التمييز) and what case does it take?', expected: 'A noun in the accusative specifying/clarifying a vague number, measure, or comparison. Takes accusative: عِشْرُونَ كِتَابًا = twenty books' },
          { type: 'translation', q: 'Translate: خُلِقَ الْإِنْسَانُ ضَعِيفًا', expected: 'Man was created weak (ضَعِيفًا = Hal — accusative — describing man\'s state at creation) (Surah An-Nisa 4:28)' },
          { type: 'grammar', q: 'What is the difference between Hal and Khabar?', expected: 'Hal is temporary — it describes the subject\'s state during the action. Khabar is a permanent/general predicate of the subject.' },
        ]
      },
      {
        week: 8, pdf: 'Level-3/36th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Arabic Cardinal Numbers (al-ʿAdad wa-l-Maʿdūd) and Apposition (al-Badal)', tr: 'Arapça Sayılar (el-Aded ve\'l-Ma\'dûd) ve Bedel', ar: 'العدد والمعدود والبدل' },
        questions: [
          { type: 'grammar', q: 'What is the Badal (البدل — apposition) and what is its grammatical rule?', expected: 'A noun that substitutes or clarifies the preceding noun (مبدل منه) and must agree with it in case: جَاءَ أَخُوكَ زَيْدٌ = Your brother Zayd came (زَيْدٌ = badal, nominative like أَخُوكَ)' },
          { type: 'grammar', q: 'What is the gender rule for Arabic numbers 3–10?', expected: 'Numbers 3–10 take the opposite gender of the counted noun: ثَلَاثَةُ كُتُبٍ (three books — كُتُب is masculine, so number takes feminine ة)' },
          { type: 'grammar', q: 'What case does the counted noun take after numbers 3–10?', expected: 'Genitive plural (مجرور جمع): ثَلَاثَةُ كُتُبٍ = three books' },
          { type: 'translation', q: 'Translate: إِنَّ عِدَّةَ الشُّهُورِ عِنْدَ اللَّهِ اثْنَا عَشَرَ شَهْرًا', expected: 'Indeed the number of months with Allah is twelve months (Surah At-Tawbah 9:36)' },
          { type: 'grammar', q: 'What case does the counted noun take after numbers 11–99?', expected: 'Accusative singular (تمييز منصوب): عِشْرُونَ كِتَابًا = twenty books' },
        ]
      },
      {
        week: 9, pdf: 'Level-3/37th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Diptote Nouns (Al-Mamnu\' min al-Sarf / Ghayrul Munsarif)', tr: 'Gayri Munsarif İsimler (Ğayrul Munsarif)', ar: 'الممنوع من الصرف' },
        questions: [
          { type: 'grammar', q: 'What is a Ghayrul Munsarif (diptote) noun and how does it differ from regular nouns?', expected: 'A noun that does not accept tanwin and uses fatha instead of kasra in the genitive case: مَرَرْتُ بِمَسَاجِدَ (not مَسَاجِدِ)' },
          { type: 'grammar', q: 'Name four conditions that make a noun a diptote.', expected: 'Any two conditions combine: proper name, feminine ending, foreign origin, adjective pattern أَفْعَل, broken plural on مَفَاعِل/مَفَاعِيل, added alif-nun (عُثْمَانُ)' },
          { type: 'vocabulary', q: 'Why is مَسَاجِدُ a diptote? Give its genitive form in a sentence.', expected: 'It is a broken plural on the مَفَاعِل pattern. Genitive: مَرَرْتُ بِمَسَاجِدَ كَثِيرَةٍ (I passed by many mosques — fatha not kasra)' },
          { type: 'grammar', q: 'When does a diptote noun accept tanwin and kasra?', expected: 'When it has ال (definite article) or is in an idafa (genitive construction): فِي الْمَسَاجِدِ (with ال) / مَسَاجِدُ الْمَدِينَةِ (in idafa)' },
          { type: 'translation', q: 'Translate: لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ', expected: 'We have certainly created man in the best of forms (Surah At-Tin 95:4 — أَحْسَنِ is diptote but has kasra here because it is in idafa)' },
        ]
      },
      {
        week: 10, pdf: 'Level-3/38th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Declinable & Indeclinable Words (Mu\'rab & Mabni) and Relative Pronouns (Ism al-Mawsul)', tr: 'Mebni ve Mu\'rab Kelimeler ile İsm-i Mevsul', ar: 'المبني والمعرب والأسماء الموصولة' },
        questions: [
          { type: 'grammar', q: 'What is the difference between Mabni (مبني) and Mu\'rab (معرب) words?', expected: 'Mu\'rab words change their ending to show grammatical case. Mabni words have fixed endings regardless of their role: pronouns, demonstratives, relative pronouns are mabni.' },
          { type: 'vocabulary', q: 'What are the main relative pronouns (أسماء موصولة) in Arabic?', expected: 'الَّذِي (masc. sing.), الَّتِي (fem. sing.), الَّذِينَ (masc. pl.), اللَّاتِي / اللَّوَاتِي (fem. pl.), مَنْ (whoever), مَا (whatever)' },
          { type: 'grammar', q: 'What must every relative pronoun be followed by?', expected: 'A relative clause (صلة الموصول) that contains a pronoun (عائد) referring back to the relative pronoun: الَّذِي كَتَبَ الْكِتَابَ = the one who wrote the book (هُوَ implied)' },
          { type: 'translation', q: 'Translate: الَّذِي خَلَقَ فَسَوَّى', expected: 'The One who created and proportioned (Surah Al-A\'la 87:2)' },
          { type: 'grammar', q: 'Why is الَّذِي considered mabni (indeclinable)?', expected: 'Its ending does not change regardless of its grammatical role: رَأَيْتُ الَّذِي كَتَبَ (object) vs. جَاءَ الَّذِي كَتَبَ (subject) — الَّذِي stays the same.' },
        ]
      },
      {
        week: 11, pdf: 'Level-3/39th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Exception (Istithna) and Absolute Object (Maf\'ul Mutlaq)', tr: 'İstisna ve Mef\'ul Mutlak', ar: 'الاستثناء والمفعول المطلق' },
        questions: [
          { type: 'grammar', q: 'What particle introduces exception (استثناء) and what case does the exception noun typically take?', expected: 'إِلَّا (except). In a complete affirmative sentence the exception (مستثنى) takes accusative: جَاءَ الطُّلَّابُ إِلَّا زَيْدًا' },
          { type: 'translation', q: 'Translate: لَا إِلَهَ إِلَّا اللَّهُ', expected: 'There is no god except Allah (لا النافية للجنس — إِلَهَ is accusative as اسم لا; اللَّهُ is بدل or خبر)' },
          { type: 'grammar', q: 'What is the Maf\'ul Mutlaq (المفعول المطلق — absolute object) and why is it used?', expected: 'A masdar in the accusative from the same root as the verb, used for: 1) emphasis, 2) describing manner, 3) specifying number: ضَرَبَ ضَرْبًا شَدِيدًا (he struck a hard blow)' },
          { type: 'translation', q: 'Translate: وَكَلَّمَ اللَّهُ مُوسَى تَكْلِيمًا', expected: 'And Allah spoke directly to Musa (Surah An-Nisa 4:164 — تَكْلِيمًا = maf\'ul mutlaq emphasizing the directness of speech)' },
          { type: 'grammar', q: 'What are the three other exception particles besides إِلَّا?', expected: 'غَيْرُ and سِوَى (other than), خَلَا، عَدَا، حَاشَا (except — verbal exceptions)' },
        ]
      },
      {
        week: 12, pdf: 'Level-3/40th Lesson Line Spacing2.0 .pdf',
        title: { en: 'Emphasis (Tawkid): Emphatic Lam, Emphatic Nun (Nun al-Tawkid al-Thaqila and Khafifa)', tr: 'Te\'kid: Te\'kid Lamı, Te\'kid Nunu (Ağır ve Hafif Nun)', ar: 'التوكيد: لام التوكيد ونونا التوكيد الثقيلة والخفيفة' },
        questions: [
          { type: 'grammar', q: 'What is لام التوكيد (Emphatic Lam) and where is it used?', expected: 'A لـ added for emphasis, often with إِنَّ: إِنَّ اللَّهَ لَغَفُورٌ (Indeed Allah is truly All-Forgiving). Also used in oaths.' },
          { type: 'grammar', q: 'What is نون التوكيد (Emphatic Nun) and its two forms?', expected: 'Heavy ن (ـَنَّ) and light ن (ـَنْ) added to verbs for emphasis, often after oaths: وَاللَّهِ لَأَكْتُبَنَّ = By Allah I will surely write' },
          { type: 'translation', q: 'Translate: وَإِنَّ رَبَّكَ لَذُو فَضْلٍ عَلَى النَّاسِ', expected: 'And indeed your Lord is full of bounty for the people (Surah An-Naml 27:73 — لَـ + إِنَّ = double emphasis)' },
          { type: 'grammar', q: 'What is the effect of combining إِنَّ and لَـ together?', expected: 'Double emphasis: إِنَّكَ لَعَلَى خُلُقٍ عَظِيمٍ = And indeed you are truly of great character (two emphatic particles)' },
          { type: 'grammar', q: 'What is tawkid with repeated nouns (التوكيد اللفظي والمعنوي)?', expected: 'Tawkid lafzi = repeating the word itself (جَاءَ جَاءَ زَيْدٌ). Tawkid ma\'nawi = using words like كُلٌّ، نَفْسٌ، عَيْنٌ: جَاءَ زَيْدٌ نَفْسُهُ (Zayd himself came)' },
        ]
      },
      {
        week: 13, pdf: 'Level-3/41st Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Augmented (Derived) Verb Forms: Triliteral with One, Two, and Three Added Letters (Forms II–V)', tr: 'Mezid Fiiller: Bir, İki ve Üç Harfle Türetilmiş Fiil Kalıpları (II–V. Bablar)', ar: 'الفعل المزيد الثلاثي بحرف وبحرفين وبثلاثة أحرف (الأبواب الثاني حتى الخامس)' },
        questions: [
          { type: 'grammar', q: 'What is the difference between a bare verb (فعل مجرد) and an augmented verb (فعل مزيد)?', expected: 'Bare verb: all letters are root letters (كَتَبَ — 3 root letters). Augmented verb: extra letters added to change meaning (كَاتَبَ، تَكَاتَبَ)' },
          { type: 'grammar', q: 'What does Form II (فَعَّلَ) typically add to the meaning?', expected: 'Causative or intensive: عَلِمَ (to know) → عَلَّمَ (to teach = cause to know); كَسَّرَ (to shatter = intensive of breaking)' },
          { type: 'grammar', q: 'What does Form III (فَاعَلَ) typically indicate?', expected: 'Mutual/reciprocal action between two parties: قَاتَلَ (to fight each other), كَاتَبَ (to correspond/write to each other), جَالَسَ (to sit with)' },
          { type: 'grammar', q: 'What does Form IV (أَفْعَلَ) typically mean?', expected: 'Causative: خَرَجَ (to go out) → أَخْرَجَ (to bring out/expel); سْلَمَ → أَسْلَمَ (to submit/become Muslim)' },
          { type: 'grammar', q: 'What does Form V (تَفَعَّلَ) typically mean in relation to Form II?', expected: 'Reflexive of Form II: عَلَّمَ (to teach) → تَعَلَّمَ (to learn = teach oneself); كَسَّرَ → تَكَسَّرَ (to be shattered)' },
        ]
      },
      {
        week: 14, pdf: 'Level-3/42nd Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Derived Verb Forms (Augmented Triliteral and Quadriliteral): Forms VII, VIII, X, and Quadriliteral Patterns', tr: 'Türetilmiş Fiil Kalıpları: VII., VIII., X. Bablar ve Dörtlü Kök Fiiller', ar: 'الفعل المجرد والفعل المزيد: الأبواب السابع والثامن والعاشر والرباعي المزيد' },
        questions: [
          { type: 'grammar', q: 'What does Form VI (تَفَاعَلَ) typically mean?', expected: 'Reflexive of Form III — mutual action between parties: تَقَاتَلَ (to fight each other), تَعَاوَنَ (to cooperate), تَكَاتَبَ (to write to each other)' },
          { type: 'grammar', q: 'What does Form VII (اِنْفَعَلَ) typically mean?', expected: 'Passive or reflexive of Form I: كَسَرَ (to break sth) → اِنْكَسَرَ (to break — intransitive/be broken); انقلب (to be overturned)' },
          { type: 'grammar', q: 'What does Form VIII (اِفْتَعَلَ) typically mean?', expected: 'Reflexive with variety of meanings: جَمَعَ → اِجْتَمَعَ (to gather/assemble), كَسَبَ → اِكْتَسَبَ (to earn/acquire), قَرَبَ → اِقْتَرَبَ (to draw near)' },
          { type: 'grammar', q: 'What does Form X (اِسْتَفْعَلَ) typically mean?', expected: 'To seek, request, or consider: غَفَرَ → اِسْتَغْفَرَ (to seek forgiveness), خَرَجَ → اِسْتَخْرَجَ (to extract), عْمَلَ → اِسْتَعْمَلَ (to use/employ)' },
          { type: 'translation', q: 'Translate: اسْتَعِينُوا بِاللَّهِ وَاصْبِرُوا', expected: 'Seek help from Allah and be patient (Surah Al-A\'raf 7:128 — اسْتَعِينُوا = Form X imperative plural of عَانَ)' },
        ]
      },
    ]
  },
];

const REFERENCE_TOPICS = [
  {
    id: 'letters',
    icon: 'ا',
    title: { en: 'Letters', tr: 'Harfler', ar: 'الحروف' },
    desc: { en: 'The 28 letters with their forms, vowel marks (harakat), and sun/moon classifications.', tr: '28 harf, harekeler ve güneş/ay harfleri.', ar: 'الحروف الثمانية والعشرون وأشكالها والحركات والحروف الشمسية والقمرية.' },
    pdfs: [
      { name: { en: 'Letters 1–10', tr: 'Harfler 1–10', ar: 'الحروف ١–١٠' }, path: 'Harfler/Harfler 1-10.pdf' },
      { name: { en: 'Letters 11–20', tr: 'Harfler 11–20', ar: 'الحروف ١١–٢٠' }, path: 'Harfler/Harfler 11-20.pdf' },
      { name: { en: 'Letters 21–25', tr: 'Harfler 21–25', ar: 'الحروف ٢١–٢٥' }, path: 'Harfler/Harfler 21-25.pdf' },
      { name: { en: 'Letters 26–30', tr: 'Harfler 26–30', ar: 'الحروف ٢٦–٣٠' }, path: 'Harfler/Harfler 26-30.pdf' },
      { name: { en: 'All Letters (Complete)', tr: 'Tüm Harfler', ar: 'جميع الحروف' }, path: 'Harfler/Harfler 1-30.pdf' },
    ]
  },
  {
    id: 'verbs',
    icon: 'ف',
    title: { en: 'Verb Lists (Fiiller)', tr: 'Fiiller', ar: 'قوائم الأفعال' },
    desc: { en: 'Top 100 most frequent Quranic verbs with roots and conjugations.', tr: 'Kuran\'da en sık geçen 100 fiil, kökleri ve çekimleriyle.', ar: 'أكثر ١٠٠ فعل تكراراً في القرآن مع جذورها وتصريفاتها.' },
    pdfs: [
      { name: { en: 'Top 100 Verbs — Set 1', tr: 'En Çok Geçen 100 Fiil (1)', ar: 'أكثر ١٠٠ فعل (١)' }, path: 'Fiiller/En Çok Geçen 100 Fiil.pdf' },
      { name: { en: 'Top 100 Verbs — Set 2', tr: 'En Çok Geçen 100 Fiil (2)', ar: 'أكثر ١٠٠ فعل (٢)' }, path: 'Fiiller/En Çok Geçen 100 Fiil_2.pdf' },
      { name: { en: 'Verbs 1–10', tr: 'Fiiller 1–10', ar: 'الأفعال ١–١٠' }, path: 'Fiiller/Fiiller 1-10.pdf' },
      { name: { en: 'Verbs 11–20', tr: 'Fiiller 11–20', ar: 'الأفعال ١١–٢٠' }, path: 'Fiiller/Fiiller 11-20.pdf' },
      { name: { en: 'Verbs 21–30', tr: 'Fiiller 21–30', ar: 'الأفعال ٢١–٣٠' }, path: 'Fiiller/Fiiller 21-30.pdf' },
      { name: { en: 'Verbs 31–40', tr: 'Fiiller 31–40', ar: 'الأفعال ٣١–٤٠' }, path: 'Fiiller/Fiiller 31-40.pdf' },
      { name: { en: 'Verbs 41–50', tr: 'Fiiller 41–50', ar: 'الأفعال ٤١–٥٠' }, path: 'Fiiller/Fiiller 41-50.pdf' },
      { name: { en: 'Verbs 51–60', tr: 'Fiiller 51–60', ar: 'الأفعال ٥١–٦٠' }, path: 'Fiiller/Fiiller 51-60.pdf' },
      { name: { en: 'Verbs 61–70', tr: 'Fiiller 61–70', ar: 'الأفعال ٦١–٧٠' }, path: 'Fiiller/Fiiller 61-70.pdf' },
      { name: { en: 'Verbs 71–80', tr: 'Fiiller 71–80', ar: 'الأفعال ٧١–٨٠' }, path: 'Fiiller/Fiiller 71-80 .pdf' },
      { name: { en: 'Verbs 81–90', tr: 'Fiiller 81–90', ar: 'الأفعال ٨١–٩٠' }, path: 'Fiiller/Fiiller 81-90.pdf' },
      { name: { en: 'Verbs 91–100', tr: 'Fiiller 91–100', ar: 'الأفعال ٩١–١٠٠' }, path: 'Fiiller/Fiiller 91-100.pdf' },
      { name: { en: 'Verb Paradigms (Bablar)', tr: 'Bablar', ar: 'أبواب الأفعال' }, path: 'Bablar/Bâblar.pdf' },
    ]
  },
  {
    id: 'nouns',
    icon: 'ن',
    title: { en: 'Noun Lists (İsimler)', tr: 'İsimler', ar: 'قوائم الأسماء' },
    desc: { en: '170 most frequent Quranic nouns with gender and plural forms.', tr: 'Kuran\'da en sık geçen 170 isim, cinsiyet ve çoğul formlarıyla.', ar: 'أكثر ١٧٠ اسماً تكراراً في القرآن مع جنسها وجمعها.' },
    pdfs: [
      { name: { en: 'All Nouns 1–170', tr: 'Tüm İsimler', ar: 'جميع الأسماء ١–١٧٠' }, path: 'Isimler/_İsimler 1-170.pdf' },
      { name: { en: 'Nouns 1–15', tr: 'İsimler 1–15', ar: 'الأسماء ١–١٥' }, path: 'Isimler/İsimler 1-15.pdf' },
      { name: { en: 'Nouns 16–30', tr: 'İsimler 16–30', ar: 'الأسماء ١٦–٣٠' }, path: 'Isimler/İsimler 16-30.pdf' },
      { name: { en: 'Nouns 31–45', tr: 'İsimler 31–45', ar: 'الأسماء ٣١–٤٥' }, path: 'Isimler/İsimler 31-45.pdf' },
      { name: { en: 'Nouns 46–60', tr: 'İsimler 46–60', ar: 'الأسماء ٤٦–٦٠' }, path: 'Isimler/İsimler 46-60.pdf' },
      { name: { en: 'Nouns 61–75', tr: 'İsimler 61–75', ar: 'الأسماء ٦١–٧٥' }, path: 'Isimler/İsimler 61-75.pdf' },
      { name: { en: 'Nouns 76–90', tr: 'İsimler 76–90', ar: 'الأسماء ٧٦–٩٠' }, path: 'Isimler/İsimler 76-90.pdf' },
      { name: { en: 'Nouns 91–105', tr: 'İsimler 91–105', ar: 'الأسماء ٩١–١٠٥' }, path: 'Isimler/İsimler 91-105.pdf' },
      { name: { en: 'Nouns 106–120', tr: 'İsimler 106–120', ar: 'الأسماء ١٠٦–١٢٠' }, path: 'Isimler/İsimler 106-120 .pdf' },
      { name: { en: 'Nouns 121–135', tr: 'İsimler 121–135', ar: 'الأسماء ١٢١–١٣٥' }, path: 'Isimler/İsimler 121-135.pdf' },
      { name: { en: 'Nouns 136–150', tr: 'İsimler 136–150', ar: 'الأسماء ١٣٦–١٥٠' }, path: 'Isimler/İsimler 136-150.pdf' },
      { name: { en: 'Nouns 151–170', tr: 'İsimler 151–170', ar: 'الأسماء ١٥١–١٧٠' }, path: 'Isimler/İsimler 151-170.pdf' },
      { name: { en: 'Top Frequency Nouns', tr: 'En Sık Geçen İsimler', ar: 'الأسماء الأكثر تكراراً' }, path: 'Nouns/Top Nouns .pdf' },
      { name: { en: 'Top Particles', tr: 'En Sık Geçen Harfler', ar: 'الحروف الأكثر تكراراً' }, path: 'Nouns/Top Particles .pdf' },
    ]
  },
  {
    id: 'words',
    icon: 'آ',
    title: { en: 'Surah Vocabulary', tr: 'Sure Kelimeleri', ar: 'مفردات السور' },
    desc: { en: 'Complete vocabulary sheets organized by Surah, plus all 42 lesson answer keys and prayer-word lists.', tr: 'Sure sure tam kelime listeleri, 42 dersin tüm cevap anahtarları ve dua kelimeleri.', ar: 'قوائم مفردات كاملة لكل سورة، إضافة إلى مفاتيح الإجابات للدروس ٤٢ وكلمات الأدعية.' },
    pdfs: [
      // ─── Surah verb vocabulary sheets ───
      { name: { en: 'Yâ-Sîn 1–40', tr: 'Yâ-Sîn 1–40', ar: 'يس ١–٤٠' }, path: 'Words/Yâ-Sîn Sûresi 1-40 Fiiller.pdf' },
      { name: { en: 'Yâ-Sîn 41–83', tr: 'Yâ-Sîn 41–83', ar: 'يس ٤١–٨٣' }, path: 'Words/Yâ-Sîn Sûresi 41-83 Fiiller.pdf' },
      { name: { en: 'Sâffât 1–76', tr: 'Sâffât 1–76', ar: 'الصافات ١–٧٦' }, path: 'Words/Sâffât Sûresi 1-76 Fiiller.pdf' },
      { name: { en: 'Sâffât 77–153', tr: 'Sâffât 77–153', ar: 'الصافات ٧٧–١٥٣' }, path: 'Words/Sâffât Sûresi 77-153 Fiiller .pdf' },
      { name: { en: 'Sâffât 154–182 · Sâd 1–26', tr: 'Sâffât 154–182 · Sâd 1–26', ar: 'الصافات ١٥٤–١٨٢ · ص ١–٢٦' }, path: 'Words/Sâffât Sûresi 154-182 Sâd Sûresi 1-26 Fiiller.pdf' },
      { name: { en: 'Sâd 27–83', tr: 'Sâd 27–83', ar: 'ص ٢٧–٨٣' }, path: 'Words/_Sâd Sûresi 27-83 Fiiller .pdf' },
      { name: { en: 'Sâd 84–88 · Zumer 1–21', tr: 'Sâd 84–88 · Zümer 1–21', ar: 'ص ٨٤–٨٨ · الزمر ١–٢١' }, path: 'Words/_Sâd Sûresi 84-88 Zumer Sûresi 1-21 Fiiller  .pdf' },
      { name: { en: 'Zumer 22–47', tr: 'Zümer 22–47', ar: 'الزمر ٢٢–٤٧' }, path: 'Words/_ Zumer Sûresi 22-47 Fiiller   .pdf' },
      { name: { en: 'Zumer 48–74', tr: 'Zümer 48–74', ar: 'الزمر ٤٨–٧٤' }, path: 'Words/_ Zumer Sûresi 48-74 Fiiller  .pdf' },
      { name: { en: 'Mu\'min 1–25', tr: 'Mü\'min 1–25', ar: 'غافر ١–٢٥' }, path: 'Words/Mu\'min Sûresi 1-25 Fiiller.pdf' },
      { name: { en: 'Mu\'min 26–49', tr: 'Mü\'min 26–49', ar: 'غافر ٢٦–٤٩' }, path: 'Words/Mu\'min Sûresi 26-49 Fiiller.pdf' },
      { name: { en: 'Mu\'min 50–77', tr: 'Mü\'min 50–77', ar: 'غافر ٥٠–٧٧' }, path: 'Words/Mu\'min Sûresi 50-77 Fiiller.pdf' },
      { name: { en: 'Mu\'min 78–85 · Fussilet 1–20', tr: 'Mü\'min 78–85 · Fussilet 1–20', ar: 'غافر ٧٨–٨٥ · فصلت ١–٢٠' }, path: 'Words/Mu\'min Sûresi 78-85 Fussilet Sûresi 1-20 Fiiller.pdf' },
      { name: { en: 'Fussilet 21–46', tr: 'Fussilet 21–46', ar: 'فصلت ٢١–٤٦' }, path: 'Words/Fussilet Sûresi 21-46 Fiiller.pdf' },
      { name: { en: 'Fussilet 47–54 · Şûrâ 1–15', tr: 'Fussilet 47–54 · Şûrâ 1–15', ar: 'فصلت ٤٧–٥٤ · الشورى ١–١٥' }, path: 'Words/Fussilet Sûresi 47-54 Şûrâ Sûresi 1-15 Fiiller.pdf' },
      { name: { en: 'Şûrâ 16–44', tr: 'Şûrâ 16–44', ar: 'الشورى ١٦–٤٤' }, path: 'Words/Şûrâ Sûresi 16-44 Fiiller.pdf' },
      { name: { en: 'Şûrâ 45–53 · Zuhruf 1–22', tr: 'Şûrâ 45–53 · Zuhruf 1–22', ar: 'الشورى ٤٥–٥٣ · الزخرف ١–٢٢' }, path: 'Words/Şûrâ Sûresi 45-53 Zuhruf Sûresi 1-22 Fiiller.pdf' },
      { name: { en: 'Zuhruf 23–60', tr: 'Zuhruf 23–60', ar: 'الزخرف ٢٣–٦٠' }, path: 'Words/_Zuhruf Sûresi 23-60 Fiiller.pdf' },
      { name: { en: 'Zuhruf 61–89 · Duhân 1–18', tr: 'Zuhruf 61–89 · Duhân 1–18', ar: 'الزخرف ٦١–٨٩ · الدخان ١–١٨' }, path: 'Words/Zuhruf Sûresi 61-89 Duhân Sûresi 1-18 Fiiller.pdf' },
      { name: { en: 'Duhân 19–59 · Câsiye 1–13', tr: 'Duhân 19–59 · Câsiye 1–13', ar: 'الدخان ١٩–٥٩ · الجاثية ١–١٣' }, path: 'Words/Duhân Sûresi 19-59 Câsiye Sûresi 1-13 Fiiller .pdf' },
      { name: { en: 'Câsiye 14–37 · Ahkâf 1–5', tr: 'Câsiye 14–37 · Ahkâf 1–5', ar: 'الجاثية ١٤–٣٧ · الأحقاف ١–٥' }, path: 'Words/Câsiye Sûresi 14-37 Ahkâf Sûresi 1-5 Fiiller.pdf' },
      { name: { en: 'Ahkâf 6–28', tr: 'Ahkâf 6–28', ar: 'الأحقاف ٦–٢٨' }, path: 'Words/Ahkâf Sûresi 6-28 Fiiller.pdf' },
      { name: { en: 'Ahkâf 29–35 · Muhammed 1–19', tr: 'Ahkâf 29–35 · Muhammed 1–19', ar: 'الأحقاف ٢٩–٣٥ · محمد ١–١٩' }, path: 'Words/Ahkâf Sûresi 29-35 Muhammed(asm) Sûresi 1-19 Fiiller.pdf' },
      { name: { en: 'Muhammed 20–38 · Fetih 1–9', tr: 'Muhammed 20–38 · Fetih 1–9', ar: 'محمد ٢٠–٣٨ · الفتح ١–٩' }, path: 'Words/Muhammed(asm) Sûresi 20-38 Fetih Sûresi 1-9 Fiiller.pdf' },
      { name: { en: 'Fetih 10–28', tr: 'Fetih 10–28', ar: 'الفتح ١٠–٢٨' }, path: 'Words/Fetih Sûresi 10-28 Fiiller.pdf' },
      { name: { en: 'Fetih 29 · Hucurât 1–18', tr: 'Fetih 29 · Hucurât 1–18', ar: 'الفتح ٢٩ · الحجرات ١–١٨' }, path: 'Words/Fetih Sûresi 29 Hucurât Sûresi 1-18 Fiiller.pdf' },
      { name: { en: 'Kâf 1–45 · Zâriyât 1–6', tr: 'Kâf 1–45 · Zâriyât 1–6', ar: 'ق ١–٤٥ · الذاريات ١–٦' }, path: 'Words/Kâf Sûresi 1-45 Zâriyât Sûresi 1-6 Fiiller.pdf' },
      { name: { en: 'Zâriyât 7–60 · Tûr 1–14', tr: 'Zâriyât 7–60 · Tûr 1–14', ar: 'الذاريات ٧–٦٠ · الطور ١–١٤' }, path: 'Words/Zâriyât Sûresi 7-60 Tûr Sûresi 1-14 Fiiller.pdf' },
      { name: { en: 'Tûr 15–49 · Necm 1–26', tr: 'Tûr 15–49 · Necm 1–26', ar: 'الطور ١٥–٤٩ · النجم ١–٢٦' }, path: 'Words/Tûr Sûresi 15-49 Necm Sûresi 1-26 Fiiller.pdf' },
      { name: { en: 'Necm 27–62 · Kamer 1–27', tr: 'Necm 27–62 · Kamer 1–27', ar: 'النجم ٢٧–٦٢ · القمر ١–٢٧' }, path: 'Words/Necm Sûresi 27-62 Kamer Sûresi 1-27 Fiiller.pdf' },
      { name: { en: 'Kamer 28–55 · Rahmân 1–40', tr: 'Kamer 28–55 · Rahmân 1–40', ar: 'القمر ٢٨–٥٥ · الرحمن ١–٤٠' }, path: 'Words/Kamer Sûresi 28-55 Rahmân Sûresi 1-40 Fiiller.pdf' },
      { name: { en: 'Rahmân 41–78 · Vâkı\'a 1–50', tr: 'Rahmân 41–78 · Vâkı\'a 1–50', ar: 'الرحمن ٤١–٧٨ · الواقعة ١–٥٠' }, path: 'Words/Rahmân Sûresi 41-78 Vâkı\'aSûresi 1-50 Fiiller.pdf' },
      { name: { en: 'Vâkı\'a 51–96 · Hadîd 1–11', tr: 'Vâkı\'a 51–96 · Hadîd 1–11', ar: 'الواقعة ٥١–٩٦ · الحديد ١–١١' }, path: 'Words/Vâkı\'a Sûresi 51-96 Hadîd Sûresi 1-11 Fiiller.pdf' },
      { name: { en: 'Hadîd 12–29', tr: 'Hadîd 12–29', ar: 'الحديد ١٢–٢٩' }, path: 'Words/Hadîd Sûresi 12-29 Fiiller .pdf' },
      { name: { en: 'Mucâdele 1–21', tr: 'Mücâdele 1–21', ar: 'المجادلة ١–٢١' }, path: 'Words/Mucadele Sûresi 1-21 Fiiller  .pdf' },
      { name: { en: 'Mucâdile 22 · Haşr 1–16', tr: 'Mücâdele 22 · Haşr 1–16', ar: 'المجادلة ٢٢ · الحشر ١–١٦' }, path: 'Words/Mucadile Sûresi 22  Haşr Sûresi 1-16 Fiiller.pdf' },
      { name: { en: 'Haşr 17–24 · Mumtehine 1–11', tr: 'Haşr 17–24 · Mumtehine 1–11', ar: 'الحشر ١٧–٢٤ · الممتحنة ١–١١' }, path: 'Words/Haşr Sûresi 17-24 Mumtehine S 1-11 Fiiller.pdf' },
      { name: { en: 'Mumtehine 12–13 · Saf 1–14 · Cum\'a 1–8', tr: 'Mumtehine 12–13 · Saf 1–14 · Cum\'a 1–8', ar: 'الممتحنة ١٢–١٣ · الصف ١–١٤ · الجمعة ١–٨' }, path: 'Words/Mumtehine Sûresi 12-13 Saf S 1-14 Cum\'a S 1-8 Fiiller.pdf' },
      { name: { en: 'Cum\'a 9–11 · Munâfikûn · Teğâbun 1–9', tr: 'Cum\'a 9–11 · Munâfikûn · Teğâbun 1–9', ar: 'الجمعة ٩–١١ · المنافقون · التغابن ١–٩' }, path: 'Words/Cum\'a Sûresi 9-11 Munâfikûn Sûresi 1-11 Teğâbun Sûresi 1-9 Fiiller.pdf' },
      { name: { en: 'Teğâbun 10–18 · Talâk 1–12', tr: 'Teğâbun 10–18 · Talâk 1–12', ar: 'التغابن ١٠–١٨ · الطلاق ١–١٢' }, path: 'Words/Teğâbun Sûresi 10-18 Talâk Sûresi 1-12 Fiiller.pdf' },
      { name: { en: 'Tahrîm 1–12 · Mülk 1–12', tr: 'Tahrîm 1–12 · Mülk 1–12', ar: 'التحريم ١–١٢ · الملك ١–١٢' }, path: 'Words/Tahrîm Sûresi 1-12 Mülk Sûresi 1-12 Fiiller.pdf' },
      { name: { en: 'Mülk 13–30 · Kalem 1–52', tr: 'Mülk 13–30 · Kalem 1–52', ar: 'الملك ١٣–٣٠ · القلم ١–٥٢' }, path: 'Words/Mülk Sûresi 13-30 Kalem S 1-52 Fiiller.pdf' },
      { name: { en: 'Kalem 43–52 · Hakka · Me\'aric 1–10', tr: 'Kalem 43–52 · Hakka · Me\'aric 1–10', ar: 'القلم ٤٣–٥٢ · الحاقة · المعارج ١–١٠' }, path: 'Words/Kalem Sûresi 43-52 Hakka S 1-52 Me\'aric S 1-10 Fiiller.pdf' },
      { name: { en: 'Me\'aric 11–44 · Nuh 1–28', tr: 'Me\'aric 11–44 · Nuh 1–28', ar: 'المعارج ١١–٤٤ · نوح ١–٢٨' }, path: 'Words/Me\'aric Sûresi 11-44 Nuh(as) S 1-28.pdf' },
      { name: { en: 'Cin 1–28 · Müzzemmil 1–20', tr: 'Cin 1–28 · Müzzemmil 1–20', ar: 'الجن ١–٢٨ · المزمل ١–٢٠' }, path: 'Words/Cin Sûresi 1-28 Müzzemmil S 1-20 Fiiller.pdf' },
      { name: { en: 'Müddessir 1–56 · Kıyâmet 1–40', tr: 'Müddessir 1–56 · Kıyâmet 1–40', ar: 'المدثر ١–٥٦ · القيامة ١–٤٠' }, path: 'Words/Müddessir Sûresi 1- 56 Kıyamet S 1-40 Fiiller.pdf' },
      { name: { en: 'İnsan 1–31 · Murselât 1–50', tr: 'İnsan 1–31 · Mürselât 1–50', ar: 'الإنسان ١–٣١ · المرسلات ١–٥٠' }, path: 'Words/İnsan Sûresi 1-31 Murselat S 1-50 Fiiller.pdf' },
      { name: { en: 'Lokmân 20–34 · Secde 1–11', tr: 'Lokmân 20–34 · Secde 1–11', ar: 'لقمان ٢٠–٣٤ · السجدة ١–١١' }, path: 'Words/Lokman Sûresi 20-34 Secde S 1-11.pdf' },
      { name: { en: 'Secde 12–30 · Ahzâb 1–6', tr: 'Secde 12–30 · Ahzâb 1–6', ar: 'السجدة ١٢–٣٠ · الأحزاب ١–٦' }, path: 'Words/Secde Sûresi 12-30 Ahzâb S 1-6.pdf' },
      { name: { en: 'Ahzâb 7–30', tr: 'Ahzâb 7–30', ar: 'الأحزاب ٧–٣٠' }, path: 'Words/Ahzâb Sûresi 7-30 Fiiller.pdf' },
      { name: { en: 'Ahzâb 31–50', tr: 'Ahzâb 31–50', ar: 'الأحزاب ٣١–٥٠' }, path: 'Words/Ahzâb Sûresi 31-50 Fiiller.pdf' },
      { name: { en: 'Ahzâb 51–73', tr: 'Ahzâb 51–73', ar: 'الأحزاب ٥١–٧٣' }, path: 'Words/Ahzâb Sûresi 51-73 Fiiller.pdf' },
      { name: { en: 'Sebe\' 1–22', tr: 'Sebe\' 1–22', ar: 'سبأ ١–٢٢' }, path: 'Words/Sebe\' Sûresi 1-22 Fiiller.pdf' },
      { name: { en: 'Sebe\' 23–48', tr: 'Sebe\' 23–48', ar: 'سبأ ٢٣–٤٨' }, path: 'Words/Sebe\' Sûresi 23-48 Fiiller.pdf' },
      { name: { en: 'Sebe\' 49–54 · Fâtır 1–18', tr: 'Sebe\' 49–54 · Fâtır 1–18', ar: 'سبأ ٤٩–٥٤ · فاطر ١–١٨' }, path: 'Words/Sebe\' Sûresi 49-54 Fâtır S 1-18 Fiiller.pdf' },
      { name: { en: 'Fâtır 19–45', tr: 'Fâtır 19–45', ar: 'فاطر ١٩–٤٥' }, path: 'Words/Fâtır Sûresi 19-45 Fiiller.pdf' },

      // ─── Lesson Answer Keys (1–42 vocabulary keys) ───
      { name: { en: 'Answer Key — Lesson 1', tr: 'Cevap Anahtarı — 1. Ders', ar: 'مفتاح الإجابة — الدرس ١' }, path: 'Words/Answer Key-1.pdf' },
      { name: { en: 'Answer Key — Lesson 2', tr: 'Cevap Anahtarı — 2. Ders', ar: 'مفتاح الإجابة — الدرس ٢' }, path: 'Words/Answer Key-2.pdf' },
      { name: { en: 'Answer Key — Lesson 3', tr: 'Cevap Anahtarı — 3. Ders', ar: 'مفتاح الإجابة — الدرس ٣' }, path: 'Words/Answer Key-3.pdf' },
      { name: { en: 'Answer Key — Lesson 4', tr: 'Cevap Anahtarı — 4. Ders', ar: 'مفتاح الإجابة — الدرس ٤' }, path: 'Words/Answer Key 4.pdf' },
      { name: { en: 'Answer Key — Lesson 5', tr: 'Cevap Anahtarı — 5. Ders', ar: 'مفتاح الإجابة — الدرس ٥' }, path: 'Words/Answer Key-5.pdf' },
      { name: { en: 'Answer Key — Lesson 6', tr: 'Cevap Anahtarı — 6. Ders', ar: 'مفتاح الإجابة — الدرس ٦' }, path: 'Words/ANSWER KEY-6.pdf' },
      { name: { en: 'Answer Key — Lesson 7', tr: 'Cevap Anahtarı — 7. Ders', ar: 'مفتاح الإجابة — الدرس ٧' }, path: 'Words/Answer Key-7.pdf' },
      { name: { en: 'Answer Key — Lesson 8', tr: 'Cevap Anahtarı — 8. Ders', ar: 'مفتاح الإجابة — الدرس ٨' }, path: 'Words/Answer Key-8.pdf' },
      { name: { en: 'Answer Key — Lesson 9', tr: 'Cevap Anahtarı — 9. Ders', ar: 'مفتاح الإجابة — الدرس ٩' }, path: 'Words/Answer Key-9.pdf' },
      { name: { en: 'Answer Key — Lesson 10', tr: 'Cevap Anahtarı — 10. Ders', ar: 'مفتاح الإجابة — الدرس ١٠' }, path: 'Words/Answer Key-10.pdf' },
      { name: { en: 'Answer Key — Lesson 11', tr: 'Cevap Anahtarı — 11. Ders', ar: 'مفتاح الإجابة — الدرس ١١' }, path: 'Words/Answer Key 11.pdf' },
      { name: { en: 'Answer Key — Lesson 15', tr: 'Cevap Anahtarı — 15. Ders', ar: 'مفتاح الإجابة — الدرس ١٥' }, path: 'Words/Answer Key-15 .pdf' },
      { name: { en: 'Answer Key — Lesson 16', tr: 'Cevap Anahtarı — 16. Ders', ar: 'مفتاح الإجابة — الدرس ١٦' }, path: 'Words/Answer Key-16.pdf' },
      { name: { en: 'Answer Key — Lesson 17', tr: 'Cevap Anahtarı — 17. Ders', ar: 'مفتاح الإجابة — الدرس ١٧' }, path: 'Words/Answer Key-17.pdf' },
      { name: { en: 'Answer Key — Lesson 18', tr: 'Cevap Anahtarı — 18. Ders', ar: 'مفتاح الإجابة — الدرس ١٨' }, path: 'Words/Answer Key-18 .pdf' },
      { name: { en: 'Answer Key — Lesson 19', tr: 'Cevap Anahtarı — 19. Ders', ar: 'مفتاح الإجابة — الدرس ١٩' }, path: 'Words/Answer Key-19.pdf' },
      { name: { en: 'Answer Key — Lesson 20', tr: 'Cevap Anahtarı — 20. Ders', ar: 'مفتاح الإجابة — الدرس ٢٠' }, path: 'Words/Answer Key-20 .pdf' },
      { name: { en: 'Answer Key — Lesson 21', tr: 'Cevap Anahtarı — 21. Ders', ar: 'مفتاح الإجابة — الدرس ٢١' }, path: 'Words/Answer Key-21 .pdf' },
      { name: { en: 'Answer Key — Lesson 22', tr: 'Cevap Anahtarı — 22. Ders', ar: 'مفتاح الإجابة — الدرس ٢٢' }, path: 'Words/Answer Key-22  .pdf' },
      { name: { en: 'Answer Key — Lesson 23', tr: 'Cevap Anahtarı — 23. Ders', ar: 'مفتاح الإجابة — الدرس ٢٣' }, path: 'Words/Answer Key-23 .pdf' },
      { name: { en: 'Answer Key — Lesson 24', tr: 'Cevap Anahtarı — 24. Ders', ar: 'مفتاح الإجابة — الدرس ٢٤' }, path: 'Words/Answer Key-24.pdf' },
      { name: { en: 'Answer Key — Lesson 25', tr: 'Cevap Anahtarı — 25. Ders', ar: 'مفتاح الإجابة — الدرس ٢٥' }, path: 'Words/Answer Key-25 .pdf' },
      { name: { en: 'Answer Key — Lesson 26', tr: 'Cevap Anahtarı — 26. Ders', ar: 'مفتاح الإجابة — الدرس ٢٦' }, path: 'Words/Answer Key-26 .pdf' },
      { name: { en: 'Answer Key — Lesson 27', tr: 'Cevap Anahtarı — 27. Ders', ar: 'مفتاح الإجابة — الدرس ٢٧' }, path: 'Words/Answer Key-27  .pdf' },
      { name: { en: 'Answer Key — Lesson 28', tr: 'Cevap Anahtarı — 28. Ders', ar: 'مفتاح الإجابة — الدرس ٢٨' }, path: 'Words/Answer Key-28 .pdf' },
      { name: { en: 'Answer Key — Lesson 29', tr: 'Cevap Anahtarı — 29. Ders', ar: 'مفتاح الإجابة — الدرس ٢٩' }, path: 'Words/Answer Key-29.pdf' },
      { name: { en: 'Answer Key — Lesson 30', tr: 'Cevap Anahtarı — 30. Ders', ar: 'مفتاح الإجابة — الدرس ٣٠' }, path: 'Words/Answer Key-30.pdf' },
      { name: { en: 'Answer Key — Lesson 31', tr: 'Cevap Anahtarı — 31. Ders', ar: 'مفتاح الإجابة — الدرس ٣١' }, path: 'Words/Answer Key-31.pdf' },
      { name: { en: 'Answer Key — Lesson 32', tr: 'Cevap Anahtarı — 32. Ders', ar: 'مفتاح الإجابة — الدرس ٣٢' }, path: 'Words/Answer Key-32.pdf' },
      { name: { en: 'Answer Key — Lesson 33', tr: 'Cevap Anahtarı — 33. Ders', ar: 'مفتاح الإجابة — الدرس ٣٣' }, path: 'Words/Answer Key-33 .pdf' },
      { name: { en: 'Answer Key — Lesson 34', tr: 'Cevap Anahtarı — 34. Ders', ar: 'مفتاح الإجابة — الدرس ٣٤' }, path: 'Words/Answer Key-34.pdf' },
      { name: { en: 'Answer Key — Lesson 35', tr: 'Cevap Anahtarı — 35. Ders', ar: 'مفتاح الإجابة — الدرس ٣٥' }, path: 'Words/Answer Key-35.pdf' },
      { name: { en: 'Answer Key — Lesson 36', tr: 'Cevap Anahtarı — 36. Ders', ar: 'مفتاح الإجابة — الدرس ٣٦' }, path: 'Words/Answer Key-36.pdf' },
      { name: { en: 'Answer Key — Lesson 37', tr: 'Cevap Anahtarı — 37. Ders', ar: 'مفتاح الإجابة — الدرس ٣٧' }, path: 'Words/Answer Key-37.pdf' },
      { name: { en: 'Answer Key — Lesson 38', tr: 'Cevap Anahtarı — 38. Ders', ar: 'مفتاح الإجابة — الدرس ٣٨' }, path: 'Words/Answer Key-38.pdf' },
      { name: { en: 'Answer Key — Lesson 39', tr: 'Cevap Anahtarı — 39. Ders', ar: 'مفتاح الإجابة — الدرس ٣٩' }, path: 'Words/Answer Key-39.pdf' },
      { name: { en: 'Answer Key — Lesson 40', tr: 'Cevap Anahtarı — 40. Ders', ar: 'مفتاح الإجابة — الدرس ٤٠' }, path: 'Words/Answer Key-40.pdf' },
      { name: { en: 'Answer Key — Lesson 41', tr: 'Cevap Anahtarı — 41. Ders', ar: 'مفتاح الإجابة — الدرس ٤١' }, path: 'Words/Answer Key-41.pdf' },
      { name: { en: 'Answer Key — Lesson 42', tr: 'Cevap Anahtarı — 42. Ders', ar: 'مفتاح الإجابة — الدرس ٤٢' }, path: 'Words/Answer Key-42.pdf' },

      // ─── Prayer-word vocabularies ───
      { name: { en: 'Prayer Words — Subhaneke & Tahiyyat', tr: 'Sübhaneke ve Tahiyyat Duaları', ar: 'كلمات التسبيح والتشهد' }, path: 'Words/Subhaneke, Tahiyyat Duaları Kelimeler.pdf' },
      { name: { en: 'Prayer Words — Salli-Bârik & Rabbenâ', tr: 'Salli-Bârik ve Rabbenâ Duaları', ar: 'كلمات الصلاة والتبريك' }, path: 'Words/Salli-Bârik ve Rabbenâ Duaları Kelimeler.pdf' },
      { name: { en: 'Prayer Words — Qunut', tr: 'Kunut Duası Kelimeleri', ar: 'كلمات دعاء القنوت' }, path: 'Words/Kunut Duaları Kelimeler.pdf' },
    ]
  },
  {
    id: 'irab',
    icon: '📖',
    irab: true,
    title: { en: 'Verse Analysis (I\'rab)', tr: 'Ayet İ\'rabı', ar: 'إعراب الآية' },
    desc: { en: 'Paste any Quranic verse to get a word-by-word grammatical analysis. Each grammar phenomenon links back to the relevant lesson in the 42-lesson curriculum.', tr: 'Kelime kelime gramer analizi için herhangi bir Kur\'an ayetini yapıştırın. Her gramer olgusu, 42 derslik müfredattaki ilgili derse bağlanır.', ar: 'الصق أي آية لتحليلها نحوياً كلمة بكلمة. كل ظاهرة نحوية مرتبطة بالدرس المعني من بين الـ ٤٢ درساً.' },
    pdfs: []
  },
  {
    id: 'vocab-quiz',
    icon: '?',
    quiz: true,
    title: { en: 'Vocabulary Quiz', tr: 'Kelime Sınavı', ar: 'اختبار المفردات' },
    desc: { en: 'Multiple-choice quiz drawn from the entire vocabulary pool extracted from all 98 vocabulary PDFs.', tr: '98 kelime PDF\'sinden çıkarılan tüm kelime havuzundan çoktan seçmeli sınav.', ar: 'اختبار اختيار من متعدد من مجمل المفردات المستخرجة من جميع ملفات الـ ٩٨ PDF.' },
    pdfs: []
  },
  {
    id: 'bablar',
    icon: 'ب',
    title: { en: 'Verb Paradigms (Bablar)', tr: 'Bâblar', ar: 'أبواب الأفعال' },
    desc: { en: 'The classical verb paradigms (forms I–X) showing how triliteral roots are conjugated across all augmented patterns.', tr: 'Klasik fiil bablarının (I–X. bablar) üç harfli kökten nasıl türetildiğini gösteren tablo.', ar: 'أبواب الأفعال الكلاسيكية (الأبواب I–X) التي تبيّن كيف تُصرَّف الجذور الثلاثية في جميع الأوزان المزيدة.' },
    pdfs: [
      { name: { en: 'Bablar — Verb Paradigms', tr: 'Bâblar', ar: 'أبواب الأفعال' }, path: 'Bablar/Bâblar.pdf' },
    ]
  },
  {
    id: 'summaries',
    icon: 'ملخص',
    title: { en: 'Lesson Summaries', tr: 'Ders Özetleri', ar: 'ملخصات الدروس' },
    desc: { en: 'Condensed grammar summaries for all three levels in Turkish and Arabic.', tr: 'Her üç seviye için Türkçe ve Arapça ders özetleri.', ar: 'ملخصات نحوية مكثفة للمستويات الثلاثة بالتركية والعربية.' },
    pdfs: [
      { name: { en: 'Level 1 Summary (Turkish)', tr: 'Seviye 1 Özeti (Türkçe)', ar: 'ملخص المستوى ١ (تركي)' }, path: 'Summary/Summary 1-14_2 satir arali.pdf' },
      { name: { en: 'Level 1 Summary (Arabic)', tr: 'Seviye 1 Özeti (Arapça)', ar: 'ملخص المستوى الأول (عربي)' }, path: 'Summary/الْمُسْتَوَى الأَوَّل (1-14).pdf' },
      { name: { en: 'Level 2 Summary (Turkish)', tr: 'Seviye 2 Özeti (Türkçe)', ar: 'ملخص المستوى ٢ (تركي)' }, path: 'Summary/Summary 15-28_2 satır aralı.pdf' },
      { name: { en: 'Level 2 Summary (Arabic)', tr: 'Seviye 2 Özeti (Arapça)', ar: 'ملخص المستوى الثاني (عربي)' }, path: 'Summary/المُسْتَوَى الثَّاني 15-28 .pdf' },
      { name: { en: 'Level 3 Summary (Turkish)', tr: 'Seviye 3 Özeti (Türkçe)', ar: 'ملخص المستوى ٣ (تركي)' }, path: 'Summary/3. Seviye Dersleri 29-42.pdf' },
      { name: { en: 'Level 3 Summary (Turkish alt)', tr: 'Seviye 3 Özeti (alternatif)', ar: 'ملخص المستوى ٣ (بديل)' }, path: 'Summary/Summary 29-42 .pdf' },
    ]
  },
];
