const LEVELS = [
  {
    id: 'level1',
    title: { en: 'Level 1 — Beginner', tr: 'Seviye 1 — Başlangıç', ar: 'المستوى الأول — المبتدئ' },
    desc: { en: '150+ verse analyses · 500+ new words', tr: '150\'den fazla ayet tahlili · 500\'den fazla yeni kelime', ar: 'تحليل أكثر من ١٥٠ آية · أكثر من ٥٠٠ كلمة جديدة' },
    lessons: [
      {
        week: 1, pdf: 'Level-1/1st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Arabic Word Types: Noun (Ism), Verb (Fiʿl), and Particle (Ḥarf)', tr: 'Arapçada Kelime Çeşitleri: İsim, Fiil ve Harf', ar: 'أقسام الكلمة: الاسم والفعل والحرف' },
        lecture: {
          sections: [
            {
              title: {
                en: 'Why classify words?',
                tr: 'Kelimeleri neden sınıflandırırız?',
                ar: 'لماذا نصنّف الكلمات؟'
              },
              body: {
                en: `Classical Arabic grammar — and therefore the language of the Qurʾān — divides every word into exactly **three categories** (أقسام الكلمة). Identifying which category a word belongs to is the very first step of i'rab (إعراب), because each category behaves by different grammatical rules. The three categories are:

- **اسم (ism)** — the noun
- **فعل (fiʿl)** — the verb
- **حرف (ḥarf)** — the particle

Once you can spot these at a glance, every other rule in the curriculum becomes much easier.`,
                tr: `Klasik Arapça gramer — ve dolayısıyla Kur'an'ın dili — her kelimeyi tam olarak **üç kategoriye** (أقسام الكلمة) ayırır. Bir kelimenin hangi kategoriye ait olduğunu belirlemek, i'rabın (إعراب) ilk adımıdır; çünkü her kategori farklı gramer kurallarıyla davranır. Üç kategori şunlardır:

- **اسم (ism)** — isim
- **فعل (fiil)** — fiil
- **حرف (harf)** — edat/harf

Bunları bir bakışta tanıyabildiğinde, müfredattaki diğer tüm kurallar çok daha kolay hale gelir.`,
                ar: `يقسّم النحو الكلاسيكي — وبذلك لغة القرآن الكريم — كل كلمة إلى **ثلاث فئات** (أقسام الكلمة). تحديد فئة الكلمة هو أول خطوات الإعراب، لأن كل فئة تتبع قواعد مختلفة. الفئات الثلاث هي:

- **الاسم** — ما يدلّ على معنى مستقلّ بالذات
- **الفعل** — ما يدلّ على معنى مرتبط بالزمن
- **الحرف** — ما لا يظهر معناه إلا مع غيره

عندما تستطيع تمييزها بسرعة، تصبح كل القواعد الأخرى في المنهج أسهل بكثير.`
              }
            },
            {
              title: {
                en: 'الاسم — The Noun (Ism)',
                tr: 'الاسم — İsim',
                ar: 'الاسم'
              },
              body: {
                en: `An **ism** names a person, place, thing, idea, or quality. Its key feature: it carries meaning **independently of time** — the word itself doesn't tell you when something happened.

**How to recognize an ism:**
- It can carry tanwīn (ـٌ ـٍ ـً) — the double-vowel ending
- It can carry the definite article **ال** (al-)
- It can come after a preposition (مِنْ, إِلَى, فِي…)
- It can be the first or second term of an idafa (إضافة, possession chain)
- It can take a feminine ending **ة** (ta marbūṭa) like in مَدْرَسَةٌ`,
                tr: `**İsim**, bir kişiyi, yeri, şeyi, kavramı veya niteliği adlandırır. Temel özelliği: anlamı **zamandan bağımsızdır** — kelimenin kendisi ne zaman olduğunu söylemez.

**İsmi tanıma yolları:**
- Tenvin alabilir (ـٌ ـٍ ـً) — sondaki çift ünlü işareti
- Belirlilik takısı **ال** (al-) alabilir
- Bir harf-i cerden sonra gelebilir (مِنْ, إِلَى, فِي…)
- Bir izafetin (إضافة) birinci veya ikinci terimi olabilir
- مَدْرَسَةٌ'deki gibi dişil **ة** (ta marbuta) alabilir`,
                ar: `**الاسم** يدلّ على شخص أو مكان أو شيء أو مفهوم أو صفة. خاصيته الأساسية: يحمل معنىً **مستقلاً عن الزمن** — أي أن الكلمة بحدّ ذاتها لا تخبرك متى وقع الحدث.

**علامات الاسم:**
- يقبل التنوين (ـٌ ـٍ ـً)
- يقبل **ال** التعريف
- يأتي بعد حرف الجر (مِنْ، إِلَى، فِي…)
- يكون مضافاً أو مضافاً إليه في الإضافة
- يمكن أن ينتهي بـ **ة** (تاء مربوطة) كما في مَدْرَسَةٌ`
              },
              examples: [
                { ar: 'مُحَمَّدٌ', gloss: { en: 'Muhammad (a name)', tr: 'Muhammed (özel ad)', ar: 'اسم علم' } },
                { ar: 'كِتَابٌ',  gloss: { en: 'a book',           tr: 'bir kitap',         ar: 'كتاب' } },
                { ar: 'الْكِتَابُ', gloss: { en: 'the book',         tr: 'kitap (belirli)',   ar: 'الكتاب' } },
                { ar: 'مَدْرَسَةٌ', gloss: { en: 'a school (feminine, with ة)', tr: 'bir okul (dişil, ة ile)', ar: 'مَدْرَسة (مؤنث)' } },
                { ar: 'رَبٌّ',     gloss: { en: 'a Lord',           tr: 'bir Rab',           ar: 'ربّ' } },
              ]
            },
            {
              title: {
                en: 'الفعل — The Verb (Fiʿl)',
                tr: 'الفعل — Fiil',
                ar: 'الفعل'
              },
              body: {
                en: `A **fiʿl** names an action or a state, and is always **tied to time** — past, present, or imperative. Its shape changes based on tense, person, and number.

**How to recognize a fiʿl:**
- It conjugates with subject endings (ـتَ, ـتُ, ـتُمْ, ـُوا…)
- It does NOT take tanwīn, does NOT take **ال**
- It accepts particles like **قَدْ** (indeed/already) and **سَ / سَوْفَ** (will, in future)
- The three tenses are **māḍī** (past), **muḍāriʿ** (present/future), and **amr** (command)`,
                tr: `**Fiil**, bir eylemi veya durumu adlandırır ve daima **zamanla bağlantılıdır** — geçmiş, şimdi veya emir. Şekli; zamana, şahsa ve sayıya göre değişir.

**Fiili tanıma yolları:**
- Şahıs ekleri ile çekilir (ـتَ, ـتُ, ـتُمْ, ـُوا…)
- Tenvin almaz, **ال** almaz
- **قَدْ** (gerçekten/zaten) ve **سَ / سَوْفَ** (gelecek) gibi edatları kabul eder
- Üç zaman vardır: **mâzî** (geçmiş), **muzâri** (şimdiki/geniş), **emir**`,
                ar: `**الفعل** يدلّ على حدث أو حالة، وهو **مرتبط بالزمن** دائماً — ماضٍ أو حاضر أو أمر. تتغيّر صيغته بحسب الزمن والضمير والعدد.

**علامات الفعل:**
- يتصرّف مع ضمائر الفاعل (ـتَ، ـتُ، ـتُمْ، ـُوا…)
- لا يقبل التنوين، ولا **ال**
- يقبل أحرفاً مثل **قَدْ** و**سَ / سَوْفَ**
- له ثلاثة أزمنة: **الماضي** و**المضارع** و**الأمر**`
              },
              examples: [
                { ar: 'كَتَبَ',  gloss: { en: 'he wrote (māḍī)',    tr: 'yazdı (mâzî)',    ar: 'فعل ماضٍ' } },
                { ar: 'يَكْتُبُ', gloss: { en: 'he writes (muḍāriʿ)', tr: 'yazıyor (muzâri)', ar: 'فعل مضارع' } },
                { ar: 'اكْتُبْ', gloss: { en: 'write! (amr)',       tr: 'yaz! (emir)',     ar: 'فعل أمر' } },
                { ar: 'خَلَقَ',  gloss: { en: 'He created',         tr: 'yarattı',         ar: 'خلق' } },
                { ar: 'قَالَ',   gloss: { en: 'He said',            tr: 'dedi',            ar: 'قال' } },
              ]
            },
            {
              title: {
                en: 'الحرف — The Particle (Ḥarf)',
                tr: 'الحرف — Edat (Harf)',
                ar: 'الحرف'
              },
              body: {
                en: `A **ḥarf** is a small connecting word that has **no independent meaning on its own** — it only yields meaning when paired with other words. Particles connect, negate, ask questions, mark cases, or qualify other words.

**How to recognize a ḥarf:**
- It does NOT take tanwīn, does NOT take **ال**, does NOT conjugate
- It is **mabnī** (fixed) — its ending never changes for grammatical reasons
- Common categories: prepositions (حرف جرّ), conjunctions (حرف عطف), negation, question particles, emphasis particles`,
                tr: `**Harf**, **kendi başına anlamı olmayan** küçük bir bağlayıcı kelimedir — yalnızca başka kelimelerle birleştiğinde anlam kazanır. Harfler bağlar, olumsuzlar, soru sorar, durum belirtir veya başka kelimeleri niteler.

**Harfi tanıma yolları:**
- Tenvin almaz, **ال** almaz, çekimlenmez
- **Mebnî**'dir (sabit) — sonu gramer sebebiyle hiç değişmez
- Yaygın türler: harf-i cerler (حرف جرّ), atıf harfleri (حرف عطف), olumsuzluk, soru, tekit harfleri`,
                ar: `**الحرف** كلمة صغيرة رابطة، **لا معنى لها بمفردها** — إنما يظهر معناها عند اقترانها بكلمات أخرى. تستخدم الحروف للربط أو النفي أو الاستفهام أو لتحديد الحالة الإعرابية.

**علامات الحرف:**
- لا يقبل التنوين، ولا **ال**، ولا يتصرّف
- هو **مبنيّ** — لا يتغيّر آخره لأسباب نحوية
- أنواعه الشائعة: حرف جرّ، حرف عطف، حرف نفي، حرف استفهام، حرف توكيد`
              },
              examples: [
                { ar: 'فِي',  gloss: { en: 'in (preposition)',         tr: 'içinde (harf-i cer)',     ar: 'حرف جر' } },
                { ar: 'مِنْ', gloss: { en: 'from (preposition)',       tr: '...den/...dan',           ar: 'حرف جر' } },
                { ar: 'إِلَى', gloss: { en: 'to (preposition)',         tr: '...e doğru',              ar: 'حرف جر' } },
                { ar: 'وَ',   gloss: { en: 'and (conjunction)',        tr: 've (atıf)',               ar: 'حرف عطف' } },
                { ar: 'لَا',  gloss: { en: 'no, not (negation)',       tr: 'değil, hayır (nefy)',     ar: 'حرف نفي' } },
                { ar: 'هَلْ', gloss: { en: 'question particle',        tr: 'soru harfi',              ar: 'حرف استفهام' } },
              ]
            },
            {
              title: {
                en: 'Quick recognition exercise',
                tr: 'Hızlı tanıma alıştırması',
                ar: 'تدريب سريع على التمييز'
              },
              body: {
                en: `Take the opening of every Surah:

**بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ**

Apply your test to each token:

- **بِ** → ḥarf (preposition: "with / in / by")
- **اسْمِ** → ism (noun: "name")
- **ٱللَّهِ** → ism (proper noun: "Allah")
- **ٱلرَّحْمَـٰنِ** → ism (adjective: "the Most Merciful")
- **ٱلرَّحِيمِ** → ism (adjective: "the Especially Merciful")

Notice the pattern: one ḥarf binds the rest into a single phrase. None of the words here are verbs — that's why this opening describes Allah without "doing" anything yet.`,
                tr: `Her sure başında geçen şu cümleyi al:

**بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ**

Her kelimeye testini uygula:

- **بِ** → harf (harf-i cer: "ile / adına")
- **اسْمِ** → isim (ad: "ism")
- **ٱللَّهِ** → isim (özel ad: "Allah")
- **ٱلرَّحْمَـٰنِ** → isim (sıfat: "Rahmân")
- **ٱلرَّحِيمِ** → isim (sıfat: "Rahîm")

Dikkat et: tek bir harf, diğer kelimeleri tek bir öbek halinde bağlıyor. Burada hiçbir kelime fiil değildir — bu yüzden bu açılış henüz hiçbir "eylem" anlatmadan Allah'ı tanıtır.`,
                ar: `خذ افتتاحية كل سورة:

**بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ**

طبّق المعايير على كل كلمة:

- **بِ** ← حرف جر بمعنى "في / مع"
- **اسْمِ** ← اسم بمعنى "اسم"
- **ٱللَّهِ** ← اسم علم
- **ٱلرَّحْمَـٰنِ** ← اسم (صفة)
- **ٱلرَّحِيمِ** ← اسم (صفة)

لاحظ النمط: حرف واحد يربط بقية الكلمات في عبارة واحدة. لا توجد أفعال هنا — لذلك تصف هذه الافتتاحية الله سبحانه دون أن تذكر "فعلاً" بعد.`
              }
            }
          ]
        },
        questions: [
          { type: 'grammar', q: { en: 'What are the three types of Arabic words (أقسام الكلمة)?', tr: 'Arapça kelimelerin üç türü (أقسام الكلمة) nelerdir?', ar: 'ما هي الأنواع الثلاثة للكلمات العربية (أقسام الكلمة)؟' }, expected: { en: 'Ism (Ø§Ø³Ù) = noun/name, Fi\'l (ÙØ¹Ù) = verb, Harf (Ø­Ø±Ù) = particle/preposition', tr: 'Ism (اسم) = isim/ad, Fi\'l (فعل) = fiil, Harf (حرف) = edat/ilgeç', ar: 'اسم = اسم/اسم، فعل = فعل، حرف = حرف/حرف جر' } },
          { type: 'grammar', q: { en: 'Is the word ÙÙØªÙØ¨Ù an isim, fi\'l, or harf? How do you know?', tr: 'كَتَبَ kelimesi isim mi, fiil mi, yoksa harf mi? Nereden biliyorsunuz?', ar: 'هل كلمة كَتَبَ اسم أم فعل أم حرف؟ وكيف تعرف ذلك؟' }, expected: { en: 'Fi\'l (verb) â it expresses an action (he wrote) and accepts tense conjugation', tr: 'Fi\'l (fiil) — bir eylemi (o yazdı) ifade eder ve zaman çekimini kabul eder.', ar: 'فعل — يعبر عن حدث (كتب) ويقبل تصريف الأزمنة.' } },
          { type: 'grammar', q: { en: 'Is the word ÙÙÙÙ an isim, fi\'l, or harf? How do you know?', tr: 'مِنْ kelimesi isim mi, fiil mi, yoksa harf mi? Nereden biliyorsunuz?', ar: 'هل كلمة مِنْ اسم أم فعل أم حرف؟ وكيف تعرف ذلك؟' }, expected: { en: 'Harf (particle) — it does not independently carry full meaning, it connects words (from/of)', tr: 'Harf (edat) — tek başına tam bir anlam taşımaz, kelimeleri birbirine bağlar (den/dan, ait).', ar: 'حرف — لا يحمل معنى كاملاً بمفرده، بل يربط الكلمات (من).' } },
          { type: 'vocabulary', q: { en: 'Give two examples each of an isim, a fi\'l, and a harf from the Quran.', tr: 'Kur\'an\'dan isim, fiil ve harf için ikişer örnek veriniz.', ar: 'أعطِ مثالين لكل من اسم وفعل وحرف من القرآن الكريم.' }, expected: { en: 'Isim: Ø§ÙÙÙÙÙÙØ ÙÙØªÙØ§Ø¨Ù â Fi\'l: Ø®ÙÙÙÙÙØ ÙÙØ§ÙÙ â Harf: ÙÙÙØ ÙÙÙÙØ Ø¥ÙÙÙÙ', tr: 'İsim: اللَّهُ، كِتَابٌ — Fi\'l: خَلَقَ، قَالَ — Harf: فِي، مِنۡ، إِلَى', ar: 'اسم: اللَّهُ، كِتَابٌ — فعل: خَلَقَ، قَالَ — حرف: فِي، مِنۡ، إِلَى' } },
          { type: 'grammar', q: { en: 'What characteristic makes an isim (noun) different from a fi\'l (verb)?', tr: 'Bir ismi (isim) bir fiilden (fiil) ayıran özellik nedir?', ar: 'ما هي الخاصية التي تميز الاسم عن الفعل؟' }, expected: { en: 'An isim names a person, place, thing, or concept and can take tanwin/Ø§Ù. A fi\'l expresses an action or state and changes with tense and person.', tr: 'Bir isim, bir kişiyi, yeri, şeyi veya kavramı adlandırır ve tenvin/ال alabilir. Bir fiil ise bir eylemi veya durumu ifade eder ve zaman ile şahsa göre değişir.', ar: 'الاسم يسمي شخصًا أو مكانًا أو شيئًا أو مفهومًا ويمكن أن يأخذ تنوين/ال. أما الفعل فيعبر عن حركة أو حالة ويتغير حسب الزمن والضمير.' } },
        ]
      },
      {
        week: 2, pdf: 'Level-1/2nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Definite and Indefinite Nouns, and Solar & Lunar Letters', tr: 'Belirli ve Belirsiz İsimler ile Şemsî ve Kamerî Harfler', ar: 'المعرفة والنكرة والحروف الشمسية والقمرية' },
        questions: [
          { type: 'grammar', q: { en: 'How do you make an Arabic noun definite? Give an example.', tr: 'Arapça bir ismi nasıl belirli hale getirirsiniz? Bir örnek veriniz.', ar: 'كيف تجعل الاسم العربي معرفة؟ أعط مثالاً.' }, expected: { en: 'Add ال (al-) prefix and remove tanwin: كِتَابٌ (a book) → الْكِتَابُ (the book)', tr: 'ال (el-) ön ekini ekleyin ve tenvini kaldırın: كِتَابٌ (bir kitap) → الْكِتَابُ (kitap)', ar: 'أضف البادئة ال (al-) وأزل التنوين: كِتَابٌ (كتاب) → الْكِتَابُ (الكتاب)' } },
          { type: 'grammar', q: { en: 'What is Tanwin (تنوين) and what does it indicate?', tr: 'Tenvin (تنوين) nedir ve neyi ifade eder?', ar: 'ما هو التنوين (تنوين) وماذا يدل عليه؟' }, expected: { en: 'Tanwin is a double vowel mark adding an "n" sound to the end of a noun, indicating it is indefinite (nakira): كِتَابٌ = a book', tr: 'Tenvin, bir ismin sonuna "n" sesi ekleyen çift harekedir ve ismin belirsiz (nekra) olduğunu gösterir: كِتَابٌ = bir kitap', ar: 'التنوين هو علامة متحركة مزدوجة تضيف صوت "ن" إلى نهاية الاسم، مما يدل على أنه نكرة: كِتَابٌ = كتاب' } },
          { type: 'grammar', q: { en: 'Is مُسْلِمٌ definite or indefinite? What is its definite form?', tr: 'مُسْلِمٌ belirli mi yoksa belirsiz mi? Belirli hali nedir?', ar: 'هل مُسْلِمٌ معرفة أم نكرة؟ وما هو شكله المعرف؟' }, expected: { en: 'Indefinite (has tanwin). Definite form: الْمُسْلِمُ (the Muslim)', tr: 'Belirsizdir (tenvini vardır). Belirli hali: الْمُسْلِمُ (Müslüman)', ar: 'نكرة (يحتوي على تنوين). شكله المعرف: الْمُسْلِمُ (المسلم)' } },
          { type: 'translation', q: { en: 'Translate: الْحَمْدُ لِلَّهِ — and explain why الْحَمْدُ is definite.', tr: 'Çeviriniz: الْحَمْدُ لِلَّهِ — ve neden الْحَمْدُ\'nun belirli olduğunu açıklayınız.', ar: 'ترجم: الْحَمْدُ لِلَّهِ — واشرح لماذا الْحَمْدُ معرفة.' }, expected: { en: 'All praise is for Allah. الْحَمْدُ is definite because it has the ال prefix and no tanwin.', tr: 'Hamd Allah\'adır. الْحَمْدُ, ال ön ekini taşıdığı ve tenvini olmadığı için belirlidir.', ar: 'كل الحمد لله. الْحَمْدُ معرفة لأنها تحتوي على البادئة ال ولا يوجد بها تنوين.' } },
          { type: 'grammar', q: { en: 'Can a noun have both ال and tanwin at the same time? Why or why not?', tr: 'Bir isim aynı anda hem ال hem de tenvin alabilir mi? Neden evet veya neden hayır?', ar: 'هل يمكن للاسم أن يأخذ ال والتنوين في نفس الوقت؟ لماذا أو لماذا لا؟' }, expected: { en: 'No. ال makes a noun definite; tanwin marks indefiniteness. They are mutually exclusive.', tr: 'Hayır. ال bir ismi belirli yapar; tenvin belirsizliği işaret eder. Birbirlerini dışlarlar.', ar: 'لا. ال تجعل الاسم معرفة؛ والتنوين يشير إلى النكرة. إنهما يستبعدان بعضهما البعض.' } },
        ]
      },
      {
        week: 3, pdf: 'Level-1/3rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Masculine & Feminine Nouns and Demonstrative Pronouns', tr: 'Eril ve Dişil İsimler ve İşaret İsimleri', ar: 'الاسم المذكر والمؤنث وأسماء الإشارة' },
        questions: [
          { type: 'grammar', q: { en: 'What suffix typically marks a feminine noun in Arabic?', tr: 'Arapçada dişil bir ismi tipik olarak hangi sonek işaret eder?', ar: 'ما هي اللاحقة التي تشير عادة إلى الاسم المؤنث في اللغة العربية؟' }, expected: { en: 'ة (ta marbuta), e.g. مُسْلِمَةٌ (a Muslim woman), مَدِينَةٌ (a city)', tr: 'ة (ta marbuta), örn. مُسْلِمَةٌ (bir Müslüman kadın), مَدِينَةٌ (bir şehir)', ar: 'ة (التاء المربوطة)، مثال: مُسْلِمَةٌ (امرأة مسلمة)، مَدِينَةٌ (مدينة)' } },
          { type: 'grammar', q: { en: 'Is مَسْجِدٌ masculine or feminine? How can you tell?', tr: 'مَسْجِدٌ eril mi dişil mi? Nasıl anlarsınız?', ar: 'هل مَسْجِدٌ مذكر أم مؤنث؟ وكيف تعرف؟' }, expected: { en: 'Masculine — it has no ta marbuta (ة) and refers to a place without natural gender', tr: 'Erildir — ta marbuta\'sı (ة) yoktur ve doğal cinsiyeti olmayan bir yeri ifade eder.', ar: 'مذكر — ليس له تاء مربوطة (ة) ويشير إلى مكان ليس له جنس طبيعي.' } },
          { type: 'vocabulary', q: { en: 'What are the demonstrative pronouns for "this" (masc.) and "this" (fem.)?', tr: '"Bu" (eril) ve "bu" (dişil) için işaret zamirleri nelerdir?', ar: 'ما هي أسماء الإشارة لـ "هذا" (مذكر) و "هذه" (مؤنث)؟' }, expected: { en: 'هَذَا (this — masculine), هَذِهِ (this — feminine)', tr: 'هَذَا (bu — eril), هَذِهِ (bu — dişil)', ar: 'هَذَا (هذا — مذكر)، هَذِهِ (هذه — مؤنث)' } },
          { type: 'vocabulary', q: { en: 'What are the demonstrative pronouns for "that" (masc.) and "that" (fem.)?', tr: '"Şu" (eril) ve "şu" (dişil) için işaret zamirleri nelerdir?', ar: 'ما هي أسماء الإشارة لـ "ذلك" (مذكر) و "تلك" (مؤنث)؟' }, expected: { en: 'ذَلِكَ (that — masculine), تِلْكَ (that — feminine)', tr: 'ذَلِكَ (şu — eril), تِلْكَ (şu — dişil)', ar: 'ذَلِكَ (ذلك — مذكر)، تِلْكَ (تلك — مؤنث)' } },
          { type: 'grammar', q: { en: 'Name two Arabic nouns that are feminine without having ta marbuta (ة).', tr: 'Ta marbuta\'sı (ة) olmaksızın dişil olan iki Arapça isim söyleyiniz.', ar: 'اذكر اسمين عربيين مؤنثين لا يحتويان على تاء مربوطة (ة).' }, expected: { en: 'Any two of: أُمٌّ (mother), أَرْضٌ (earth), شَمْسٌ (sun), نَفْسٌ (soul), يَدٌ (hand), عَيْنٌ (eye)', tr: 'Herhangi ikisi: أُمٌّ (anne), أَرْضٌ (yer/toprak), شَمْسٌ (güneş), نَفْسٌ (nefis/ruh), يَدٌ (el), عَيْنٌ (göz)', ar: 'أي اثنتين من: أُمٌّ (أم)، أَرْضٌ (أرض)، شَمْسٌ (شمس)، نَفْسٌ (نفس)، يَدٌ (يد)، عَيْنٌ (عين)' } },
        ]
      },
      {
        week: 4, pdf: 'Level-1/4th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Idafa (Genitive / Possessive Noun Construction)', tr: 'İsim Tamlaması (İzafet)', ar: 'الإضافة' },
        questions: [
          { type: 'grammar', q: { en: 'What is the Idafa construction and what are its two parts?', tr: 'İdafa yapısı nedir ve iki bölümü nelerdir?', ar: 'ما هو تركيب الإضافة وما هما جزآه؟' }, expected: { en: 'A genitive noun phrase: Mudaf (مضاف) + Mudaf ilayh (مضاف إليه). The mudaf loses tanwin and ال; the mudaf ilayh takes genitive (kasra).', tr: 'Bir tamlama (izafet tamlaması): Mudaf (مضاف) + Mudaf ilayh (مضاف إليه). Mudaf tenvin ve ال\'i kaybeder; Mudaf ilayh ise genitif (kesra) alır.', ar: 'عبارة اسمية مضاف ومضاف إليه: مضاف + مضاف إليه. المضاف يفقد التنوين و ال؛ والمضاف إليه يأخذ حالة الجر (الكسرة).' } },
          { type: 'translation', q: { en: 'Translate: كِتَابُ اللَّهِ', tr: 'Çeviriniz: كِتَابُ اللَّهِ', ar: 'ترجم: كِتَابُ اللَّهِ' }, expected: { en: 'The Book of Allah / Allah\'s Book', tr: 'Allah\'ın Kitabı', ar: 'كتاب الله' } },
          { type: 'grammar', q: { en: 'Can the first noun (mudaf) in an idafa have ال? Why?', tr: 'İdafa\'da ilk isim (mudaf) ال alabilir mi? Neden?', ar: 'هل يمكن للاسم الأول (المضاف) في الإضافة أن يأخذ ال؟ لماذا؟' }, expected: { en: 'No. The mudaf cannot have ال or tanwin because the idafa itself makes it specific.', tr: 'Hayır. Mudaf, ال veya tenvin alamaz çünkü idafa\'nın kendisi onu belirli kılar.', ar: 'لا. المضاف لا يمكن أن يأخذ ال أو التنوين لأن الإضافة بحد ذاتها تجعله معرفة.' } },
          { type: 'translation', q: { en: 'Translate: بَيْتُ الْمُسْلِمِ', tr: 'Çeviriniz: بَيْتُ الْمُسْلِمِ', ar: 'ترجم: بَيْتُ الْمُسْلِمِ' }, expected: { en: 'The Muslim\'s house / The house of the Muslim', tr: 'Müslümanın evi / Müslümana ait ev', ar: 'بيت المسلم / منزل المسلم' } },
          { type: 'grammar', q: { en: 'What case does the second noun (mudaf ilayh) always take in idafa?', tr: 'İdafa\'da ikinci isim (mudaf ilayh) her zaman hangi hal ekini alır?', ar: 'أي حالة إعرابية يأخذها الاسم الثاني (المضاف إليه) دائمًا في الإضافة؟' }, expected: { en: 'Genitive case (مجرور), marked by kasra (ـِ) or kasratan (ـٍ)', tr: 'Genitif hal (مجرور), kesra (ـِ) veya kesratan (ـٍ) ile işaretlenir.', ar: 'حالة الجر (مجرور)، وتكون بـ الكسرة (ـِ) أو كسرتين (ـٍ).' } },
        ]
      },
      {
        week: 5, pdf: 'Level-1/5th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Adjective and the Noun it Describes (Al-Sifa and Al-Mawsuf)', tr: 'Sıfat ve Mevsuf (Nitelenen İsim)', ar: 'الصِّفَةُ وَالْمَوْصُوف' },
        questions: [
          { type: 'grammar', q: { en: 'In Arabic, does the adjective (na\'t) come before or after the noun it describes?', tr: 'Arapçada sıfat (na\'t), nitelediği isimden önce mi yoksa sonra mı gelir?', ar: 'في اللغة العربية، هل تأتي الصفة (نعت) قبل أم بعد الاسم الذي تصفه؟' }, expected: { en: 'After the noun: الطَّالِبُ الْمُجْتَهِدُ (the hardworking student)', tr: 'İsimden sonra: الطَّالِبُ الْمُجْتَهِدُ (çalışkan öğrenci)', ar: 'بعد الاسم: الطَّالِبُ الْمُجْتَهِدُ (الطالب المجتهد)' } },
          { type: 'grammar', q: { en: 'In what four things must an adjective agree with its noun?', tr: 'Bir sıfat, nitelediği isimle hangi dört şeyde uyumlu olmalıdır?', ar: 'في أي أربعة أمور يجب أن تتوافق الصفة مع الاسم الموصوف؟' }, expected: { en: 'Gender (masculine/feminine), number (singular/dual/plural), definiteness (definite/indefinite), and case (nominative/accusative/genitive)', tr: 'Cinsiyet (eril/dişil), sayı (tekil/ikil/çoğul), belirlilik (belirli/belirsiz) ve hal (merfu/mansub/mecrur)', ar: 'الجنس (مذكر/مؤنث)، العدد (مفرد/مثنى/جمع)، التعريف والتنكير (معرفة/نكرة)، والحالة الإعرابية (مرفوع/منصوب/مجرور)' } },
          { type: 'grammar', q: { en: 'What is the feminine form of the adjective كَبِيرٌ (big)?', tr: 'كَبِيرٌ (büyük) sıfatının dişil hali nedir?', ar: 'ما هو الشكل المؤنث لصفة كَبِيرٌ (كبير)؟' }, expected: { en: 'كَبِيرَةٌ', tr: 'كَبِيرَةٌ', ar: 'كَبِيرَةٌ' } },
          { type: 'translation', q: { en: 'Translate: الطَّالِبُ الْمُجْتَهِدُ', tr: 'Çeviriniz: الطَّالِبُ الْمُجْتَهِدُ', ar: 'ترجم: الطَّالِبُ الْمُجْتَهِدُ' }, expected: { en: 'The hardworking/diligent student', tr: 'Çalışkan/gayretli öğrenci', ar: 'الطالب المجتهد / الطالب الدؤوب' } },
          { type: 'grammar', q: { en: 'Make this phrase definite: طَالِبٌ مُجْتَهِدٌ', tr: 'Bu ifadeyi belirli hale getiriniz: طَالِبٌ مُجْتَهِدٌ', ar: 'اجعل هذه العبارة معرفة: طَالِبٌ مُجْتَهِدٌ' }, expected: { en: 'الطَّالِبُ الْمُجْتَهِدُ — both the noun and adjective take ال', tr: 'الطَّالِبُ الْمُجْتَهِدُ — hem isim hem de sıfat ال alır.', ar: 'الطَّالِبُ الْمُجْتَهِدُ — يأخذ كل من الاسم والصفة ال.' } },
        ]
      },
      {
        week: 6, pdf: 'Level-1/6th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Pronouns (Detached/Separate Pronouns for Nominative and Accusative)', tr: 'Zamirler (Munfasıl Ref\' ve Nasb Zamirleri)', ar: 'الضمائر المنفصلة (ضمائر الرفع والنصب المنفصلة)' },
        questions: [
          { type: 'vocabulary', q: { en: 'What are the detached pronouns for: he, she, they (masc. pl.)?', tr: 'o, o (dişi), onlar (eril çoğul) için ayrık zamirler nelerdir?', ar: 'ما هي الضمائر المنفصلة لـ: هو، هي، هم (جمع مذكر)؟' }, expected: { en: 'هُوَ (he), هِيَ (she), هُمْ (they — masculine or mixed group)', tr: 'هُوَ (o - eril), هِيَ (o - dişi), هُمْ (onlar - eril veya karma grup)', ar: 'هُوَ (هو), هِيَ (هي), هُمْ (هم — للمذكر أو المجموعة المختلطة)' } },
          { type: 'vocabulary', q: { en: 'When is هُمَا used?', tr: 'هُمَا ne zaman kullanılır?', ar: 'متى يُستخدم هُمَا؟' }, expected: { en: 'For "they two" (dual) — both masculine and feminine: those two people', tr: '"O ikisi" (ikil) için kullanılır - hem eril hem dişil: o iki kişi', ar: 'للمثنى (الجنسين) - مذكر ومؤنث على حد سواء: أي الشخصان أو الاثنتان.' } },
          { type: 'translation', q: { en: 'Translate: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ', tr: 'Çevir: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ', ar: 'ترجم: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ' }, expected: { en: 'You alone we worship and You alone we ask for help (إِيَّاكَ = You — emphatic detached object pronoun)', tr: 'Yalnız Sana kulluk ederiz ve yalnız Senden yardım dileriz (إِيَّاكَ = Sen - pekiştirici ayrık nesne zamiri)', ar: 'فقط إياك نعبد وإياك نستعين (إِيَّاكَ = أنت — ضمير نصب منفصل للتوكيد)' } },
          { type: 'vocabulary', q: { en: 'What is the detached pronoun for "you" (feminine singular)?', tr: '"Sen" (dişil tekil) için ayrık zamir nedir?', ar: 'ما هو الضمير المنفصل لـ "أنتِ" (مفرد مؤنث)؟' }, expected: { en: 'أَنْتِ', tr: 'أَنْتِ', ar: 'أَنْتِ' } },
          { type: 'grammar', q: { en: 'What is the difference between هُمْ and هُنَّ?', tr: 'هُمْ ve هُنَّ arasındaki fark nedir?', ar: 'ما الفرق بين هُمْ و هُنَّ؟' }, expected: { en: 'هُمْ = they (masculine or mixed group); هُنَّ = they (exclusively feminine group)', tr: 'هُمْ = onlar (eril veya karma grup); هُنَّ = onlar (sadece dişil grup)', ar: 'هُمْ = هم (للمذكر أو للمجموعة المختلطة); هُنَّ = هن (للمجموعة المؤنثة فقط)' } },
        ]
      },
      {
        week: 7, pdf: 'Level-1/7th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Attached Pronouns (Damair Muttasila)', tr: 'Bitişik Zamirler (Muttasıl Zamirler)', ar: 'الضمائر المتصلة' },
        questions: [
          { type: 'vocabulary', q: { en: 'What attached pronoun suffix means "his/him" in Arabic?', tr: 'Arapçada "onun/onu" anlamına gelen bitişik zamir eki nedir?', ar: 'ما هي لاحقة الضمير المتصلة التي تعني \'له\' أو \'إياه\'؟' }, expected: { en: 'ـهُ (after most letters): كِتَابُهُ = his book', tr: 'ـهُ (çoğu harften sonra): كِتَابُهُ = onun kitabı', ar: 'ـهُ (بعد معظم الحروف): كِتَابُهُ = كتابه' } },
          { type: 'translation', q: { en: 'Translate: رَبُّهُمْ', tr: 'Çevir: رَبُّهُمْ', ar: 'ترجم: رَبُّهُمْ' }, expected: { en: 'Their Lord (ـهُمْ = their/them, masculine plural)', tr: 'Onların Rabbi (ـهُمْ = onların/onlara, eril çoğul)', ar: 'ربهم (ـهُمْ = لهم/إياهم، جمع مذكر)' } },
          { type: 'grammar', q: { en: 'What is the attached pronoun for "our/us" and give an example?', tr: '"Bizim/bizi" için bitişik zamir nedir ve bir örnek verin?', ar: 'ما هو الضمير المتصل لـ "لنا/إيانا" وأعط مثالا؟' }, expected: { en: 'ـنَا: رَبُّنَا = our Lord, هَدَانَا = He guided us', tr: 'ـنَا: رَبُّنَا = Rabbimiz, هَدَانَا = Bizi hidayete erdirdi', ar: 'ـنَا: رَبُّنَا = ربنا, هَدَانَا = هدانا' } },
          { type: 'grammar', q: { en: 'Attach the pronoun "her" (ـهَا) to the word بَيْتٌ.', tr: '"Dişil onun" (ـهَا) zamirini بَيْتٌ kelimesine ekleyin.', ar: 'ألحق الضمير "لها" (ـهَا) بكلمة بَيْتٌ.' }, expected: { en: 'بَيْتُهَا = her house (tanwin drops when pronoun is added)', tr: 'بَيْتُهَا = onun evi (zamir eklendiğinde tenvin düşer)', ar: 'بَيْتُهَا = بيتها (يسقط التنوين عند إضافة الضمير)' } },
          { type: 'vocabulary', q: { en: 'What pronoun suffix is used for "you" (masculine singular)?', tr: '"Sen" (eril tekil) için hangi zamir eki kullanılır?', ar: 'ما هي لاحقة الضمير المستخدمة لـ "أنت" (مفرد مذكر)؟' }, expected: { en: 'ـكَ: كِتَابُكَ = your book, رَبُّكَ = your Lord', tr: 'ـكَ: كِتَابُكَ = senin kitabın, رَبُّكَ = senin Rabbin', ar: 'ـكَ: كِتَابُكَ = كتابك, رَبُّكَ = ربك' } },
        ]
      },
      {
        week: 8, pdf: 'Level-1/8th Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Prepositions (Huruf al-Jarr) and Adverbs of Place (Zarf al-Makan)', tr: 'Harf-i Cerler ve Yer Zarfları', ar: 'حروف الجرّ وظروف المكان' },
        questions: [
          { type: 'vocabulary', q: { en: 'What does the preposition فِي mean and what case follows it?', tr: 'فِي edatı ne anlama gelir ve hangi hal kendisini takip eder?', ar: 'ماذا تعني حرف الجر فِي وما هي الحالة الإعرابية التي تليه؟' }, expected: { en: 'فِي = in/inside. The following noun takes genitive case (kasra): فِي الْبَيْتِ = in the house', tr: 'فِي = içinde/içerisinde. Kendisini takip eden isim genitif hal alır (kesra): فِي الْبَيْتِ = evin içinde', ar: 'فِي = في/داخل. الاسم الذي يليه يأخذ حالة الجر (الكسرة): فِي الْبَيْتِ = في البيت' } },
          { type: 'vocabulary', q: { en: 'What does عَلَى mean and give a Quranic example?', tr: 'عَلَى ne anlama gelir ve Kur\'ani bir örnek verin?', ar: 'ماذا تعني عَلَى وأعط مثالاً قرآنياً؟' }, expected: { en: 'عَلَى = on/upon. Example: عَلَى صِرَاطٍ مُسْتَقِيمٍ = on a straight path', tr: 'عَلَى = üzerinde/üstünde. Örnek: عَلَى صِرَاطٍ مُسْتَقِيمٍ = doğru bir yol üzerinde', ar: 'عَلَى = على/فوق. مثال: عَلَى صِرَاطٍ مُسْتَقِيمٍ = على صراط مستقيم' } },
          { type: 'vocabulary', q: { en: 'What do إِلَى and مِنْ mean?', tr: 'إِلَى ve مِنْ ne anlama gelir?', ar: 'ماذا تعني إِلَى و مِنْ؟' }, expected: { en: 'إِلَى = to/towards; مِنْ = from/of', tr: 'إِلَى = -e/doğru; مِنْ = -den/-dan/ait', ar: 'إِلَى = إلى/نحو; مِنْ = من/عن' } },
          { type: 'translation', q: { en: 'Translate: الْكِتَابُ فِي الْبَيْتِ', tr: 'Çevir: الْكِتَابُ فِي الْبَيْتِ', ar: 'ترجم: الْكِتَابُ فِي الْبَيْتِ' }, expected: { en: 'The book is in the house', tr: 'Kitap evin içindedir', ar: 'الكتاب في البيت' } },
          { type: 'grammar', q: { en: 'What are ظروف المكان (adverbs of place)? Give two examples.', tr: 'ظروف المكان (yer zarfları) nelerdir? İki örnek verin.', ar: 'ما هي ظروف المكان؟ أعط مثالين.' }, expected: { en: 'Words expressing location: فَوْقَ (above), تَحْتَ (below), أَمَامَ (in front of), خَلْفَ (behind), بَيْنَ (between)', tr: 'Yer bildiren kelimeler: فَوْقَ (üstünde), تَحْتَ (altında), أَمَامَ (önünde), خَلْفَ (arkasında), بَيْنَ (arasında)', ar: 'كلمات تدل على المكان: فَوْقَ (فوق), تَحْتَ (تحت), أَمَامَ (أمام), خَلْفَ (خلف), بَيْنَ (بين)' } },
        ]
      },
      {
        week: 9, pdf: 'Level-1/9th Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Nominal Sentence (Jumlah Ismiyya): Mubtada and Khabar', tr: 'İsim Cümlesi: Mübteda ve Haber', ar: 'الجملة الاسمية: المبتدأ والخبر' },
        questions: [
          { type: 'grammar', q: { en: 'What are the two parts of a nominal sentence (جملة اسمية)?', tr: 'İsim cümlesinin (جملة اسمية) iki bölümü nedir?', ar: 'ما هما جزآ الجملة الاسمية (جملة اسمية)؟' }, expected: { en: 'Mubtada (مبتدأ) = subject and Khabar (خبر) = predicate. Together they make a complete statement.', tr: 'Mübteda (مبتدأ) = özne ve Haber (خبر) = yüklem. Birlikte tam bir ifade oluştururlar.', ar: 'المبتدأ (مبتدأ) والخبر (خبر). يشكلان معًا جملة تامة.' } },
          { type: 'grammar', q: { en: 'What case does the Mubtada take and why is it usually definite?', tr: 'Mübteda hangi hali alır ve neden genellikle belirlidir?', ar: 'ما هي الحالة الإعرابية التي يأخذها المبتدأ ولماذا يكون معرفة عادة؟' }, expected: { en: 'Nominative (مرفوع — damma). It is usually definite because it is the known topic of the sentence.', tr: 'Merfu (مرفوع — damme). Genellikle belirli olur çünkü cümlenin bilinen konusudur.', ar: 'حالة الرفع (مرفوع — ضمة). يكون عادة معرفة لأنه الموضوع المعروف في الجملة.' } },
          { type: 'translation', q: { en: 'Translate and identify mubtada and khabar: اللَّهُ غَفُورٌ', tr: 'Çevir ve mübteda ile haberi belirle: اللَّهُ غَفُورٌ', ar: 'ترجم وحدد المبتدأ والخبر: اللَّهُ غَفُورٌ' }, expected: { en: 'Allah is All-Forgiving. Mubtada: اللَّهُ (definite); Khabar: غَفُورٌ (indefinite)', tr: 'Allah çok bağışlayandır. Mübteda: اللَّهُ (belirli); Haber: غَفُورٌ (belirsiz)', ar: 'الله غفور. المبتدأ: اللَّهُ (معرفة); الخبر: غَفُورٌ (نكرة)' } },
          { type: 'grammar', q: { en: 'What is the difference between a nominal sentence (جملة اسمية) and a verbal sentence (جملة فعلية)?', tr: 'İsim cümlesi (جملة اسمية) ile fiil cümlesi (جملة فعلية) arasındaki fark nedir?', ar: 'ما الفرق بين الجملة الاسمية (جملة اسمية) والجملة الفعلية (جملة فعلية)؟' }, expected: { en: 'Nominal sentence begins with a noun (isim); verbal sentence begins with a verb (fi\'l)', tr: 'İsim cümlesi bir isim (isim) ile başlar; fiil cümlesi bir fiil (fi\'l) ile başlar.', ar: 'الجملة الاسمية تبدأ باسم (اسم); الجملة الفعلية تبدأ بفعل (فعل).' } },
          { type: 'translation', q: { en: 'Translate: الْقُرْآنُ الْكَرِيمُ كِتَابُ اللَّهِ', tr: 'Çevir: الْقُرْآنُ الْكَرِيمُ كِتَابُ اللَّهِ', ar: 'ترجم: الْقُرْآنُ الْكَرِيمُ كِتَابُ اللَّهِ' }, expected: { en: 'The Noble Quran is the Book of Allah', tr: 'Kerim Kur\'an Allah\'ın Kitabıdır', ar: 'القرآن الكريم كتاب الله' } },
        ]
      },
      {
        week: 10, pdf: 'Level-1/10th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Singular, Dual, and Sound Masculine Plural', tr: 'Tekil, İkil ve Kurallı Eril Çoğul', ar: 'المفرد والمثنى وجمع المذكر السالم' },
        questions: [
          { type: 'grammar', q: { en: 'How do you form the dual of a noun in Arabic?', tr: 'Arapçada bir ismin ikili (müsenna) hali nasıl oluşturulur?', ar: 'كيف تشكل المثنى من الاسم في العربية؟' }, expected: { en: 'Add ـَانِ (nominative) or ـَيْنِ (genitive/accusative): كِتَابٌ → كِتَابَانِ / كِتَابَيْنِ', tr: 'İsimin sonuna ـَانِ (merfu hali) veya ـَيْنِ (mecrur/mansup hali) ekleyerek: كِتَابٌ → كِتَابَانِ / كِتَابَيْنِ', ar: 'بإضافة ـَانِ (في حالة الرفع) أو ـَيْنِ (في حالتي الجر والنصب) إلى المفرد: كِتَابٌ → كِتَابَانِ / كِتَابَيْنِ' } },
          { type: 'grammar', q: { en: 'How do you form the Sound Masculine Plural (جمع مذكر سالم)?', tr: 'Cemi Müzekker Salim (جمع مذكر سالم) nasıl oluşturulur?', ar: 'كيف تشكل جمع المذكر السالم (جمع مذكر سالم)؟' }, expected: { en: 'Add ـُونَ (nominative) or ـِينَ (genitive/accusative) to the singular: مُسْلِمٌ → مُسْلِمُونَ / مُسْلِمِينَ', tr: 'Tekilin sonuna ـُونَ (merfu hali) veya ـِينَ (mecrur/mansup hali) ekleyerek: مُسْلِمٌ → مُسْلِمُونَ / مُسْلِمِينَ', ar: 'بإضافة ـُونَ (في حالة الرفع) أو ـِينَ (في حالتي الجر والنصب) إلى المفرد: مُسْلِمٌ → مُسْلِمُونَ / مُسْلِمِينَ' } },
          { type: 'grammar', q: { en: 'What is the plural of مُؤْمِنٌ (believer) using the sound masculine plural?', tr: 'مُؤْمِنٌ (mümin) kelimesinin cemi müzekker salim ile çoğulu nedir?', ar: 'ما هو جمع مُؤْمِنٌ (مؤمن) باستخدام جمع المذكر السالم؟' }, expected: { en: 'مُؤْمِنُونَ (nominative) / مُؤْمِنِينَ (genitive/accusative)', tr: 'مُؤْمِنُونَ (merfu hali) / مُؤْمِنِينَ (mecrur/mansup hali)', ar: 'مُؤْمِنُونَ (في حالة الرفع) / مُؤْمِنِينَ (في حالتي الجر والنصب)' } },
          { type: 'translation', q: { en: 'Translate: وَالْمُؤْمِنُونَ وَالْمُؤْمِنَاتُ', tr: 'Çevir: وَالْمُؤْمِنُونَ وَالْمُؤْمِنَاتُ', ar: 'ترجم: وَالْمُؤْمِنُونَ وَالْمُؤْمِنَاتُ' }, expected: { en: 'And the believing men and the believing women', tr: 'Ve mümin erkekler ve mümin kadınlar', ar: 'والمؤمنون والمؤمنات' } },
          { type: 'grammar', q: { en: 'What is the dual of رَجُلٌ (man)?', tr: 'رَجُلٌ (adam) kelimesinin ikili (müsenna) hali nedir?', ar: 'ما هو مثنى رَجُلٌ (رجل)؟' }, expected: { en: 'رَجُلَانِ (two men — nominative) / رَجُلَيْنِ (genitive/accusative)', tr: 'رَجُلَانِ (iki adam - merfu hali) / رَجُلَيْنِ (mecrur/mansup hali)', ar: 'رَجُلَانِ (رجلان — في حالة الرفع) / رَجُلَيْنِ (في حالتي الجر والنصب)' } },
        ]
      },
      {
        week: 11, pdf: 'Level-1/11th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Sound Feminine Plural (Jam\' Mu\'annath Salim)', tr: 'Kurallı Müennes Çoğul (Cem\' Müennes Salim)', ar: 'جَمْعُ مُؤَنَّثٍ سَالِم' },
        questions: [
          { type: 'grammar', q: { en: 'How do you form the Sound Feminine Plural (جمع مؤنث سالم)?', tr: 'Müennes Salim Cemi (جمع مؤنث سالم) nasıl oluşturulur?', ar: 'كيف تشكل جمع مؤنث سالم؟' }, expected: { en: 'Remove ة (ta marbuta) if present, then add ـَاتٌ (nominative) or ـَاتٍ (genitive/accusative): مُسْلِمَةٌ → مُسْلِمَاتٌ', tr: 'Eğer mevcutsa ة (ta marbuta) harfini kaldırın, sonra ـَاتٌ (merfu) veya ـَاتٍ (mecrur/mansub) ekleyin: مُسْلِمَةٌ → مُسْلِمَاتٌ', ar: 'احذف ة (تاء مربوطة) إن وجدت، ثم أضف ـَاتٌ (الرفع) أو ـَاتٍ (الجر/النصب): مُسْلِمَةٌ → مُسْلِمَاتٌ' } },
          { type: 'grammar', q: { en: 'What is the sound feminine plural of آيَةٌ (verse/sign)?', tr: 'آيَةٌ (ayet/işaret) kelimesinin müennes salim cemi nedir?', ar: 'ما هو جمع مؤنث سالم لكلمة آيَةٌ (آية/علامة)؟' }, expected: { en: 'آيَاتٌ (nominative) / آيَاتٍ (genitive/accusative)', tr: 'آيَاتٌ (merfu) / آيَاتٍ (mecrur/mansub)', ar: 'آيَاتٌ (الرفع) / آيَاتٍ (الجر/النصب)' } },
          { type: 'grammar', q: { en: 'What is the sound feminine plural of جَنَّةٌ (paradise)?', tr: 'جَنَّةٌ (cennet) kelimesinin müennes salim cemi nedir?', ar: 'ما هو جمع مؤنث سالم لكلمة جَنَّةٌ (جنة)؟' }, expected: { en: 'جَنَّاتٌ', tr: 'جَنَّاتٌ', ar: 'جَنَّاتٌ' } },
          { type: 'translation', q: { en: 'Translate: وَبَشِّرِ الْمُؤْمِنِينَ بِأَنَّ لَهُمْ مِنَ اللَّهِ فَضْلًا كَبِيرًا', tr: 'Çeviriniz: وَبَشِّرِ الْمُؤْمِنِينَ بِأَنَّ لَهُمْ مِنَ اللَّهِ فَضْلًا كَبِيرًا', ar: 'ترجم: وَبَشِّرِ الْمُؤْمِنِينَ بِأَنَّ لَهُمْ مِنَ اللَّهِ فَضْلًا كَبِيرًا' }, expected: { en: 'And give good tidings to the believers that for them from Allah is great bounty', tr: 'Müminlere müjdele ki Allah\'tan onlara büyük bir lütuf vardır.', ar: 'وبشر المؤمنين بأن لهم من الله فضلاً كبيراً' } },
          { type: 'grammar', q: { en: 'Can the sound feminine plural form apply to masculine nouns? Give an example.', tr: 'Müennes salim cemi, müzekker isimler için de kullanılabilir mi? Bir örnek verin.', ar: 'هل يمكن تطبيق صيغة جمع مؤنث سالم على الأسماء المذكرة؟ أعط مثالاً.' }, expected: { en: 'Yes, in some cases: صَلَاةٌ → صَلَوَاتٌ; also يَوْمٌ (masculine) has no sound fem. plural — but some masculine words borrowed the ـات ending', tr: 'Evet, bazı durumlarda: صَلَاةٌ → صَلَوَاتٌ; ayrıca يَوْمٌ (müzekker) müennes salim cemi yoktur — ancak bazı müzekker kelimeler ـات ekini almıştır.', ar: 'نعم، في بعض الحالات: صَلَاةٌ → صَلَوَاتٌ؛ وكذلك يَوْمٌ (مذكر) لا يوجد له جمع مؤنث سالم — لكن بعض الكلمات المذكرة استعارت نهاية ـات.' } },
        ]
      },
      {
        week: 12, pdf: 'Level-1/12th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Broken Plural (Jam\' al-Taksir) — Patterns and Quranic Examples', tr: 'Kırık Çoğul (Cemü\'t-Teksir) — Kalıpları ve Kuran\'dan Örnekler', ar: 'جَمْعُ التَّكْسِيرِ — أوزانه وأمثلته القرآنية' },
        questions: [
          { type: 'grammar', q: { en: 'What is a broken plural (جمع تكسير) and why is it called "broken"?', tr: 'Mükesser Cemi (جمع تكسير) nedir ve neden "kırık" olarak adlandırılır?', ar: 'ما هو جمع تكسير ولماذا يسمى "مكسراً"؟' }, expected: { en: 'A plural formed by changing the internal vowel pattern of the word — called "broken" because the word pattern is broken/rearranged, e.g. كِتَابٌ → كُتُبٌ', tr: 'Kelimenin iç sesli harf düzenini değiştirerek oluşan bir çoğuldur — kelime düzeni kırıldığı/yeniden düzenlendiği için "kırık" denir, örn. كِتَابٌ → كُتُبٌ', ar: 'هو جمع يتشكل بتغيير النمط الصوتي الداخلي للكلمة — ويسمى "مكسراً" لأن نمط الكلمة يتكسر/يعاد ترتيبه، مثل كِتَابٌ → كُتُبٌ.' } },
          { type: 'vocabulary', q: { en: 'What is the broken plural of مَسْجِدٌ (mosque)?', tr: 'مَسْجِدٌ (cami) kelimesinin mükesser cemi nedir?', ar: 'ما هو جمع تكسير لكلمة مَسْجِدٌ (مسجد)؟' }, expected: { en: 'مَسَاجِدُ', tr: 'مَسَاجِدُ', ar: 'مَسَاجِدُ' } },
          { type: 'vocabulary', q: { en: 'What is the broken plural of رَجُلٌ (man)?', tr: 'رَجُلٌ (adam) kelimesinin mükesser cemi nedir?', ar: 'ما هو جمع تكسير لكلمة رَجُلٌ (رجل)؟' }, expected: { en: 'رِجَالٌ', tr: 'رِجَالٌ', ar: 'رِجَالٌ' } },
          { type: 'vocabulary', q: { en: 'What is the broken plural of قَلْبٌ (heart)?', tr: 'قَلْبٌ (kalp) kelimesinin mükesser cemi nedir?', ar: 'ما هو جمع تكسير لكلمة قَلْبٌ (قلب)؟' }, expected: { en: 'قُلُوبٌ', tr: 'قُلُوبٌ', ar: 'قُلُوبٌ' } },
          { type: 'grammar', q: { en: 'Does a broken plural have a fixed pattern, or does each word need to be memorized?', tr: 'Mükesser cemilerin belirli bir kalıbı var mıdır, yoksa her kelime için ezberlenmesi mi gerekir?', ar: 'هل لجمع التكسير نمط ثابت، أم يجب حفظ كل كلمة على حدة؟' }, expected: { en: 'There are common patterns (e.g. فُعُولٌ, أَفْعَالٌ, فِعَالٌ) but broken plurals largely need to be memorized per word, unlike sound plurals.', tr: 'Ortak kalıplar (örn. فُعُولٌ, أَفْعَالٌ, فِعَالٌ) vardır, ancak mükesser cemiler, salim cemilerin aksine, büyük ölçüde kelime bazında ezberlenmelidir.', ar: 'توجد أنماط شائعة (مثل فُعُولٌ، أَفْعَالٌ، فِعَالٌ) ولكن جمع التكسير يحتاج في الغالب إلى الحفظ لكل كلمة على حدة، على عكس الجموع السالمة.' } },
        ]
      },
      {
        week: 13, pdf: 'Level-1/13th Lesson Line Spacing 2.0.pdf',
        title: { en: 'The Past Tense Verb (Al-Fi\'l Al-Madi) — Forms and Conjugations', tr: 'Geçmiş Zaman Fiili (El-Fi\'lu\'l-Mâdî) — Çekimleri', ar: 'الفعل الماضي — صيغه وتصريفاته' },
        questions: [
          { type: 'grammar', q: { en: 'What is the base/dictionary form of an Arabic past tense verb?', tr: 'Arapça geçmiş zaman fiilinin kök/sözlük formu nedir?', ar: 'ما هو شكل المصدر/القاموس للفعل الماضي في اللغة العربية؟' }, expected: { en: 'Third person masculine singular past tense: e.g. كَتَبَ (he wrote), ذَهَبَ (he went)', tr: 'Üçüncü tekil şahıs eril geçmiş zaman: örn. كَتَبَ (o yazdı), ذَهَبَ (o gitti)', ar: 'صيغة الماضي للمفرد المذكر الغائب: على سبيل المثال كَتَبَ (هو كتب)، ذَهَبَ (هو ذهب).' } },
          { type: 'grammar', q: { en: 'Conjugate كَتَبَ for "she wrote" and "they (masc. pl.) wrote."', tr: 'كَتَبَ fiilini "o (kadın) yazdı" ve "onlar (eril çoğul) yazdı" için çekimleyin.', ar: 'صرف الفعل كَتَبَ لـ "هي كتبت" و "هم كتبوا (مذكر جمع)".' }, expected: { en: 'She wrote: كَتَبَتْ (add تْ) · They wrote: كَتَبُوا (add واo)', tr: 'O (kadın) yazdı: كَتَبَتْ (تْ ekleyin) · Onlar yazdı: كَتَبُوا (وا ekleyin)', ar: 'هي كتبت: كَتَبَتْ (أضف تْ) · هم كتبوا: كَتَبُوا (أضف وا).' } },
          { type: 'grammar', q: { en: 'Conjugate كَتَبَ for "I wrote" and "you (masc. sing.) wrote."', tr: 'كَتَبَ fiilini "ben yazdım" ve "sen (eril tekil) yazdın" için çekimleyin.', ar: 'صرف الفعل كَتَبَ لـ "أنا كتبت" و "أنت كتبت (مذكر مفرد)".' }, expected: { en: 'I wrote: كَتَبْتُ · You wrote: كَتَبْتَ', tr: 'Ben yazdım: كَتَبْتُ · Sen yazdın: كَتَبْتَ', ar: 'أنا كتبت: كَتَبْتُ · أنت كتبت: كَتَبْتَ.' } },
          { type: 'translation', q: { en: 'Translate: خَلَقَ اللَّهُ السَّمَاوَاتِ وَالْأَرْضَ', tr: 'Çeviriniz: خَلَقَ اللَّهُ السَّمَاوَاتِ وَالْأَرْضَ', ar: 'ترجم: خَلَقَ اللَّهُ السَّمَاوَاتِ وَالْأَرْضَ' }, expected: { en: 'Allah created the heavens and the earth', tr: 'Allah gökleri ve yeri yarattı.', ar: 'خلق الله السماوات والأرض.' } },
          { type: 'grammar', q: { en: 'In the past tense, what suffix is added for "you (fem. sing.)"?', tr: 'Geçmiş zamanda "sen (dişil tekil)" için hangi ek eklenir?', ar: 'في الماضي، ما هي اللاحقة التي تضاف لـ "أنتِ (مؤنث مفرد)"؟' }, expected: { en: 'ـتِ: كَتَبْتِ (you, feminine singular, wrote)', tr: 'ـتِ: كَتَبْتِ (sen, dişil tekil, yazdın)', ar: 'ـتِ: كَتَبْتِ (أنتِ، مؤنث مفرد، كتبتِ).' } },
        ]
      },
      {
        week: 14, pdf: 'Level-1/14th Lesson Line Spacing 2.0.pdf',
        title: { en: 'The Present Tense Verb (Al-Fi\'l Al-Mudari\')', tr: 'Geniş Zaman Fiili (Muzari\' Fiil)', ar: 'الفعل المضارع' },
        questions: [
          { type: 'grammar', q: { en: 'How is the present tense formed? What letters are added?', tr: 'Muzari (şimdiki zaman) nasıl oluşturulur? Hangi harfler eklenir?', ar: 'كيف يتكون الفعل المضارع؟ وما هي الأحرف التي تضاف؟' }, expected: { en: 'Add prefix letters (أ، ت، ي، ن) and adjust vowels: كَتَبَ → يَكْتُبُ (he writes)', tr: 'Ön ek harfleri (أ، ت، ي، ن) eklenir ve sesli harfler ayarlanır: كَتَبَ → يَكْتُبُ (o yazar)', ar: 'أضف أحرف المضارعة (أ، ت، ي، ن) واضبط الحركات: كَتَبَ → يَكْتُبُ (هو يكتب).' } },
          { type: 'grammar', q: { en: 'What prefix indicates "he" and what prefix indicates "I" in the present tense?', tr: 'Muzari fiilde "o (eril)" için hangi ön ek ve "ben" için hangi ön ek kullanılır?', ar: 'ما هي البادئة التي تشير إلى "هو" وما هي البادئة التي تشير إلى "أنا" في الفعل المضارع؟' }, expected: { en: 'يَـ = he; أَ = I: يَكْتُبُ (he writes), أَكْتُبُ (I write)', tr: 'يَـ = o (eril); أَ = ben: يَكْتُبُ (o yazar), أَكْتُبُ (ben yazarım)', ar: 'يَـ = هو؛ أَ = أنا: يَكْتُبُ (هو يكتب)، أَكْتُبُ (أنا أكتب).' } },
          { type: 'grammar', q: { en: 'Conjugate يَكْتُبُ for "they (masc. pl.) write" and "we write."', tr: 'يَكْتُبُ fiilini "onlar (eril çoğul) yazıyorlar" ve "biz yazıyoruz" için çekimleyin.', ar: 'صرف الفعل يَكْتُبُ لـ "هم يكتبون (مذكر جمع)" و "نحن نكتب".' }, expected: { en: 'They write: يَكْتُبُونَ · We write: نَكْتُبُ', tr: 'Onlar yazıyorlar: يَكْتُبُونَ · Biz yazıyoruz: نَكْتُبُ', ar: 'هم يكتبون: يَكْتُبُونَ · نحن نكتب: نَكْتُبُ.' } },
          { type: 'translation', q: { en: 'Translate: يَعْلَمُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ', tr: 'Çeviriniz: يَعْلَمُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ', ar: 'ترجم: يَعْلَمُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ' }, expected: { en: 'He knows what is in the heavens and what is in the earth', tr: 'Göklerde ve yerde olan her şeyi bilir.', ar: 'يعلم ما في السماوات وما في الأرض.' } },
          { type: 'grammar', q: { en: 'What prefix and suffix are used for "she writes" (3rd person fem. sing.)?', tr: '"O (dişil tekil) yazar" için hangi ön ek ve son ek kullanılır?', ar: 'ما هي البادئة واللاحقة المستخدمة لـ "هي تكتب" (الغائب المفرد المؤنث)؟' }, expected: { en: 'تَكْتُبُ — prefix تَـ, no suffix (same prefix as "you" masculine singular)', tr: 'تَكْتُبُ — ön ek تَـ, son ek yok (eril tekil "sen" ile aynı ön ek)', ar: 'تَكْتُبُ — بادئة تَـ، لا توجد لاحقة (نفس بادئة "أنتَ" للمفرد المذكر).' } },
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
          { type: 'grammar', q: { en: 'How is the imperative (فعل أمر) formed from the present tense?', tr: 'Emir (فعل أمر) muzari fiilden nasıl oluşturulur?', ar: 'كيف يتكون فعل الأمر من الفعل المضارع؟' }, expected: { en: 'Take the jussive form, remove the يَـ prefix, and add a helping hamza if needed: يَكْتُبُ → يَكْتُبْ → اُكْتُبْ (Write!)', tr: 'Cezimli (cezmli) şekli alın, يَـ ön ekini kaldırın ve gerekirse bir yardımcı hemze ekleyin: يَكْتُبُ → يَكْتُبْ → اُكْتُبْ (Yaz!)', ar: 'خذ صيغة المجزوم، احذف بادئة يَـ، وأضف همزة وصل عند الحاجة: يَكْتُبُ → يَكْتُبْ → اُكْتُبْ (اكتب!).' } },
          { type: 'translation', q: { en: 'Translate: اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ', tr: 'Çeviriniz: اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ', ar: 'ترجم: اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ' }, expected: { en: 'Read in the name of your Lord who created (Surah Al-Alaq 96:1)', tr: 'Yaratan Rabbinin adıyla oku. (Alak Suresi 96:1)', ar: 'اقرأ باسم ربك الذي خلق. (سورة العلق 96:1).' } },
          { type: 'grammar', q: { en: 'What is the difference between Emr-i Hazır (direct imperative) and Emr-i Gaib (3rd person command)?', tr: 'Emr-i Hazır (doğrudan emir) ve Emr-i Gaib (üçüncü şahıs emir) arasındaki fark nedir?', ar: 'ما الفرق بين أمر الحاضر وأمر الغائب؟' }, expected: { en: 'Emr-i Hazır directly addresses "you": اكْتُبْ (Write!). Emr-i Gaib uses لِـ + jussive: لِيَكْتُبْ (Let him write!)', tr: 'Emr-i Hazır doğrudan "seni" muhatap alır: اكْتُبْ (Yaz!). Emr-i Gaib, لِـ + cezimli muzari kullanır: لِيَكْتُبْ (O yazsın!)', ar: 'أمر الحاضر يخاطب "أنت" مباشرة: اكْتُبْ (اكتب!). أمر الغائب يستخدم لِـ + المجزوم: لِيَكْتُبْ (ليكتب!).' } },
          { type: 'grammar', q: { en: 'What is لام الابتداء (Lam al-Ibtida) and what effect does it have?', tr: 'لام الابتداء (Lam al-Ibtida) nedir ve ne etkisi vardır?', ar: 'ما هي لام الابتداء وما هو تأثيرها؟' }, expected: { en: 'An emphatic لـ at the start of a sentence for emphasis — it does not change the case of the following word', tr: 'Cümlenin başında vurgu için kullanılan teyit edici bir لـ\'dır — kendisinden sonra gelen kelimenin durumunu (irabını) değiştirmez.', ar: 'هي لام تأكيدية (لـ) في بداية الجملة للتأكيد — لا تغير حالة الكلمة التي تليها.' } },
          { type: 'translation', q: { en: 'Give the imperative (command form) of the verb ذَهَبَ/يَذْهَبُ.', tr: 'ذَهَبَ/يَذْهَبُ fiilinin emir (komut) şeklini verin.', ar: 'أعط صيغة الأمر للفعل ذَهَبَ/يَذْهَبُ.' }, expected: { en: 'اِذْهَبْ (Go!)', tr: 'اِذْهَبْ (Git!)', ar: 'اِذْهَبْ (اذهب!).' } },
        ]
      },
      {
        week: 2, pdf: 'Level-2/16th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Prohibition (Nahiy) and Active Participle (Ism al-Fa\'il)', tr: 'Nehiy ve İsm-i Fâil', ar: 'النهي واسم الفاعل' },
        questions: [
          { type: 'grammar', q: { en: 'How is prohibition (نهي) formed in Arabic?', tr: 'Arapçada nehiy (نهي) nasıl oluşturulur?', ar: 'كيف يُصاغ النهي (نهي) في اللغة العربية؟' }, expected: { en: 'ÙÙØ§ + jussive present tense: ÙÙØ§ ØªÙÙÙØªÙØ¨Ù (Don\'t write!), ÙÙØ§ ØªÙÙÙØ±ÙØ¨ÙÙØ§ (Don\'t approach â plural)', tr: 'لَا + meczum muzari fiil: لَا تَكْتُبْ (Yazma!), لَا تَقْرَبُوا (Yaklaşmayın — çoğul)', ar: 'لَا + فعل مضارع مجزوم: لَا تَكْتُبْ (لا تكتب!), لَا تَقْرَبُوا (لا تقتربوا - جمع)' } },
          { type: 'grammar', q: { en: 'What is the pattern for the active participle (اسم الفاعل) of Form I verbs?', tr: 'Birinci kalıp fiillerin etken ismi fail (اسم الفاعل) kalıbı nedir?', ar: 'ما هو وزن اسم الفاعل للفعل الثلاثي المجرد (اسم الفاعل)؟' }, expected: { en: 'Pattern: فَاعِلٌ — e.g. كَتَبَ → كَاتِبٌ (writer), قَرَأَ → قَارِئٌ (reader)', tr: 'Kalıp: فَاعِلٌ — örn. كَتَبَ → كَاتِبٌ (yazan), قَرَأَ → قَارِئٌ (okuyan)', ar: 'الوزن: فَاعِلٌ — مثال: كَتَبَ → كَاتِبٌ (كاتب), قَرَأَ → قَارِئٌ (قارئ)' } },
          { type: 'vocabulary', q: { en: 'What is the active participle of عَلِمَ (to know)?', tr: 'عَلِمَ (bilmek) fiilinin etken ismi faili nedir?', ar: 'ما هو اسم الفاعل للفعل عَلِمَ (يعرف)؟' }, expected: { en: 'عَالِمٌ (one who knows/scholar) — pattern فَاعِلٌ', tr: 'عَالِمٌ (bilen/alim) — kalıp فَاعِلٌ', ar: 'عَالِمٌ (العارف/العالم) — وزن فَاعِلٌ' } },
          { type: 'translation', q: { en: 'Translate: لَا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا', tr: 'Çevir: لَا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا', ar: 'ترجم: لَا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا' }, expected: { en: 'Do not grieve — indeed Allah is with us (Surah At-Tawbah 9:40)', tr: 'Üzülme — şüphesiz Allah bizimledir (Tevbe Suresi 9:40)', ar: 'لا تحزن — إن الله معنا (سورة التوبة 9:40)' } },
          { type: 'grammar', q: { en: 'What is the active participle of رَحِمَ (to have mercy)?', tr: 'رَحِمَ (merhamet etmek) fiilinin etken ismi faili nedir?', ar: 'ما هو اسم الفاعل للفعل رَحِمَ (يرحم)؟' }, expected: { en: 'رَاحِمٌ (one who is merciful) — pattern فَاعِلٌ. Note: الرَّحِيمُ is an intensive form (صيغة مبالغة), not the regular participle.', tr: 'رَاحِمٌ (merhamet eden) — kalıp فَاعِلٌ. Not: الرَّحِيمُ, olağan ismi fail değil, mübalağa kalıbıdır (صيغة مبالغة).', ar: 'رَاحِمٌ (الذي يرحم) — وزن فَاعِلٌ. ملاحظة: الرَّحِيمُ هي صيغة مبالغة، وليست اسم الفاعل القياسي.' } },
        ]
      },
      {
        week: 3, pdf: 'Level-2/17th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Case Endings (I\'rab) for Nouns', tr: 'İsimlerde İ\'rab (Hâl Ekleri)', ar: 'عَلامات الإعراب في الأسماء' },
        questions: [
          { type: 'grammar', q: { en: 'What are the three grammatical cases (إعراب) in Arabic and their vowel markers?', tr: 'Arapçada üç gramer durumu (إعراب) ve onların hareke işaretleri nelerdir?', ar: 'ما هي الحالات الإعرابية الثلاث (إعراب) في اللغة العربية وعلاماتها الحركية؟' }, expected: { en: 'Nominative (رفع) = ضمة (ـُ) · Accusative (نصب) = فتحة (ـَ) · Genitive (جر) = كسرة (ـِ)', tr: 'Merfu (رفع) = damme (ـُ) · Mansup (نصب) = fetha (ـَ) · Mecrur (جر) = kesra (ـِ)', ar: 'الرفع = ضمة (ـُ) · النصب = فتحة (ـَ) · الجر = كسرة (ـِ)' } },
          { type: 'grammar', q: { en: 'What case does a noun take as subject of a nominal sentence (مبتدأ)?', tr: 'İsim cümlesinin öznesi (مبتدأ) olarak bir isim hangi durumu alır?', ar: 'ما هي الحالة الإعرابية التي يأخذها الاسم كـ مبتدأ في الجملة الاسمية (مبتدأ)؟' }, expected: { en: 'Nominative (مرفوع) — marked by damma (ـُ)', tr: 'Merfu (مرفوع) — damme (ـُ) ile işaretlenir', ar: 'مرفوع — يُعلام بالضمة (ـُ)' } },
          { type: 'grammar', q: { en: 'What is صيغة المبالغة (intensive/hyperbolic adjective)? Give two Quranic examples.', tr: 'صيغة المبالغة (yoğun/abartılı sıfat) nedir? İki Kur\'anî örnek verin.', ar: 'ما هي صيغة المبالغة (الصفة المشبهة/المبالغة)؟ أعطِ مثالين قرآنيين.' }, expected: { en: 'A pattern expressing intensity beyond the regular active participle. Common patterns: فَعُولٌ, فَعَّالٌ, فَعِيلٌ. Examples: غَفُورٌ (very forgiving), عَلِيمٌ (all-knowing), رَحِيمٌ (especially merciful)', tr: 'Olağan ismi failin ötesinde bir yoğunluk ifade eden bir kalıptır. Yaygın kalıplar: فَعُولٌ, فَعَّالٌ, فَعِيلٌ. Örnekler: غَفُورٌ (çok bağışlayıcı), عَلِيمٌ (her şeyi bilen), رَحِيمٌ (çok merhametli)', ar: 'صيغة تعبر عن شدة تفوق اسم الفاعل العادي. الأوزان الشائعة: فَعُولٌ, فَعَّالٌ, فَعِيلٌ. أمثلة: غَفُورٌ (كثير الغفران), عَلِيمٌ (عليم بكل شيء), رَحِيمٌ (شديد الرحمة)' } },
          { type: 'grammar', q: { en: 'What case does the object (مفعول به) of a verb take?', tr: 'Bir fiilin nesnesi (مفعول به) hangi durumu alır?', ar: 'ما هي الحالة الإعرابية التي يأخذها المفعول به للفعل (مفعول به)؟' }, expected: { en: 'Accusative (منصوب) — marked by fatha (ـَ): كَتَبَ الطَّالِبُ الدَّرْسَ — الدَّرْسَ is accusative', tr: 'Mansup (منصوب) — fetha (ـَ) ile işaretlenir: كَتَبَ الطَّالِبُ الدَّرْسَ — الدَّرْسَ mansuptur', ar: 'منصوب — يُعلام بالفتحة (ـَ): كَتَبَ الطَّالِبُ الدَّرْسَ — الدَّرْسَ منصوب' } },
          { type: 'vocabulary', q: { en: 'What is the intensive form of كَثِيرٌ (many) seen in the Quran?', tr: 'Kur\'an\'da görülen كَثِيرٌ (çok) kelimesinin mübalağa kalıbı nedir?', ar: 'ما هي صيغة المبالغة لـ كَثِيرٌ (كثير) كما وردت في القرآن؟' }, expected: { en: 'كَثِيرٌ itself is already an intensive pattern. Related: the Quran uses كَثِيرٌ frequently to mean "a great many"', tr: 'كَثِيرٌ kelimesi zaten bir mübalağa kalıbıdır. İlgili: Kur\'an, كَثِيرٌ kelimesini sıkça \'pek çok\' anlamında kullanır.', ar: 'كَثِيرٌ بحد ذاته هو بالفعل وزن مبالغة. ملاحظة: يستخدم القرآن كلمة كَثِيرٌ بكثرة لتعني "عدداً كبيراً جداً".' } },
        ]
      },
      {
        week: 4, pdf: 'Level-2/18th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Verbal Sentence (Jumlah Fi\'liyya) and Intensive Adjective Forms (Siyagh al-Mubalaghah)', tr: 'Fiil Cümlesi ve Mübalağa Sıfatları', ar: 'الجملة الفعلية وصيغ المبالغة' },
        questions: [
          { type: 'grammar', q: { en: 'What are the essential components of a verbal sentence (جملة فعلية)?', tr: 'Fiil cümlesinin (جملة فعلية) temel bileşenleri nelerdir?', ar: 'ما هي المكونات الأساسية للجملة الفعلية (جملة فعلية)؟' }, expected: { en: 'Verb (فعل) + Subject/Doer (فاعل). The object (مفعول به) is optional.', tr: 'Fiil (فعل) + Özne/Fail (فاعل). Nesne (مفعول به) isteğe bağlıdır.', ar: 'فعل + فاعل. المفعول به اختياري.' } },
          { type: 'grammar', q: { en: 'In a verbal sentence, what case does the فاعل (subject/doer) take?', tr: 'Bir fiil cümlesinde, فاعل (özne/fail) hangi durumu alır?', ar: 'في الجملة الفعلية، ما هي الحالة الإعرابية التي يأخذها الفاعل (فاعل)؟' }, expected: { en: 'Nominative (مرفوع)', tr: 'Merfu (مرفوع)', ar: 'مرفوع' } },
          { type: 'grammar', q: { en: 'When a verb comes before a plural subject in Arabic, does the verb agree in number?', tr: 'Arapçada fiil, çoğul bir özneden önce geldiğinde, fiil sayıda uyum sağlar mı?', ar: 'عندما يأتي الفعل قبل الفاعل الجمع في اللغة العربية، هل يتفق الفعل في العدد؟' }, expected: { en: 'No — the verb stays singular (agrees only in gender) when it precedes the subject: كَتَبَ الطُّلَّابُ (The students wrote — verb is singular)', tr: 'Hayır — fiil, özneden önce geldiğinde tekil kalır (yalnızca cinsiyette uyum sağlar): كَتَبَ الطُّلَّابُ (Öğrenciler yazdı — fiil tekildir)', ar: 'لا — يبقى الفعل مفرداً (يتفق في الجنس فقط) عندما يسبق الفاعل: كَتَبَ الطُّلَّابُ (كتب الطلاب — الفعل مفرد)' } },
          { type: 'translation', q: { en: 'Translate: خَلَقَ اللَّهُ الْإِنْسَانَ مِنْ عَلَقٍ', tr: 'Çevir: خَلَقَ اللَّهُ الْإِنْسَانَ مِنْ عَلَقٍ', ar: 'ترجم: خَلَقَ اللَّهُ الْإِنْسَانَ مِنْ عَلَقٍ' }, expected: { en: 'Allah created mankind from a clinging clot (Surah Al-Alaq 96:2)', tr: 'Allah, insanı \'alak\'tan (embriyo, asılıp tutunan şey) yarattı (Alak Suresi 96:2)', ar: 'خلق الله الإنسان من علق (سورة العلق 96:2)' } },
          { type: 'grammar', q: { en: 'Identify verb, fa\'il, and maf\'ul in: Ø¹ÙÙÙÙÙÙ Ø§ÙÙÙÙÙÙ Ø§ÙÙØ¥ÙÙÙØ³ÙØ§ÙÙ ÙÙØ§ ÙÙÙÙ ÙÙØ¹ÙÙÙÙÙ', tr: 'عَلَّمَ اللَّهُ الْإِنْسَانَ مَا لَمْ يَعْلَمْ cümlesinde fiil, fail ve mef\'ulü belirleyin:', ar: 'حدّد الفعل والفاعل والمفعول به في: عَلَّمَ اللَّهُ الْإِنْسَانَ مَا لَمْ يَعْلَمْ' }, expected: { en: 'Verb: Ø¹ÙÙÙÙÙÙ Â· Fa\'il: Ø§ÙÙÙÙÙÙ (nominative) Â· Maf\'ul: Ø§ÙÙØ¥ÙÙÙØ³ÙØ§ÙÙ (accusative)', tr: 'Fiil: عَلَّمَ · Fail: اللَّهُ (merfu) · Mef\'ul: الْإِنْسَانَ (mansup)', ar: 'الفعل: عَلَّمَ · الفاعل: اللَّهُ (مرفوع) · المفعول به: الْإِنْسَانَ (منصوب)' } },
        ]
      },
      {
        week: 5, pdf: 'Level-2/19th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Types of مَا / Future Tense Particles (س and سوف)', tr: 'مَا\'nın Çeşitleri / Gelecek Zaman Edatları (س ve سوف)', ar: 'أنواع مَا / (س) و(سوف) للزمن المستقبل' },
        questions: [
          { type: 'grammar', q: { en: 'What are the main types of لا in Arabic and their functions?', tr: 'Arapçada لا\'nın ana türleri ve işlevleri nelerdir?', ar: 'ما هي الأنواع الرئيسية لـ لا في اللغة العربية ووظائفها؟' }, expected: { en: 'لا النافية (negation of verbs): لا يَعْلَمُ · لا الناهية (prohibition) + jussive · لا النافية للجنس (total negation of nouns): لا إِلَهَ إِلَّا اللَّهُ', tr: 'لا النافية (fiilleri olumsuzlama): لا يَعْلَمُ · لا الناهية (nehiy) + meczum · لا النافية للجنس (isimleri tamamen olumsuzlama): لا إِلَهَ إِلَّا اللَّهُ', ar: 'لا النافية (نفي الأفعال): لا يَعْلَمُ · لا الناهية (النهي) + جازمة · لا النافية للجنس (نفي الأسماء مطلقًا): لا إِلَهَ إِلَّا اللَّهُ' } },
          { type: 'grammar', q: { en: 'How do سَـ and سَوْفَ differ when indicating the future?', tr: 'Geleceği belirtirken سَـ ve سَوْفَ nasıl farklılaşır?', ar: 'كيف تختلف سَـ و سَوْفَ عند الإشارة إلى المستقبل؟' }, expected: { en: 'Both mean "will/shall". سَـ is a short attached prefix for near future; سَوْفَ is a separate word, more emphatic, often for distant or certain future.', tr: 'Her ikisi de \'edecek/olacak\' anlamına gelir. سَـ yakın gelecek için kısa, bitişik bir ön ektir; سَوْفَ ayrı bir kelimedir, daha vurguludur, genellikle uzak veya kesin gelecek için kullanılır.', ar: 'كلاهما يعني "سوف". سَـ حرف قصير متصل للمستقبل القريب؛ سَوْفَ كلمة منفصلة، أكثر توكيداً، وغالباً للمستقبل البعيد أو المؤكد.' } },
          { type: 'translation', q: { en: 'Translate: سَيَقُولُ السُّفَهَاءُ', tr: 'Çevir: سَيَقُولُ السُّفَهَاءُ', ar: 'ترجم: سَيَقُولُ السُّفَهَاءُ' }, expected: { en: 'The foolish ones will say (Surah Al-Baqarah 2:142 — سَ prefix = near future)', tr: 'Akılsızlar diyecekler ki (Bakara Suresi 2:142 — سَ ön eki = yakın gelecek)', ar: 'سيقول السفهاء (سورة البقرة 2:142 — سَ هي حرف للمستقبل القريب)' } },
          { type: 'grammar', q: { en: 'In لَا إِلَهَ إِلَّا اللَّهُ, what type of لا is used and what case does إِلَهَ take?', tr: 'لَا إِلَهَ إِلَّا اللَّهُ cümlesinde hangi tür لا kullanılmıştır ve إِلَهَ hangi durumu alır?', ar: 'في لَا إِلَهَ إِلَّا اللَّهُ، أي نوع من لا يستخدم وما هي الحالة الإعرابية التي يأخذها إِلَهَ؟' }, expected: { en: 'لا النافية للجنس (total negation لا). إِلَهَ takes accusative/fatha (as اسم لا النافية للجنس).', tr: 'لا النافية للجنس (cinsini nefyeden لا). إِلَهَ mansup/fetha (لا النافية للجنس\'in ismi olarak) alır.', ar: 'لا النافية للجنس (لا للنفي المطلق). إِلَهَ يأخذ النصب/الفتحة (كاسم لا النافية للجنس).' } },
          { type: 'translation', q: { en: 'Translate: وَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَى', tr: 'Çevir: وَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَى', ar: 'ترجم: وَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَى' }, expected: { en: 'And your Lord will give to you and you will be satisfied (Surah Ad-Duha 93:5)', tr: 'Ve Rabbin sana verecek, sen de razı olacaksın (Duha Suresi 93:5)', ar: 'وسوف يعطيك ربك فترضى (سورة الضحى 93:5)' } },
        ]
      },
      {
        week: 6, pdf: 'Level-2/20th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Negation Particles: لَيْسَ, مَا, and لَا (Negating Verbal and Nominal Sentences)', tr: 'Olumsuzluk Edatları: لَيْسَ / مَا / لَا ile Fiil ve İsim Cümlelerinin Olumsuzlanması', ar: 'أدوات النفي: لَيْسَ وَمَا وَلَا في الجملة الفعلية والاسمية' },
        questions: [
          { type: 'grammar', q: { en: 'How does لَيْسَ work grammatically?', tr: 'لَيْسَ gramer açısından nasıl işler?', ar: 'كيف تعمل لَيْسَ نحويًا؟' }, expected: { en: 'Like كَانَ: subject takes nominative (اسم ليس), predicate takes accusative (خبر ليس): لَيْسَ اللَّهُ غَافِلًا — اللَّهُ nominative, غَافِلًا accusative', tr: 'كَانَ gibi: özne merfu (اسم ليس), yüklem mansup (خبر ليس) alır: لَيْسَ اللَّهُ غَافِلًا — اللَّهُ merfu, غَافِلًا mansuptur.', ar: 'مثل كَانَ: يأخذ المبتدأ الرفع (اسم ليس)، ويأخذ الخبر النصب (خبر ليس): لَيْسَ اللَّهُ غَافِلًا — اللَّهُ مرفوع، غَافِلًا منصوب.' } },
          { type: 'translation', q: { en: 'Translate: لَيْسَ كَمِثْلِهِ شَيْءٌ', tr: 'Çevir: لَيْسَ كَمِثْلِهِ شَيْءٌ', ar: 'ترجم: لَيْسَ كَمِثْلِهِ شَيْءٌ' }, expected: { en: 'There is nothing like Him (Surah Ash-Shura 42:11)', tr: 'O\'nun benzeri hiçbir şey yoktur (Şura Suresi 42:11)', ar: 'ليس كمثله شيء (سورة الشورى 42:11)' } },
          { type: 'grammar', q: { en: 'How is مَا used for negation and what tense does it typically negate?', tr: 'مَا olumsuzlama için nasıl kullanılır ve genellikle hangi zamanı olumsuzlar?', ar: 'كيف تُستخدم مَا للنفي وما هو الزمن الذي تنفيه عادة؟' }, expected: { en: 'مَا negates past or present: مَا كَتَبَ = he did not write · مَا يَعْلَمُ = he does not know', tr: 'مَا geçmiş veya şimdiki zamanı olumsuzlar: مَا كَتَبَ = yazmadı · مَا يَعْلَمُ = bilmiyor', ar: 'مَا تنفي الماضي أو المضارع: مَا كَتَبَ = لم يكتب · مَا يَعْلَمُ = لا يعلم' } },
          { type: 'grammar', q: { en: 'What is the difference between لَيْسَ and لَا for negation?', tr: 'Olumsuzlama için لَيْسَ ve لَا arasındaki fark nedir?', ar: 'ما الفرق بين لَيْسَ و لَا للنفي؟' }, expected: { en: 'لَيْسَ is a verb ("is not") affecting cases; لَا simply negates verbs or uses the lā-of-genus construction for nouns', tr: 'لَيْسَ durumları etkileyen bir fiildir (\'değildir\'); لَا ise sadece fiilleri olumsuzlar veya isimler için cinsini nefyeden لا yapısını kullanır.', ar: 'لَيْسَ فعل (\'ليس\') يؤثر على الحالات الإعرابية؛ بينما لَا تنفي الأفعال ببساطة أو تستخدم صيغة لا النافية للجنس للأسماء.' } },
          { type: 'translation', q: { en: 'Translate: مَا هَذَا بَشَرًا', tr: 'Çevir: مَا هَذَا بَشَرًا', ar: 'ترجم: مَا هَذَا بَشَرًا' }, expected: { en: 'This is not a human being (Surah Yusuf 12:31 — بَشَرًا accusative as خبر ما)', tr: 'Bu bir insan değildir (Yusuf Suresi 12:31 — بَشَرًا مَا\'nın haberi olarak mansuptur)', ar: 'ما هذا بشراً (سورة يوسف 12:31 — بَشَرًا منصوب كخبر ما)' } },
        ]
      },
      {
        week: 7, pdf: 'Level-2/21st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Particles That Put the Muḍāriʿ (Present/Future) Verb in the Subjunctive (Manṣūb) Case', tr: 'Geniş Zaman Fiilini Mansûb Yapan Edatlar (Nâsıblar)', ar: 'أدوات نصب الفعل المضارع' },
        questions: [
          { type: 'grammar', q: { en: 'Which particles put the present tense in the subjunctive (منصوب) mood?', tr: 'Hangi edatlar şimdiki zamanı mansûb (subjunctive) hale getirir?', ar: 'ما هي الأدوات التي تجعل الفعل المضارع منصوبًا؟' }, expected: { en: 'أَنْ (to/that), لَنْ (will not), كَيْ (in order to), حَتَّى (until/so that), لِـ (in order to)', tr: 'أَنْ (için/ki), لَنْ (asla yapmayacak), كَيْ (amaçla), حَتَّى (e kadar/böylece), لِـ (için)', ar: 'أَنْ (أن), لَنْ (لن), كَيْ (كي), حَتَّى (حتى), لِـ (لِـ)' } },
          { type: 'grammar', q: { en: 'What happens to the final ن of يَكْتُبُونَ in the subjunctive?', tr: 'يَكْتُبُونَ kelimesinin sonundaki ن harfine mansûb halde ne olur?', ar: 'ماذا يحدث للنون في آخر يَكْتُبُونَ في حالة النصب؟' }, expected: { en: 'It is dropped: يَكْتُبُوا (this is one sign of subjunctive in plural forms)', tr: 'Düşer: يَكْتُبُوا (bu, çoğul formlarda mansûb olmanın bir işaretidir)', ar: 'تُحذف: يَكْتُبُوا (وهذه إحدى علامات النصب في صيغ الجمع)' } },
          { type: 'translation', q: { en: 'Translate: أُرِيدُ أَنْ أَتَعَلَّمَ الْعَرَبِيَّةَ', tr: 'Çevir: أُرِيدُ أَنْ أَتَعَلَّمَ الْعَرَبِيَّةَ', ar: 'ترجم: أُرِيدُ أَنْ أَتَعَلَّمَ الْعَرَبِيَّةَ' }, expected: { en: 'I want to learn Arabic (أَنْ puts أَتَعَلَّمَ in subjunctive)', tr: 'Arapça öğrenmek istiyorum (أَنْ, أَتَعَلَّمَ fiilini mansûb hale getirir)', ar: 'أريد أن أتعلم العربية (أَنْ تجعل أَتَعَلَّمَ منصوبًا)' } },
          { type: 'grammar', q: { en: 'What does لَنْ express and how is it different from لَا?', tr: 'لَنْ ne ifade eder ve لَا\'dan farkı nedir?', ar: 'ماذا تعبر لَنْ وكيف تختلف عن لَا؟' }, expected: { en: 'لَنْ = emphatic future negation (will absolutely not), takes subjunctive: لَنْ يَنْجَحَ = he will never succeed. لَا negates present without this emphasis.', tr: 'لَنْ = vurgulu gelecek olumsuzluk (kesinlikle yapmayacak), mansûb hale getirir: لَنْ يَنْجَحَ = asla başaramayacak. لَا, bu vurgu olmaksızın şimdiki zamanı olumsuz yapar.', ar: 'لَنْ = نفي مستقبلي مؤكد (لن يفعل إطلاقًا)، وتجعل الفعل منصوبًا: لَنْ يَنْجَحَ = لن ينجح أبدًا. لَا تنفي المضارع بدون هذا التوكيد.' } },
          { type: 'translation', q: { en: 'Translate: جِئْتُ لِأَتَعَلَّمَ', tr: 'Çevir: جِئْتُ لِأَتَعَلَّمَ', ar: 'ترجم: جِئْتُ لِأَتَعَلَّمَ' }, expected: { en: 'I came in order to learn (لِـ = in order to, puts verb in subjunctive)', tr: 'Öğrenmek için geldim (لِـ = için, fiili mansûb hale getirir)', ar: 'جئت لأتعلم (لِـ = لكي، تجعل الفعل منصوبًا)' } },
        ]
      },
      {
        week: 8, pdf: 'Level-2/22nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Jussive Mood (Majzum): Particles That Govern It and Their Effects on the Mudari\' Verb', tr: 'Cezm Eden Edatlar ve Muzari Fiilin Meczum Hali', ar: 'أدوات جزم الفعل المضارع وأحكامها' },
        questions: [
          { type: 'grammar', q: { en: 'Which particles put the present tense in the jussive (مجزوم) mood?', tr: 'Hangi edatlar şimdiki zamanı meczûm (jussive) hale getirir?', ar: 'ما هي الأدوات التي تجعل الفعل المضارع مجزومًا؟' }, expected: { en: 'ÙÙÙÙ (did not), ÙÙÙÙÙØ§ (not yet), ÙÙØ§ Ø§ÙÙØ§ÙÙØ© (prohibitive don\'t), ÙÙÙ (let him â 3rd person command), and conditional particles like Ø¥ÙÙÙ', tr: 'لَمْ (yapmadı), لَمَّا (henüz değil), لَا النّاهية (yasaklama emir kipi), لِـ (yapsın — 3. şahıs emir), ve إِنْ gibi şart edatları.', ar: 'لَمْ (لم), لَمَّا (لما), لَا النّاهية (لا الناهية), لِـ (لِـ — أمر الغائب), وأدوات الشرط مثل إِنْ.' } },
          { type: 'grammar', q: { en: 'What does لَمْ do and what tense does it effectively create?', tr: 'لَمْ ne iş yapar ve hangi zamanı etkili bir şekilde oluşturur?', ar: 'ماذا تفعل لَمْ وما هو الزمن الذي تحدثه فعليًا؟' }, expected: { en: 'لَمْ negates and converts the present to past: لَمْ يَكْتُبْ = he did not write (past negation)', tr: 'لَمْ, şimdiki zamanı olumsuz yapar ve geçmiş zamana dönüştürür: لَمْ يَكْتُبْ = yazmadı (geçmiş zaman olumsuzluğu).', ar: 'لَمْ تنفي الفعل المضارع وتحوله إلى الماضي: لَمْ يَكْتُبْ = لم يكتب (نفي ماضٍ).' } },
          { type: 'translation', q: { en: 'Translate: لَمْ يَلِدْ وَلَمْ يُولَدْ', tr: 'Çevir: لَمْ يَلِدْ وَلَمْ يُولَدْ', ar: 'ترجم: لَمْ يَلِدْ وَلَمْ يُولَدْ' }, expected: { en: 'He did not beget nor was He begotten (Surah Al-Ikhlas 112:3)', tr: 'Doğurmadı ve doğurulmadı (İhlas Suresi 112:3)', ar: 'لم يلد ولم يولد (سورة الإخلاص 112:3)' } },
          { type: 'grammar', q: { en: 'What happens to the final vowel of يَكْتُبُ in the jussive?', tr: 'يَكْتُبُ fiilinin son sesli harfine meczûm halde ne olur?', ar: 'ماذا يحدث لحركة الحرف الأخير في يَكْتُبُ في حالة الجزم؟' }, expected: { en: 'The damma drops: يَكْتُبْ (sukun on the last root letter)', tr: 'Damme düşer: يَكْتُبْ (son kök harfte sükun olur)', ar: 'تسقط الضمة: يَكْتُبْ (سكون على الحرف الأصلي الأخير)' } },
          { type: 'translation', q: { en: 'Translate: لَا تَحْزَنْ وَلَا تَخَفْ', tr: 'Çevir: لَا تَحْزَنْ وَلَا تَخَفْ', ar: 'ترجم: لَا تَحْزَنْ وَلَا تَخَفْ' }, expected: { en: 'Do not grieve and do not fear', tr: 'Üzülme ve korkma', ar: 'لا تحزن ولا تخف' } },
        ]
      },
      {
        week: 9, pdf: 'Level-2/23rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Passive Voice: Passive Verb (Fi\'l al-Mabni lil-Majhul) and Passive Participle (Ism al-Maf\'ul)', tr: 'Edilgen Çatı: Meçhul Fiil ve İsm-i Mef\'ul', ar: 'الفعل المبني للمجهول واسم المفعول' },
        questions: [
          { type: 'grammar', q: { en: 'How do you form the passive voice of the past tense (Form I)?', tr: 'Geçmiş zamanın meçhul çatısını (Form I) nasıl oluşturursunuz?', ar: 'كيف تُصاغ صيغة المبني للمجهول للفعل الماضي (الوزن الأول)؟' }, expected: { en: 'Change the vowel pattern to فُعِلَ: كَتَبَ → كُتِبَ (it was written), خَلَقَ → خُلِقَ (was created)', tr: 'Sesli harf düzenini فُعِلَ şekline değiştirin: كَتَبَ → كُتِبَ (yazıldı), خَلَقَ → خُلِقَ (yaratıldı)', ar: 'بتغيير شكل الحركات إلى فُعِلَ: كَتَبَ → كُتِبَ (كتب)، خَلَقَ → خُلِقَ (خلق)' } },
          { type: 'grammar', q: { en: 'How do you form the passive of the present tense?', tr: 'Şimdiki zamanın meçhul çatısını nasıl oluşturursunuz?', ar: 'كيف تُصاغ صيغة المبني للمجهول للفعل المضارع؟' }, expected: { en: 'Change to يُفْعَلُ pattern: يَكْتُبُ → يُكْتَبُ (it is written/being written)', tr: 'يُفْعَلُ kalıbına değiştirin: يَكْتُبُ → يُكْتَبُ (yazılır/yazılmakta)', ar: 'بتغيير إلى وزن يُفْعَلُ: يَكْتُبُ → يُكْتَبُ (يُكتَب)' } },
          { type: 'grammar', q: { en: 'What is the pattern for the passive participle (اسم المفعول) of Form I?', tr: 'Form I\'in meçhul ism-i mef\'ul (اسم المفعول) kalıbı nedir?', ar: 'ما هو وزن اسم المفعول من الفعل الثلاثي المجرد (الوزن الأول)؟' }, expected: { en: 'Pattern: مَفْعُولٌ — e.g. كَتَبَ → مَكْتُوبٌ (written), خَلَقَ → مَخْلُوقٌ (created)', tr: 'Kalıp: مَفْعُولٌ — örn. كَتَبَ → مَكْتُوبٌ (yazılı), خَلَقَ → مَخْلُوقٌ (yaratılmış)', ar: 'الوزن: مَفْعُولٌ — مثال: كَتَبَ → مَكْتُوبٌ (مكتوب)، خَلَقَ → مَخْلُوقٌ (مخلوق)' } },
          { type: 'translation', q: { en: 'Translate: خُلِقَ الْإِنْسَانُ مِنْ عَجَلٍ', tr: 'Çevir: خُلِقَ الْإِنْسَانُ مِنْ عَجَلٍ', ar: 'ترجم: خُلِقَ الْإِنْسَانُ مِنْ عَجَلٍ' }, expected: { en: 'Man was created of haste (Surah Al-Anbiya 21:37)', tr: 'İnsan aceleden yaratılmıştır (Enbiya Suresi 21:37)', ar: 'خلق الإنسان من عجل (سورة الأنبياء 21:37)' } },
          { type: 'vocabulary', q: { en: 'What is the passive participle of فَتَحَ (to open)?', tr: 'فَتَحَ (açmak) fiilinin meçhul ism-i mef\'ulü nedir?', ar: 'ما هو اسم المفعول من فَتَحَ (to open)؟' }, expected: { en: 'مَفْتُوحٌ (opened) — pattern مَفْعُولٌ', tr: 'مَفْتُوحٌ (açılmış) — kalıp مَفْعُولٌ', ar: 'مَفْتُوحٌ (مفتوح) — وزن مَفْعُولٌ' } },
        ]
      },
      {
        week: 10, pdf: 'Level-2/24th Lesson Line Spacing 2.0.pdf',
        title: { en: 'إِنَّ and its sisters, كَانَ and its sisters, إِذْ, إِذَا, and لَمَّا', tr: 'İnne ve kardeşleri, Kâne ve kardeşleri, İz, İzâ ve Lemmâ', ar: 'إِنَّ وأخواتها وكَانَ وأخواتها وإِذْ وإِذَا ولَمَّا' },
        questions: [
          { type: 'grammar', q: { en: 'What is the difference between إِذْ and إِذَا?', tr: 'إِذْ ile إِذَا arasındaki fark nedir?', ar: 'ما الفرق بين إِذْ و إِذَا؟' }, expected: { en: 'إِذْ = "when" referring to a definite past moment; إِذَا = "when/if" referring to the future or something expected', tr: 'إِذْ = belirli bir geçmiş anına atıfta bulunan "iken/ne zaman"; إِذَا = geleceğe veya beklenen bir şeye atıfta bulunan "ne zaman/eğer"', ar: 'إِذْ = "حين" للإشارة إلى وقت محدد في الماضي؛ إِذَا = "حين/إذا" للإشارة إلى المستقبل أو شيء متوقع.' } },
          { type: 'grammar', q: { en: 'What does لَمَّا mean and how is it used?', tr: 'لَمَّا ne anlama gelir ve nasıl kullanılır?', ar: 'ماذا تعني لَمَّا وكيف تُستخدم؟' }, expected: { en: 'With past tense: "when" (at the moment that). With present: "not yet". لَمَّا يَقْضِ = he has not yet decided', tr: 'Geçmiş zamanla: "iken" (o anda). Şimdiki zamanla: "henüz değil". لَمَّا يَقْضِ = henüz karar vermedi.', ar: 'مع الفعل الماضي: "عندما" (في اللحظة التي). مع الفعل المضارع: "لم يفعل بعد". لَمَّا يَقْضِ = لم يقضِ بعد.' } },
          { type: 'grammar', q: { en: 'What grammatical effect does كَانَ have on the following predicate?', tr: 'كَانَ\'nin kendisini takip eden yüklem üzerinde nasıl bir dilbilgisel etkisi vardır?', ar: 'ما هو الأثر النحوي لـ كَانَ على خبرها؟' }, expected: { en: 'كَانَ takes a subject (nominative — اسم كان) and puts the predicate in accusative (خبر كان): كَانَ اللَّهُ غَفُورًا رَحِيمًا', tr: 'كَانَ bir özne alır (ötreli — اسم كان) ve yüklemi üstünlü (خبر كان) yapar: كَانَ اللَّهُ غَفُورًا رَحِيمًا', ar: 'ترفع كَانَ الاسم (مرفوع — اسم كان) وتنصب الخبر (منصوب — خبر كان): كَانَ اللَّهُ غَفُورًا رَحِيمًا.' } },
          { type: 'translation', q: { en: 'Translate: كَانَ اللَّهُ عَلِيمًا حَكِيمًا', tr: 'Çevir: كَانَ اللَّهُ عَلِيمًا حَكِيمًا', ar: 'ترجم: كَانَ اللَّهُ عَلِيمًا حَكِيمًا' }, expected: { en: 'Allah has always been All-Knowing, All-Wise (ÙÙØ§ÙÙ here indicates eternality of Allah\'s attribute)', tr: 'Allah her zaman Her Şeyi Bilen, Her Şeyde Hikmet Sahibi olmuştur (buradaki كَانَ, Allah\'ın sıfatının ebediliğini gösterir)', ar: 'كان الله عليمًا حكيمًا (كَانَ هنا تشير إلى أزلية صفة الله)' } },
          { type: 'translation', q: { en: 'Translate: إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ', tr: 'Çevir: إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ', ar: 'ترجم: إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ' }, expected: { en: 'When the victory of Allah comes and the conquest (Surah An-Nasr 110:1)', tr: 'Allah\'ın yardımı ve fetih geldiği zaman (Nasr Suresi 110:1)', ar: 'إذا جاء نصر الله والفتح (سورة النصر 110:1)' } },
        ]
      },
      {
        week: 11, pdf: 'Level-2/25th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Inna and Its Sisters / Possessive Particles (Dhū and Its Forms) / Noun Declension', tr: 'İnne ve Kardeşleri / Sahiplik Edatları (Zū ve Çekimleri) / İsim Çekimi', ar: 'إِنَّ وأخواتها / أسماء الملكية (ذو وتصريفاتها) / إعراب الأسماء' },
        questions: [
          { type: 'grammar', q: { en: 'What are the "sisters of إِنَّ" (إن وأخواتها) and their meanings?', tr: '"إِنَّ ve kardeşleri" (إن وأخواتها) nelerdir ve anlamları nelerdir?', ar: 'ما هي "أخوات إِنَّ" (إن وأخواتها) وما معانيها؟' }, expected: { en: 'إِنَّ (indeed/verily), أَنَّ (that — subordinate), كَأَنَّ (as if), لَكِنَّ (but/however), لَيْتَ (I wish), لَعَلَّ (perhaps/hopefully)', tr: 'إِنَّ (gerçekten/şüphesiz), أَنَّ (ki — bağlaç), كَأَنَّ (sanki), لَكِنَّ (fakat/ancak), لَيْتَ (keşke), لَعَلَّ (belki/umulur ki)', ar: 'إِنَّ (إن), أَنَّ (أن — مصدرية), كَأَنَّ (كأن), لَكِنَّ (لكن), لَيْتَ (ليت), لَعَلَّ (لعل).' } },
          { type: 'grammar', q: { en: 'What grammatical effect do إِنَّ and sisters have?', tr: 'إِنَّ ve kardeşlerinin dilbilgisel etkisi nedir?', ar: 'ما هو الأثر النحوي لـ إِنَّ وأخواتها؟' }, expected: { en: 'They put the subject (اسم إن) in the accusative and keep the predicate (خبر إن) in the nominative: إِنَّ اللَّهَ (acc.) غَفُورٌ (nom.)', tr: 'Özneyi (اسم إن) üstünlü yapar ve yüklemi (خبر إن) ötreli bırakır: إِنَّ اللَّهَ (üstünlü) غَفُورٌ (ötreli).', ar: 'تنصب الاسم (اسم إن) وترفع الخبر (خبر إن): إِنَّ اللَّهَ (منصوب) غَفُورٌ (مرفوع).' } },
          { type: 'translation', q: { en: 'Translate: إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ', tr: 'Çevir: إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ', ar: 'ترجم: إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ' }, expected: { en: 'Indeed Allah is All-Forgiving, Most Merciful', tr: 'Şüphesiz Allah, çok bağışlayıcıdır, çok merhametlidir.', ar: 'إن الله غفور رحيم.' } },
          { type: 'grammar', q: { en: 'What particles express possession in Arabic?', tr: 'Arapçada ait olma/sahiplik ifade eden edatlar nelerdir?', ar: 'ما هي الأدوات التي تعبر عن الملكية في اللغة العربية؟' }, expected: { en: 'لِـ (belonging to), عِنْدَ (with/at — physical possession), لَدَى (with — more literary), مَعَ (with — accompaniment)', tr: 'لِـ (ait olan), عِنْدَ (yanında/de — fiziksel sahiplik), لَدَى (yanında — daha edebi), مَعَ (ile — eşlik)', ar: 'لِـ (لِـ — للملكية), عِنْدَ (عند — للملكية المادية), لَدَى (لدى — أكثر أدبية), مَعَ (مع — للمصاحبة).' } },
          { type: 'translation', q: { en: 'Translate: لَيْتَنِي كُنْتُ تُرَابًا', tr: 'Çevir: لَيْتَنِي كُنْتُ تُرَابًا', ar: 'ترجم: لَيْتَنِي كُنْتُ تُرَابًا' }, expected: { en: 'I wish I were dust! (Surah An-Naba 78:40 — لَيْتَ expresses a wish)', tr: 'Keşke toprak olsaydım! (Nebe Suresi 78:40 — لَيْتَ bir dileği ifade eder)', ar: 'ليتني كنت ترابًا! (سورة النبأ 78:40 — لَيْتَ تعبر عن التمني)' } },
        ]
      },
      {
        week: 12, pdf: 'Level-2/26th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Kāna and Its Sisters / Restriction with إِنْ...إِلَّا and مَا...إِلَّا / Conjunctions وَ، فَ، ثُمَّ', tr: 'Kâne ve Kardeşleri / İn...İllâ ve Mâ...İllâ ile Hasır / Bağlaçlar وَ، فَ، ثُمَّ', ar: 'كَانَ وَأَخَوَاتُهَا / الْحَصْرُ بِإِنْ...إِلَّا وَمَا...إِلَّا / حُرُوفُ الْعَطْفِ وَ، فَ، ثُمَّ' },
        questions: [
          { type: 'grammar', q: { en: 'Name five sisters of كَانَ and their meanings.', tr: 'كَانَ\'nin beş kız kardeşini ve anlamlarını belirtin.', ar: 'اذكر خمسًا من أخوات كَانَ ومعانيها.' }, expected: { en: 'أَصْبَحَ (became in morning/became), أَمْسَى (became in evening), صَارَ (became), ظَلَّ (remained), لَيْسَ (is not), مَازَالَ (still is), بَاتَ (spent the night)', tr: 'أَصْبَحَ (sabahleyin oldu/oldu), أَمْسَى (akşamleyin oldu), صَارَ (dönüştü/oldu), ظَلَّ (kalmaya devam etti), لَيْسَ (değildir), مَازَالَ (hala), بَاتَ (geceledi)', ar: 'أَصْبَحَ (صار في الصباح/أصبح), أَمْسَى (صار في المساء), صَارَ (تحول/أصبح), ظَلَّ (بقي/استمر), لَيْسَ (ليس), مَازَالَ (لا يزال), بَاتَ (قضى الليل)' } },
          { type: 'grammar', q: { en: 'What is the grammatical rule of أَمَّا...فَـ?', tr: 'أَمَّا...فَـ\'nın gramer kuralı nedir?', ar: 'ما هي القاعدة النحوية لـ أَمَّا...فَـ؟' }, expected: { en: 'أَمَّا introduces a topic; فَـ is obligatory before the comment/result. Structure: أَمَّا [topic] فَـ [comment]: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ', tr: 'أَمَّا bir konuyu tanıtır; فَـ yorum/sonuçtan önce zorunludur. Yapı: أَمَّا [konu] فَـ [yorum]: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ', ar: 'أَمَّا تقدم الموضوع؛ فَـ واجبة قبل الخبر/النتيجة. الهيكل: أَمَّا [الموضوع] فَـ [الخبر]: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ' } },
          { type: 'translation', q: { en: 'Translate: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ · وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ', tr: 'Çeviriniz: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ · وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ', ar: 'ترجم: أَمَّا الْيَتِيمَ فَلَا تَقْهَرْ · وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ' }, expected: { en: 'As for the orphan, do not oppress him · And as for the beggar, do not rebuke him (Surah Ad-Duha 93:9-10)', tr: 'Yetim için, ona kahretme (eziyet etme) · Dilenciye gelince, onu azarlama (Duha Suresi 93:9-10)', ar: 'أما اليتيم فلا تقهره · وأما السائل فلا تزجره (سورة الضحى 93:9-10)' } },
          { type: 'grammar', q: { en: 'What does صَارَ indicate that is different from كَانَ?', tr: 'صَارَ, كَانَ\'den farklı olarak neyi belirtir?', ar: 'ما الذي تدل عليه صَارَ ويختلف عن كَانَ؟' }, expected: { en: 'صَارَ indicates a transition/change of state (he became): صَارَ الطَّالِبُ عَالِمًا = The student became a scholar. كَانَ just describes a past state.', tr: 'صَارَ bir durum geçişini/değişimini belirtir (o oldu): صَارَ الطَّالِبُ عَالِمًا = Öğrenci alim oldu. كَانَ sadece geçmiş bir durumu tanımlar.', ar: 'صَارَ تدل على التحول/تغيير الحالة (أصبح): صَارَ الطَّالِبُ عَالِمًا = أصبح الطالب عالمًا. كَانَ تصف حالة ماضية فقط.' } },
          { type: 'translation', q: { en: 'Translate: وَكَانَ اللَّهُ بِكُلِّ شَيْءٍ عَلِيمًا', tr: 'Çeviriniz: وَكَانَ اللَّهُ بِكُلِّ شَيْءٍ عَلِيمًا', ar: 'ترجم: وَكَانَ اللَّهُ بِكُلِّ شَيْءٍ عَلِيمًا' }, expected: { en: 'And Allah is ever All-Knowing of everything (Surah Al-Ahzab 33:40)', tr: 'Ve Allah her şeyi hakkıyla bilendir (Ahzab Suresi 33:40)', ar: 'وكان الله بكل شيء عليمًا (سورة الأحزاب 33:40)' } },
        ]
      },
      {
        week: 13, pdf: 'Level-2/27th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Question Particles, Plural Idafa (Sound Masculine Plural in Genitive Construction), and Vocative Particles (Nida)', tr: 'Soru Edatları, Çoğul İsim Tamlamaları (Eril Çoğul İdafe) ve Nida (Seslenme) Edatları', ar: 'أدوات الاستفهام وإضافة جمع المذكر السالم وأسلوب النداء' },
        questions: [
          { type: 'grammar', q: { en: 'What is the difference between هَلْ and أَ as question particles?', tr: 'Soru edatları olan هَلْ ve أَ arasındaki fark nedir?', ar: 'ما الفرق بين هَلْ و أَ كأدوات استفهام؟' }, expected: { en: 'Both ask yes/no questions. هَلْ is neutral; أَ can express rhetorical questions, surprise, or disbelief', tr: 'Her ikisi de evet/hayır soruları sorar. هَلْ nötrdür; أَ retorik soruları, şaşkınlığı veya inkârı ifade edebilir.', ar: 'كلاهما يسأل أسئلة بنعم/لا. هَلْ محايدة؛ أَ يمكن أن تعبر عن أسئلة بلاغية، أو دهشة، أو عدم تصديق.' } },
          { type: 'vocabulary', q: { en: 'What do the question words مَنْ, مَا, أَيْنَ, مَتَى, كَيْفَ, كَمْ mean?', tr: 'مَنْ, مَا, أَيْنَ, مَتَى, كَيْفَ, كَمْ soru kelimeleri ne anlama gelir?', ar: 'ماذا تعني كلمات الاستفهام مَنْ, مَا, أَيْنَ, مَتَى, كَيْفَ, كَمْ؟' }, expected: { en: 'مَنْ = who · مَا = what · أَيْنَ = where · مَتَى = when · كَيْفَ = how · كَمْ = how many', tr: 'مَنْ = kim · مَا = ne · أَيْنَ = nerede · مَتَى = ne zaman · كَيْفَ = nasıl · كَمْ = kaç', ar: 'مَنْ = مَن · مَا = ما · أَيْنَ = أين · مَتَى = متى · كَيْفَ = كيف · كَمْ = كم' } },
          { type: 'grammar', q: { en: 'What is the vocative particle (حرف النداء) and what case follows it?', tr: 'Seslenme edatı (حرف النداء) nedir ve ondan sonra gelen isim hangi halde olur?', ar: 'ما هو حرف النداء وما هي الحالة الإعرابية للاسم الذي يليه؟' }, expected: { en: 'ÙÙØ§ (O!) â the addressed noun takes nominative with Ø§Ù if it\'s a defined noun: ÙÙØ§ Ø£ÙÙÙÙÙÙØ§ Ø§ÙÙÙÙØ§Ø³Ù (O Mankind!)', tr: 'يَا (Ey!) — hitap edilen isim, belirli bir isim ise ال ile merfu (nominatif) olur: يَا أَيُّهَا النَّاسُ (Ey insanlar!)', ar: 'يَا (يا!) — الاسم المنادى يأتي مرفوعًا مع ال إذا كان معرفة: يَا أَيُّهَا النَّاسُ (يا أيها الناس!)' } },
          { type: 'translation', q: { en: 'Translate: يَا أَيُّهَا الَّذِينَ آمَنُوا', tr: 'Çeviriniz: يَا أَيُّهَا الَّذِينَ آمَنُوا', ar: 'ترجم: يَا أَيُّهَا الَّذِينَ آمَنُوا' }, expected: { en: 'O you who have believed! (common Quranic address to believers)', tr: 'Ey iman edenler! (Müminlere Kur\'an\'daki yaygın bir hitap)', ar: 'يا أيها الذين آمنوا! (نداء قرآني شائع للمؤمنين)' } },
          { type: 'grammar', q: { en: 'Translate this question and identify the question word: أَيْنَ تَذْهَبُونَ؟', tr: 'Bu soruyu çevirin ve soru kelimesini belirleyin: أَيْنَ تَذْهَبُونَ؟', ar: 'ترجم هذا السؤال وحدد كلمة الاستفهام: أَيْنَ تَذْهَبُونَ؟' }, expected: { en: 'Where are you going? — أَيْنَ = where (adverb of place)', tr: 'Nereye gidiyorsunuz? — أَيْنَ = nerede (mekan zarfı)', ar: 'إلى أين تذهبون؟ — أَيْنَ = أين (ظرف مكان)' } },
        ]
      },
      {
        week: 14, pdf: 'Level-2/28th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Comparative/Superlative (Ism al-Tafdil) and Exclamatory Expression (Uslub al-Ta\'ajjub)', tr: 'İsm-i Tafdil ve Ta\'accub Üslubu', ar: 'اسم التفضيل وأسلوب التعجب' },
        questions: [
          { type: 'grammar', q: { en: 'What is the pattern for the comparative/superlative (اسم التفضيل)?', tr: 'Karşılaştırma/üstünlük (اسم التفضيل) için kalıp nedir?', ar: 'ما هو وزن اسم التفضيل؟' }, expected: { en: 'Pattern: أَفْعَلُ — e.g. كَبِيرٌ → أَكْبَرُ (bigger/greatest), كَرِيمٌ → أَكْرَمُ (more/most generous)', tr: 'Kalıp: أَفْعَلُ — örn. كَبِيرٌ → أَكْبَرُ (daha büyük/en büyük), كَرِيمٌ → أَكْرَمُ (daha/en cömert)', ar: 'الوزن: أَفْعَلُ — مثال: كَبِيرٌ → أَكْبَرُ (أكبر/الأعظم), كَرِيمٌ → أَكْرَمُ (أكرم/الأكثر كرمًا)' } },
          { type: 'translation', q: { en: 'Translate: اللَّهُ أَكْبَرُ', tr: 'Çeviriniz: اللَّهُ أَكْبَرُ', ar: 'ترجم: اللَّهُ أَكْبَرُ' }, expected: { en: 'Allah is the Greatest (superlative — اسم التفضيل)', tr: 'Allah en büyüktür (üstünlük ismi — اسم التفضيل)', ar: 'الله أكبر (صيغة تفضيل — اسم التفضيل)' } },
          { type: 'grammar', q: { en: 'What are the two patterns for expressing astonishment (تعجب) in Arabic?', tr: 'Arapçada şaşkınlığı (تعجب) ifade etmenin iki kalıbı nedir?', ar: 'ما هما وزنا التعجب في اللغة العربية؟' }, expected: { en: '1) مَا أَفْعَلَهُ!: مَا أَجْمَلَ السَّمَاءَ! (How beautiful the sky is!) 2) أَفْعِلْ بِهِ!: أَكْرِمْ بِهِ! (How noble he is!)', tr: '1) مَا أَفْعَلَهُ!: مَا أَجْمَلَ السَّمَاءَ! (Gökyüzü ne güzel!) 2) أَفْعِلْ بِهِ!: أَكْرِمْ بِهِ! (O ne kadar soylu!)', ar: '1) مَا أَفْعَلَهُ!: مَا أَجْمَلَ السَّمَاءَ! (ما أجمل السماء!) 2) أَفْعِلْ بِهِ!: أَكْرِمْ بِهِ! (ما أكرمه!)' } },
          { type: 'translation', q: { en: 'Translate: إِنَّ أَكْرَمَكُمْ عِنْدَ اللَّهِ أَتْقَاكُمْ', tr: 'Çeviriniz: إِنَّ أَكْرَمَكُمْ عِنْدَ اللَّهِ أَتْقَاكُمْ', ar: 'ترجم: إِنَّ أَكْرَمَكُمْ عِنْدَ اللَّهِ أَتْقَاكُمْ' }, expected: { en: 'Indeed the most noble of you in the sight of Allah is the most righteous of you (Surah Al-Hujurat 49:13)', tr: 'Şüphesiz Allah katında en şerefliniz, takvaca en üstün olanınızdır (Hucurat Suresi 49:13)', ar: 'إن أكرمكم عند الله أتقاكم (سورة الحجرات 49:13)' } },
          { type: 'grammar', q: { en: 'What is the comparative/superlative of قَرِيبٌ (near)?', tr: 'قَرِيبٌ (yakın) kelimesinin karşılaştırma/üstünlük (ismi) nedir?', ar: 'ما هو اسم التفضيل من قَرِيبٌ؟' }, expected: { en: 'أَقْرَبُ (nearer/nearest) — Quranic: وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ', tr: 'أَقْرَبُ (daha yakın/en yakın) — Kur\'an\'dan: وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ', ar: 'أَقْرَبُ (أقرب/الأقرب) — قرآنياً: وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ' } },
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
          { type: 'grammar', q: { en: 'What is a Masdar (مصدر) and what role does it play in Arabic grammar?', tr: 'Masdar (مصدر) nedir ve Arapça gramerinde hangi rolü oynar?', ar: 'ما هو المصدر (مصدر) وما الدور الذي يلعبه في قواعد اللغة العربية؟' }, expected: { en: 'A verbal noun expressing the action abstractly. It can be subject, object, or modifier: الضَّرْبُ حَرَامٌ (Hitting is forbidden)', tr: 'Eylemi soyut olarak ifade eden bir fiil ismidir. Özne, nesne veya niteleyici olabilir: الضَّرْبُ حَرَامٌ (Vurmak haramdır)', ar: 'اسم فعل يعبر عن الحدث بشكل مجرد. يمكن أن يكون فاعلاً أو مفعولاً به أو مضافًا: الضَّرْبُ حَرَامٌ (الضرب محرم)' } },
          { type: 'grammar', q: { en: 'What is the Masdar Mimi (مصدر ميمي) and what is its pattern?', tr: 'Masdar Mimi (مصدر ميمي) nedir ve kalıbı nedir?', ar: 'ما هو المصدر الميمي (مصدر ميمي) وما هو وزنه؟' }, expected: { en: 'A verbal noun beginning with م: pattern مَفْعَلٌ or مَفْعِلٌ — e.g. مَكْتَبٌ (desk/office, from writing), مَذْهَبٌ (school of thought, from going)', tr: 'م harfiyle başlayan bir fiil ismidir: kalıp مَفْعَلٌ veya مَفْعِلٌ — örn. مَكْتَبٌ (masa/ofis, yazmaktan), مَذْهَبٌ (mezhep, gitmekten)', ar: 'اسم فعل يبدأ بالميم: وزن مَفْعَلٌ أو مَفْعِلٌ — مثال: مَكْتَبٌ (مكتب/مكتبة، من الكتابة), مَذْهَبٌ (مذهب، من الذهاب)' } },
          { type: 'vocabulary', q: { en: 'What is the masdar of ذَهَبَ (to go)?', tr: 'ذَهَبَ (gitmek) fiilinin masdarı nedir?', ar: 'ما هو مصدر ذَهَبَ؟' }, expected: { en: 'ذَهَابٌ (going/departure)', tr: 'ذَهَابٌ (gitmek/ayrılma)', ar: 'ذَهَابٌ (الذهاب/المغادرة)' } },
          { type: 'grammar', q: { en: 'What is أَنْ المصدرية and how does it function?', tr: 'أَنْ المصدرية nedir ve nasıl işler?', ar: 'ما هي أَنْ المصدرية وكيف تعمل؟' }, expected: { en: 'أَنْ + subjunctive verb = verbal noun equivalent: أُرِيدُ أَنْ أَكْتُبَ = أُرِيدُ الْكِتَابَةَ (I want writing/to write)', tr: 'أَنْ + mansub fiil (subjunctive verb) = masdar eşdeğeri: أُرِيدُ أَنْ أَكْتُبَ = أُرِيدُ الْكِتَابَةَ (Yazmayı istiyorum)', ar: 'أَنْ + الفعل المضارع المنصوب = ما يعادل المصدر: أُرِيدُ أَنْ أَكْتُبَ = أُرِيدُ الْكِتَابَةَ (أريد الكتابة)' } },
          { type: 'translation', q: { en: 'Translate: وَأَنْ تَصُومُوا خَيْرٌ لَكُمْ', tr: 'Çeviriniz: وَأَنْ تَصُومُوا خَيْرٌ لَكُمْ', ar: 'ترجم: وَأَنْ تَصُومُوا خَيْرٌ لَكُمْ' }, expected: { en: 'And that you fast is better for you (Surah Al-Baqarah 2:184 — أَنْ تَصُومُوا = a masdar-like clause = "your fasting")', tr: 'Oruç tutmanız sizin için daha hayırlıdır (Bakara Suresi 2:184 — أَنْ تَصُومُوا = masdar benzeri bir cümle = "sizin oruç tutmanız")', ar: 'وأن تصوموا خير لكم (سورة البقرة 2:184 — أَنْ تَصُومُوا = جملة مصدرية = "صيامكم")' } },
        ]
      },
      {
        week: 2, pdf: 'Level-3/30th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Nouns of Time and Place, Instrument Nouns, Attributive Adjective (Nisba), Diminutive, and Similative Participle', tr: 'İsmi Zaman ve Mekân, İsmi Âlet, İsmi Mensûb, Tasgîr ve Sıfat-ı Müşebbehe', ar: 'اسم الزمان والمكان، اسم الآلة، الاسم المنسوب، التصغير، والصفة المشبهة' },
        questions: [
          { type: 'grammar', q: { en: 'What are the patterns for the noun of time/place (اسم الزمان والمكان)?', tr: 'Zaman/mekan ismi (اسم الزمان والمكان) için kalıplar nelerdir?', ar: 'ما هي أوزان اسم الزمان والمكان؟' }, expected: { en: 'مَفْعَلٌ or مَفْعِلٌ: مَسْجِدٌ (place of prostration), مَطْلَعٌ (time of rising), مَدْخَلٌ (entrance)', tr: 'مَفْعَلٌ veya مَفْعِلٌ: مَسْجِدٌ (secde yeri), مَطْلَعٌ (doğuş vakti), مَدْخَلٌ (giriş)', ar: 'مَفْعَلٌ أو مَفْعِلٌ: مَسْجِدٌ (مكان السجود), مَطْلَعٌ (وقت الطلوع), مَدْخَلٌ (مكان الدخول)' } },
          { type: 'grammar', q: { en: 'What is the noun of instrument (اسم الآلة) and its patterns?', tr: 'İsmi alet (اسم الآلة) nedir ve kalıpları nelerdir?', ar: 'ما هو اسم الآلة (اسم الآلة) وما هي أوزانه؟' }, expected: { en: 'A noun for the tool of an action. Patterns: مِفْعَلٌ, مِفْعَالٌ, مِفْعَلَةٌ — examples: مِفْتَاحٌ (key), مِيزَانٌ (scale), مِكْنَسَةٌ (broom)', tr: 'Bir eylemin aracı için kullanılan isimdir. Kalıplar: مِفْعَلٌ, مِفْعَالٌ, مِفْعَلَةٌ — örnekler: مِفْتَاحٌ (anahtar), مِيزَانٌ (terazi), مِكْنَسَةٌ (süpürge)', ar: 'اسم للأداة المستخدمة في فعل. أوزانه: مِفْعَلٌ, مِفْعَالٌ, مِفْعَلَةٌ — أمثلة: مِفْتَاحٌ (مفتاح), مِيزَانٌ (ميزان), مِكْنَسَةٌ (مكنسة)' } },
          { type: 'grammar', q: { en: 'What is a Nisba adjective (اسم المنسوب) and how is it formed?', tr: 'Nisbe sıfatı (اسم المنسوب) nedir ve nasıl oluşur?', ar: 'ما هو اسم المنسوب (اسم المنسوب) وكيف يتكون؟' }, expected: { en: 'An adjective of relation/attribution: add ـِيٌّ to the noun: عَرَبٌ → عَرَبِيٌّ (Arabic), إِسْلَامٌ → إِسْلَامِيٌّ (Islamic)', tr: 'İlişki/aitlik sıfatıdır: isme ـِيٌّ eklenir: عَرَبٌ → عَرَبِيٌّ (Arapça), إِسْلَامٌ → إِسْلَامِيٌّ (İslami)', ar: 'صفة تدل على النسبة/الانتساب: تضاف ـِيٌّ إلى الاسم: عَرَبٌ → عَرَبِيٌّ (عربي), إِسْلَامٌ → إِسْلَامِيٌّ (إسلامي)' } },
          { type: 'grammar', q: { en: 'What is the diminutive (تصغير) and what is its basic pattern?', tr: 'Diminütif (تصغير) nedir ve temel kalıbı nedir?', ar: 'ما هو التصغير (تصغير) وما هو وزنه الأساسي؟' }, expected: { en: 'Expresses smallness or endearment. Basic pattern: فُعَيْلٌ — e.g. كَلْبٌ → كُلَيْبٌ (little dog), كِتَابٌ → كُتَيِّبٌ (booklet)', tr: 'Küçüklüğü veya sevimliliği ifade eder. Temel kalıp: فُعَيْلٌ — örn. كَلْبٌ → كُلَيْبٌ (küçük köpek), كِتَابٌ → كُتَيِّبٌ (kitapçık)', ar: 'تعبير عن الصغر أو التحبب. الوزن الأساسي: فُعَيْلٌ — مثال: كَلْبٌ → كُلَيْبٌ (كلب صغير), كِتَابٌ → كُتَيِّبٌ (كتيب)' } },
          { type: 'vocabulary', q: { en: 'What does مَشْرِقٌ mean and what type of noun is it?', tr: 'مَشْرِقٌ ne anlama gelir ve ne tür bir isimdir?', ar: 'ماذا تعني مَشْرِقٌ وما نوع الاسم الذي هي عليه؟' }, expected: { en: 'مَشْرِقٌ = the East / place of sunrise — it is an اسم مكان (noun of place), from شَرَقَ (to rise/shine)', tr: 'مَشْرِقٌ = Doğu / güneşin doğduğu yer — bu bir اسم مكان\'dır (mekan ismi), شَرَقَ (doğmak/parlamak) fiilinden türemiştir.', ar: 'مَشْرِقٌ = المشرق / مكان الشروق — وهو اسم مكان، من شَرَقَ (أشرق/سطع)' } },
        ]
      },
      {
        week: 3, pdf: 'Level-3/31st Lesson Line Spacing 2.0.pdf',
        title: { en: 'Introduction to Defective Verbs (Fi\'l Mu\'tall) — Classification of Sound and Weak Verbs', tr: 'İlletli Fiillere Giriş — Sahih ve Mu\'tell Fiillerin Sınıflandırılması', ar: 'مقدمة في الفعل المعتل — تصنيف الأفعال الصحيحة والمعتلة' },
        questions: [
          { type: 'grammar', q: { en: 'What is the Sifat Mushabbaha (الصفة المشبهة) and how does it differ from the active participle?', tr: 'Sıfat-ı Müşebbehe (الصفة المشبهة) nedir ve ism-i failden farkı nedir?', ar: 'ما هي الصفة المشبهة (الصفة المشبهة) وما الفرق بينها وبين اسم الفاعل؟' }, expected: { en: 'It expresses a permanent or inherent quality (not a temporary action). Pattern: فَعِيلٌ, فَعِلٌ, فَعْلَانٌ etc. — e.g. كَرِيمٌ (generous by nature), حَسَنٌ (beautiful/good)', tr: 'Kalıcı veya doğuştan gelen bir niteliği (geçici bir eylemi değil) ifade eder. Kalıp: فَعِيلٌ, فَعِلٌ, فَعْلَانٌ vb. — örn. كَرِيمٌ (doğuştan cömert), حَسَنٌ (güzel/iyi)', ar: 'تعبر عن صفة دائمة أو متأصلة (وليست فعلاً مؤقتاً). الأوزان: فَعِيلٌ, فَعِلٌ, فَعْلَانٌ إلخ. — مثال: كَرِيمٌ (كريم بالطبع), حَسَنٌ (جميل/جيد)' } },
          { type: 'grammar', q: { en: 'What makes a verb "defective" (فعل معتل / illetli fiil)?', tr: 'Bir fiili "illetli" (فعل معتل / illetli fiil) yapan nedir?', ar: 'ما الذي يجعل الفعل "معتلاً" (فعل معتل / illetli fiil)؟' }, expected: { en: 'Having a weak letter (حرف علة) — و، ا، ي — in one of the three root positions', tr: 'Üç kök harfinden birinde illet harfi (حرف علة) — و، ا، ي — bulunması', ar: 'وجود حرف علة (حرف علة) — و، ا، ي — في أحد المواضع الثلاثة للأحرف الأصلية' } },
          { type: 'grammar', q: { en: 'What are the three types of defective verbs?', tr: 'Üç tür illetli fiil nedir?', ar: 'ما هي أنواع الأفعال المعتلة الثلاثة؟' }, expected: { en: 'Mithal (مثال): weak first letter — وَقَفَ · Ajwaf (أجوف): weak middle letter — قَالَ، بَاعَ · Naqis (ناقص): weak final letter — دَعَا، رَمَى', tr: 'Misal (مثال): ilk harfi illetli — وَقَفَ · Ecvef (أجوف): orta harfi illetli — قَالَ، بَاعَ · Nakıs (ناقص): son harfi illetli — دَعَا، رَمَى', ar: 'مثال (مثال): حرف العلة في الأول — وَقَفَ · أجوف (أجوف): حرف العلة في الوسط — قَالَ، بَاعَ · ناقص (ناقص): حرف العلة في الآخر — دَعَا، رَمَى' } },
          { type: 'vocabulary', q: { en: 'Is قَالَ a defective verb? What type and what is its root?', tr: 'قَالَ illetli bir fiil midir? Hangi türdendir ve kökü nedir?', ar: 'هل قَالَ فعل معتل؟ وما نوعه وما هو أصله؟' }, expected: { en: 'Yes — Ajwaf (weak middle letter). Root: ق-و-ل. The و becomes ا in the past: قَالَ (he said)', tr: 'Evet — Ecvef (orta harfi illetli). Kök: ق-و-ل. Mazi fiilde و, ا\'ya dönüşür: قَالَ (o dedi)', ar: 'نعم — أجوف (حرف العلة في الوسط). الأصل: ق-و-ل. تصبح الواو ألفاً في الماضي: قَالَ (قال هو)' } },
          { type: 'grammar', q: { en: 'Give two Quranic examples of Sifat Mushabbaha adjectives.', tr: 'Sıfat-ı Müşebbehe sıfatlarına iki Kur\'an örneği veriniz.', ar: 'اذكر مثالين قرآنيين لصفات مشبهة.' }, expected: { en: 'كَرِيمٌ (noble/generous), عَظِيمٌ (great), حَكِيمٌ (wise), جَمِيلٌ (beautiful), قَوِيٌّ (strong)', tr: 'كَرِيمٌ (yüce/cömert), عَظِيمٌ (büyük), حَكِيمٌ (bilge), جَمِيلٌ (güzel), قَوِيٌّ (güçlü)', ar: 'كَرِيمٌ (نبيل/كريم), عَظِيمٌ (عظيم), حَكِيمٌ (حكيم), جَمِيلٌ (جميل), قَوِيٌّ (قوي)' } },
        ]
      },
      {
        week: 4, pdf: 'Level-3/32nd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Conjugation of Defective Verbs (Past Tense) — All Weak Verb Types', tr: 'İlletli Fiillerin Çekimi (Mazi) — Tüm Zayıf Fiil Türleri', ar: 'تصريف الأفعال المعتلة في الماضي — جميع الأنواع' },
        questions: [
          { type: 'grammar', q: { en: 'In the Ajwaf verb قَالَ, what happens to the weak middle letter in the jussive?', tr: 'Ecvef fiil قَالَ\'de, meczum (cezmli) halde orta illet harfi ne olur?', ar: 'في الفعل الأجوف قَالَ، ماذا يحدث لحرف العلة الأوسط في حالة الجزم؟' }, expected: { en: 'It drops: لَمْ يَقُلْ (the و drops and the ق gets a sukun)', tr: 'Düşer: لَمْ يَقُلْ (و düşer ve ق cezim alır)', ar: 'يحذف: لَمْ يَقُلْ (تحذف الواو وتصبح القاف ساكنة)' } },
          { type: 'grammar', q: { en: 'Conjugate دَعَا (Naqis verb — he called/invited) for "she called."', tr: 'دَعَا (Nakıs fiil — o çağırdı/davet etti) fiilini "o (kadın) çağırdı" için çekimleyiniz.', ar: 'صرف الفعل دَعَا (فعل ناقص — دعا/دعا) لـ "هي دعت".' }, expected: { en: 'دَعَتْ (the final ا drops before تْ)', tr: 'دَعَتْ (sonundaki ا, تْ\'den önce düşer)', ar: 'دَعَتْ (تحذف الألف النهائية قبل تْ)' } },
          { type: 'grammar', q: { en: 'What is the jussive form of يَدْعُو (he calls)?', tr: 'يَدْعُو (o çağırır) fiilinin meczum (cezmli) hali nedir?', ar: 'ما هي صيغة الجزم للفعل يَدْعُو (هو يدعو)؟' }, expected: { en: 'يَدْعُ (the و drops in jussive): لَمْ يَدْعُ = he did not call', tr: 'يَدْعُ (cezimli halde و düşer): لَمْ يَدْعُ = o çağırmadı', ar: 'يَدْعُ (تحذف الواو في الجزم): لَمْ يَدْعُ = لم يدعُ هو' } },
          { type: 'grammar', q: { en: 'What happens to a Mithal verb like وَقَفَ in the imperative?', tr: 'وَقَفَ gibi bir Misal fiilde emir kipinde ne olur?', ar: 'ماذا يحدث لفعل مثال مثل وَقَفَ في صيغة الأمر؟' }, expected: { en: 'The initial و drops: يَقِفُ → قِفْ (Stop!) — the hamzat al-wasl is also not needed since the word now starts with a consonant', tr: 'Baştaki و düşer: يَقِفُ → قِفْ (Dur!) — kelime şimdi bir sessiz harfle başladığı için vasıl hemzesine de gerek kalmaz', ar: 'تحذف الواو الأولى: يَقِفُ → قِفْ (توقف!) — ولا حاجة بهمزة الوصل لأن الكلمة تبدأ الآن بحرف ساكن' } },
          { type: 'translation', q: { en: 'Translate: وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ', tr: 'Çeviriniz: وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ', ar: 'ترجم الآية: وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ' }, expected: { en: 'And your Lord said: Call upon Me, I will respond to you (Surah Ghafir 40:60)', tr: 'Ve Rabbiniz buyurdu ki: Bana dua edin, size icabet edeyim (Gafir Suresi 40:60)', ar: 'وقال ربكم: ادعوني أستجب لكم (سورة غافر 40:60)' } },
        ]
      },
      {
        week: 5, pdf: 'Level-3/33rd Lesson Line Spacing 2.0.pdf',
        title: { en: 'Defective Verbs: Full Conjugation Tables (Imperfect, Imperative, Negation with لَنْ and لا)', tr: 'İlletli Fiiller: Tam Çekim Tabloları (Muzari, Emir, لَنْ ve لا ile Olumsuzluk)', ar: 'الأفعال المعتلة: جداول التصريف الكاملة (مضارع، أمر، النفي بلَنْ ولا)' },
        questions: [
          { type: 'grammar', q: { en: 'Conjugate جَاءَ (he came) for "they (masc. pl.) came."', tr: 'جَاءَ (o geldi) fiilini "onlar (erkek çoğul) geldiler" için çekimleyiniz.', ar: 'صرف الفعل جَاءَ (هو جاء) لـ "هم جاؤوا" (جمع مذكر).' }, expected: { en: 'جَاؤُوا (the ء is retained, و added for plural)', tr: 'جَاؤُوا (ء korunur, çoğul için و eklenir)', ar: 'جَاؤُوا (تبقى الهمزة، وتضاف الواو للجمع)' } },
          { type: 'grammar', q: { en: 'What is the passive of قَالَ (he said)?', tr: 'قَالَ (o dedi) fiilinin meçhulü (pasifi) nedir?', ar: 'ما هو المبني للمجهول للفعل قَالَ (قال هو)؟' }, expected: { en: 'قِيلَ (it was said) — the vowel pattern changes to فِيلَ for Ajwaf passives', tr: 'قِيلَ (denildi) — Ecvef meçhuller için hareke kalıbı فِيلَ\'ye dönüşür', ar: 'قِيلَ (قيل) — يتغير نمط الحركات إلى فِيلَ في الأفعال الأجوف المبنية للمجهول' } },
          { type: 'grammar', q: { en: 'What is the passive of بَاعَ (he sold)?', tr: 'بَاعَ (o sattı) fiilinin meçhulü (pasifi) nedir?', ar: 'ما هو المبني للمجهول للفعل بَاعَ (باع هو)؟' }, expected: { en: 'بِيعَ (it was sold) — same فِيلَ pattern for Ajwaf', tr: 'بِيعَ (satıldı) — Ecvef için aynı فِيلَ kalıbı', ar: 'بِيعَ (بيع) — نفس نمط فِيلَ للأجوف' } },
          { type: 'translation', q: { en: 'Translate: وَقِيلَ يَا أَرْضُ ابْلَعِي مَاءَكِ', tr: 'Çeviriniz: وَقِيلَ يَا أَرْضُ ابْلَعِي مَاءَكِ', ar: 'ترجم الآية: وَقِيلَ يَا أَرْضُ ابْلَعِي مَاءَكِ' }, expected: { en: 'And it was said: O earth, swallow your water (Surah Hud 11:44 — قِيلَ = passive of قَالَ)', tr: 'Ve denildi ki: Ey yer, suyunu yut (Hud Suresi 11:44 — قِيلَ = قَالَ\'nin meçhulü)', ar: 'وقيل: يا أرض ابلعي ماءك (سورة هود 11:44 — قِيلَ = مبني للمجهول من قَالَ)' } },
          { type: 'grammar', q: { en: 'What is the jussive of يَرَى (he sees — Naqis)?', tr: 'يَرَى (o görür — Nakıs) fiilinin meczum hali nedir?', ar: 'ما هي صيغة الجزم للفعل يَرَى (هو يرى — ناقص)؟' }, expected: { en: 'يَرَ (the final ى drops): لَمْ يَرَ = he did not see', tr: 'يَرَ (son ى düşer): لَمْ يَرَ = o görmedi', ar: 'يَرَ (تحذف الياء النهائية): لَمْ يَرَ = لم يرَ هو' } },
        ]
      },
      {
        week: 6, pdf: 'Level-3/34th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Conditional Sentences and Conditional Particles in Arabic', tr: 'Şart Cümlesi ve Şart Edatları', ar: 'أسلوب الشرط وأدواته' },
        questions: [
          { type: 'grammar', q: { en: 'What are the two parts of a conditional sentence in Arabic?', tr: 'Arapça şart cümlesinin iki bölümü nedir?', ar: 'ما هما الجزآن الرئيسيان للجملة الشرطية في اللغة العربية؟' }, expected: { en: 'Condition (شرط / protasis) and result (جواب الشرط / apodosis). Both verbs are typically jussive.', tr: 'Şart (شرط / protasis) ve cevap (جواب الشرط / apodosis). Her iki fiil de genellikle meczumdur.', ar: 'الشرط (شرط / protasis) والجواب (جواب الشرط / apodosis). الفعلان كلاهما مجزومان عادة.' } },
          { type: 'grammar', q: { en: 'What is the difference between إِنْ and إِذَا in conditionals?', tr: 'Şart cümlelerinde إِنْ ve إِذَا arasındaki fark nedir?', ar: 'ما الفرق بين إِنْ و إِذَا في الجمل الشرطية؟' }, expected: { en: 'إِنْ = for uncertain/hypothetical conditions · إِذَا = for expected/likely conditions. Both are followed by jussive or past verb.', tr: 'إِنْ = belirsiz/varsayımsal koşullar için · إِذَا = beklenen/muhtemel koşullar için. Her ikisi de meczum veya mazi fiil ile takip edilir.', ar: 'إِنْ = للظروف غير المؤكدة/الافتراضية · إِذَا = للظروف المتوقعة/المحتملة. كلاهما يتبعه فعل مجزوم أو فعل ماضٍ.' } },
          { type: 'vocabulary', q: { en: 'What do the conditional particles مَنْ, مَا, أَيْنَمَا, مَتَى mean?', tr: 'مَنْ, مَا, أَيْنَمَا, مَتَى şart edatları ne anlama gelir?', ar: 'ماذا تعني أدوات الشرط مَنْ, مَا, أَيْنَمَا, مَتَى؟' }, expected: { en: 'مَنْ = whoever · مَا = whatever · أَيْنَمَا = wherever · مَتَى = whenever', tr: 'مَنْ = kim (her kim) · مَا = ne (her ne) · أَيْنَمَا = nerede (her nerede) · مَتَى = ne zaman (her ne zaman)', ar: 'مَنْ = من · مَا = ما · أَيْنَمَا = أينما · مَتَى = متى' } },
          { type: 'translation', q: { en: 'Translate: مَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ', tr: 'Çeviriniz: مَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ', ar: 'ترجم الآية: مَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ' }, expected: { en: 'Whoever does an atom\'s weight of good will see it (Surah Az-Zalzalah 99:7)', tr: 'Kim zerre ağırlığınca bir hayır işlerse onu görecektir (Zilzal Suresi 99:7)', ar: 'من يعمل مثقال ذرة خيراً يره (سورة الزلزلة 99:7)' } },
          { type: 'grammar', q: { en: 'When is فَـ required at the start of the result clause (جواب الشرط)?', tr: 'Cevap cümlesinin (جواب الشرط) başında فَـ ne zaman gereklidir?', ar: 'متى يجب استخدام الفاء (فَـ) في بداية جواب الشرط؟' }, expected: { en: 'When the result clause is a nominal sentence, imperative, negative لا/لن/لم, or begins with قَدْ or سَـ/سَوْفَ', tr: 'Cevap cümlesi isim cümlesi olduğunda, emir olduğunda, olumsuz لا/لن/لم içerdiğinde veya قَدْ ya da سَـ/سَوْفَ ile başladığında', ar: 'عندما يكون جواب الشرط جملة اسمية، أو فعل أمر، أو منفياً بـ لا/لن/لم، أو يبدأ بـ قَدْ أو سَـ/سَوْفَ' } },
        ]
      },
      {
        week: 7, pdf: 'Level-3/35th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Circumstantial Accusative (Hal) and Specification (Tamyiz)', tr: 'Hal ve Temyiz', ar: 'الحال والتمييز' },
        questions: [
          { type: 'grammar', q: { en: 'What is the Hal (الحال) and what case does it take?', tr: 'Hal (الحال) nedir ve hangi halde bulunur?', ar: 'ما هو الحال (الحال) وما هي حالته الإعرابية؟' }, expected: { en: 'A noun/adjective/clause in the accusative describing the state of the doer or object when the action occurs. Takes accusative (منصوب).', tr: 'Eylem gerçekleştiğinde failin veya nesnenin durumunu açıklayan, nasp (üstün) halinde olan bir isim/sıfat/cümle. Nasp (منصوب) halini alır.', ar: 'اسم أو صفة أو جملة منصوبة تصف حالة الفاعل أو المفعول به عند وقوع الفعل. يكون منصوباً (منصوب).' } },
          { type: 'translation', q: { en: 'Translate and identify the Hal: جَاءَ زَيْدٌ رَاكِبًا', tr: 'Çeviriniz ve Hal\'i belirleyiniz: جَاءَ زَيْدٌ رَاكِبًا', ar: 'ترجم وحدد الحال: جَاءَ زَيْدٌ رَاكِبًا' }, expected: { en: 'Zayd came riding. Ø±ÙØ§ÙÙØ¨ÙØ§ = Hal (accusative) describing Zayd\'s state when he came.', tr: 'Zeyd binmiş olarak geldi. رَاكِبًا = Hal (nasp halinde) Zeyd\'in geldiğindeki durumunu tanımlar.', ar: 'جاء زيد راكباً. رَاكِبًا = حال (منصوب) يصف حالة زيد عند مجيئه.' } },
          { type: 'grammar', q: { en: 'What is the Tamyiz (التمييز) and what case does it take?', tr: 'Temyiz (التمييز) nedir ve hangi halde bulunur?', ar: 'ما هو التمييز (التمييز) وما هي حالته الإعرابية؟' }, expected: { en: 'A noun in the accusative specifying/clarifying a vague number, measure, or comparison. Takes accusative: عِشْرُونَ كِتَابًا = twenty books', tr: 'Belirsiz bir sayı, ölçü veya karşılaştırmayı belirten/açıklayan, nasp (üstün) halinde bir isim. Nasp halini alır: عِشْرُونَ كِتَابًا = yirmi kitap', ar: 'اسم منصوب يوضح أو يفسر عدداً مبهماً، أو قياساً، أو مقارنة. يكون منصوباً: عِشْرُونَ كِتَابًا = عشرون كتاباً' } },
          { type: 'translation', q: { en: 'Translate: خُلِقَ الْإِنْسَانُ ضَعِيفًا', tr: 'Çeviriniz: خُلِقَ الْإِنْسَانُ ضَعِيفًا', ar: 'ترجم الآية: خُلِقَ الْإِنْسَانُ ضَعِيفًا' }, expected: { en: 'Man was created weak (Ø¶ÙØ¹ÙÙÙÙØ§ = Hal â accusative â describing man\'s state at creation) (Surah An-Nisa 4:28)', tr: 'İnsan zayıf yaratılmıştır (ضَعِيفًا = Hal — nasp halinde — insanın yaratılışındaki durumunu tanımlar) (Nisa Suresi 4:28)', ar: 'خلق الإنسان ضعيفاً (ضَعِيفًا = حال — منصوب — يصف حالة الإنسان عند خلقه) (سورة النساء 4:28)' } },
          { type: 'grammar', q: { en: 'What is the difference between Hal and Khabar?', tr: 'Hal ve Haber arasındaki fark nedir?', ar: 'ما الفرق بين الحال والخبر؟' }, expected: { en: 'Hal is temporary â it describes the subject\'s state during the action. Khabar is a permanent/general predicate of the subject.', tr: 'Hal geçicidir — fiil sırasında öznenin durumunu tanımlar. Haber ise öznenin kalıcı/genel bir yüklemidir.', ar: 'الحال مؤقتة — تصف حالة الفاعل أثناء وقوع الفعل. الخبر هو محمول دائم/عام للفاعل.' } },
        ]
      },
      {
        week: 8, pdf: 'Level-3/36th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Arabic Cardinal Numbers (al-ʿAdad wa-l-Maʿdūd) and Apposition (al-Badal)', tr: 'Arapça Sayılar (el-Aded ve\'l-Ma\'dûd) ve Bedel', ar: 'العدد والمعدود والبدل' },
        questions: [
          { type: 'grammar', q: { en: 'What is the Badal (البدل — apposition) and what is its grammatical rule?', tr: 'Badal (البدل — açıklayıcı isim) nedir ve dilbilgisel kuralı nedir?', ar: 'ما هو البدل (البدل — Apposition) وما هي قاعدته النحوية؟' }, expected: { en: 'A noun that substitutes or clarifies the preceding noun (مبدل منه) and must agree with it in case: جَاءَ أَخُوكَ زَيْدٌ = Your brother Zayd came (زَيْدٌ = badal, nominative like أَخُوكَ)', tr: 'Önceki ismi (مبدل منه) yerine geçen veya açıklayan bir isim olup, durumunda ona uymalıdır: جَاءَ أَخُوكَ زَيْدٌ = Kardeşin Zeyd geldi (زَيْدٌ = bedel, أَخُوكَ gibi merfu).', ar: 'اسم يحل محل الاسم السابق (مبدل منه) أو يوضحه ويجب أن يتوافق معه في الحالة الإعرابية: جَاءَ أَخُوكَ زَيْدٌ = جاء أخوك زيد (زَيْدٌ = بدل، مرفوع مثل أَخُوكَ).' } },
          { type: 'grammar', q: { en: 'What is the gender rule for Arabic numbers 3–10?', tr: 'Arapça 3-10 arası sayılar için cinsiyet kuralı nedir?', ar: 'ما هي قاعدة الجنس للأعداد العربية 3–10؟' }, expected: { en: 'Numbers 3–10 take the opposite gender of the counted noun: ثَلَاثَةُ كُتُبٍ (three books — كُتُب is masculine, so number takes feminine ة)', tr: '3-10 arası sayılar, sayılan ismin zıt cinsiyetini alır: ثَلَاثَةُ كُتُبٍ (üç kitap — كُتُب müzekkerdir, bu yüzden sayı müennes ة alır).', ar: 'تأخذ الأعداد من 3 إلى 10 الجنس المعاكس للاسم المعدود: ثَلَاثَةُ كُتُبٍ (ثلاثة كتب — كُتُب مذكر، لذا يأخذ العدد تأنيث ة).' } },
          { type: 'grammar', q: { en: 'What case does the counted noun take after numbers 3–10?', tr: '3-10 arası sayılardan sonra sayılan isim hangi hali alır?', ar: 'ما هي الحالة الإعرابية التي يأخذها الاسم المعدود بعد الأعداد من 3 إلى 10؟' }, expected: { en: 'Genitive plural (مجرور جمع): ثَلَاثَةُ كُتُبٍ = three books', tr: 'Cerli çoğul (مجرور جمع): ثَلَاثَةُ كُتُبٍ = üç kitap', ar: 'جمع مجرور (مجرور جمع): ثَلَاثَةُ كُتُبٍ = ثلاثة كتب.' } },
          { type: 'translation', q: { en: 'Translate: إِنَّ عِدَّةَ الشُّهُورِ عِنْدَ اللَّهِ اثْنَا عَشَرَ شَهْرًا', tr: 'Çevir: إِنَّ عِدَّةَ الشُّهُورِ عِنْدَ اللَّهِ اثْنَا عَشَرَ شَهْرًا', ar: 'ترجم: إِنَّ عِدَّةَ الشُّهُورِ عِنْدَ اللَّهِ اثْنَا عَشَرَ شَهْرًا' }, expected: { en: 'Indeed the number of months with Allah is twelve months (Surah At-Tawbah 9:36)', tr: 'Şüphesiz Allah katında ayların sayısı on iki aydır (Tevbe Suresi 9:36)', ar: 'إن عدة الشهور عند الله اثنا عشر شهرا (سورة التوبة 9:36).' } },
          { type: 'grammar', q: { en: 'What case does the counted noun take after numbers 11–99?', tr: '11-99 arası sayılardan sonra sayılan isim hangi hali alır?', ar: 'ما هي الحالة الإعرابية التي يأخذها الاسم المعدود بعد الأعداد من 11 إلى 99؟' }, expected: { en: 'Accusative singular (تمييز منصوب): عِشْرُونَ كِتَابًا = twenty books', tr: 'Nasb halinde tekil (تمييز منصوب): عِشْرُونَ كِتَابًا = yirmi kitap', ar: 'مفرد منصوب (تمييز منصوب): عِشْرُونَ كِتَابًا = عشرون كتاباً.' } },
        ]
      },
      {
        week: 9, pdf: 'Level-3/37th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Diptote Nouns (Al-Mamnu\' min al-Sarf / Ghayrul Munsarif)', tr: 'Gayri Munsarif İsimler (Ğayrul Munsarif)', ar: 'الممنوع من الصرف' },
        questions: [
          { type: 'grammar', q: { en: 'What is a Ghayrul Munsarif (diptote) noun and how does it differ from regular nouns?', tr: 'Gayr-i Munsarif (diptot) isim nedir ve normal isimlerden farkı nedir?', ar: 'ما هو الاسم الممنوع من الصرف (Ghayrul Munsarif / diptote) وكيف يختلف عن الأسماء العادية؟' }, expected: { en: 'A noun that does not accept tanwin and uses fatha instead of kasra in the genitive case: مَرَرْتُ بِمَسَاجِدَ (not مَسَاجِدِ)', tr: 'Tenvin kabul etmeyen ve cer halinde kesra yerine fetha kullanan bir isimdir: مَرَرْتُ بِمَسَاجِدَ (مَسَاجِدِ değil).', ar: 'هو الاسم الذي لا يقبل التنوين ويستخدم الفتحة بدلاً من الكسرة في حالة الجر: مَرَرْتُ بِمَسَاجِدَ (وليس مَسَاجِدِ).' } },
          { type: 'grammar', q: { en: 'Name four conditions that make a noun a diptote.', tr: 'Bir ismi diptot yapan dört koşul söyleyin.', ar: 'اذكر أربعة شروط تجعل الاسم ممنوعًا من الصرف.' }, expected: { en: 'Any two conditions combine: proper name, feminine ending, foreign origin, adjective pattern أَفْعَل, broken plural on مَفَاعِل/مَفَاعِيل, added alif-nun (عُثْمَانُ)', tr: 'Herhangi iki koşul birleşebilir: özel isim, müenneslik son eki, yabancı kökenli, أَفْعَل sıfat kalıbı, مَفَاعِل/مَفَاعِيل vezninde cemi teksir, eklenmiş alif-nun (عُثْمَانُ).', ar: 'أي شرطين يجتمعان: اسم علم، مؤنث، أعجمي، صفة على وزن أَفْعَل، صيغة منتهى الجموع على وزن مَفَاعِل/مَفَاعِيل، زيادة ألف ونون (عُثْمَانُ).' } },
          { type: 'vocabulary', q: { en: 'Why is مَسَاجِدُ a diptote? Give its genitive form in a sentence.', tr: 'مَسَاجِدُ neden bir diptottur? Cümle içinde cer halini verin.', ar: 'لماذا مَسَاجِدُ ممنوع من الصرف؟ أعطِ صيغة الجر له في جملة.' }, expected: { en: 'It is a broken plural on the مَفَاعِل pattern. Genitive: مَرَرْتُ بِمَسَاجِدَ كَثِيرَةٍ (I passed by many mosques — fatha not kasra)', tr: 'O, مَفَاعِل vezninde bir cemi teksirdir. Cer hali: مَرَرْتُ بِمَسَاجِدَ كَثِيرَةٍ (Çok caminin yanından geçtim — kesra yerine fetha).', ar: 'إنها صيغة منتهى الجموع على وزن مَفَاعِل. الجر: مَرَرْتُ بِمَسَاجِدَ كَثِيرَةٍ (مررت بالعديد من المساجد — فتحة لا كسرة).' } },
          { type: 'grammar', q: { en: 'When does a diptote noun accept tanwin and kasra?', tr: 'Bir diptot isim ne zaman tenvin ve kesra kabul eder?', ar: 'متى يقبل الاسم الممنوع من الصرف التنوين والكسرة؟' }, expected: { en: 'When it has ال (definite article) or is in an idafa (genitive construction): فِي الْمَسَاجِدِ (with ال) / مَسَاجِدُ الْمَدِينَةِ (in idafa)', tr: 'ال (belirlilik takısı) aldığında veya bir izafet (tamlayan tamlanan) terkibinde olduğunda: فِي الْمَسَاجِدِ (ال ile) / مَسَاجِدُ الْمَدِينَةِ (izafet içinde).', ar: 'عندما يكون معرفاً بـ ال (definite article) أو في إضافة (genitive construction): فِي الْمَسَاجِدِ (مع ال) / مَسَاجِدُ الْمَدِينَةِ (في إضافة).' } },
          { type: 'translation', q: { en: 'Translate: لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ', tr: 'Çevir: لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ', ar: 'ترجم: لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ' }, expected: { en: 'We have certainly created man in the best of forms (Surah At-Tin 95:4 — أَحْسَنِ is diptote but has kasra here because it is in idafa)', tr: 'Biz insanı gerçekten en güzel şekilde yarattık (Tin Suresi 95:4 — أَحْسَنِ diptottur ama burada izafet içinde olduğu için kesra almıştır).', ar: 'ولقد خلقنا الإنسان في أحسن تقويم (سورة التين 95:4 — أَحْسَنِ ممنوع من الصرف ولكن أخذ الكسرة هنا لأنه مضاف).' } },
        ]
      },
      {
        week: 10, pdf: 'Level-3/38th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Declinable & Indeclinable Words (Mu\'rab & Mabni) and Relative Pronouns (Ism al-Mawsul)', tr: 'Mebni ve Mu\'rab Kelimeler ile İsm-i Mevsul', ar: 'المبني والمعرب والأسماء الموصولة' },
        questions: [
          { type: 'grammar', q: { en: 'What is the difference between Mabni (ÙØ¨ÙÙ) and Mu\'rab (ÙØ¹Ø±Ø¨) words?', tr: 'Mabni (مبني) ve Mu\'rab (معرب) kelimeler arasındaki fark nedir?', ar: 'ما الفرق بين الكلمات المبنية (مبني) والمعربة (معرب)؟' }, expected: { en: 'Mu\'rab words change their ending to show grammatical case. Mabni words have fixed endings regardless of their role: pronouns, demonstratives, relative pronouns are mabni.', tr: 'Mu\'rab kelimeler dilbilgisel durumu göstermek için sonlarını değiştirirler. Mabni kelimeler ise rollerine bakılmaksızın sabit sonlara sahiptir: zamirler, işaret zamirleri, ilgi zamirleri مبني\'dir.', ar: 'الكلمات المعربة تغير نهاياتها لإظهار الحالة الإعرابية. الكلمات المبنية لها نهايات ثابتة بغض النظر عن دورها: الضمائر وأسماء الإشارة والأسماء الموصولة كلها مبنية.' } },
          { type: 'vocabulary', q: { en: 'What are the main relative pronouns (أسماء موصولة) in Arabic?', tr: 'Arapça\'daki ana ilgi zamirleri (أسماء موصولة) nelerdir?', ar: 'ما هي الأسماء الموصولة الرئيسية في اللغة العربية؟' }, expected: { en: 'الَّذِي (masc. sing.), الَّتِي (fem. sing.), الَّذِينَ (masc. pl.), اللَّاتِي / اللَّوَاتِي (fem. pl.), مَنْ (whoever), مَا (whatever)', tr: 'الَّذِي (eril tekil), الَّتِي (dişil tekil), الَّذِينَ (eril çoğul), اللَّاتِي / اللَّوَاتِي (dişil çoğul), مَنْ (kimse), مَا (ne olursa olsun).', ar: 'الَّذِي (مذكر مفرد)، الَّتِي (مؤنث مفرد)، الَّذِينَ (مذكر جمع)، اللَّاتِي / اللَّوَاتِي (مؤنث جمع)، مَنْ (من)، مَا (ما).' } },
          { type: 'grammar', q: { en: 'What must every relative pronoun be followed by?', tr: 'Her ilgi zamiri ne ile takip edilmelidir?', ar: 'بماذا يجب أن يتبع كل اسم موصول؟' }, expected: { en: 'A relative clause (صلة الموصول) that contains a pronoun (عائد) referring back to the relative pronoun: الَّذِي كَتَبَ الْكِتَابَ = the one who wrote the book (هُوَ implied)', tr: 'İlgi zamirine geri dönen bir zamir (عائد) içeren bir ilgi cümlesi (صلة الموصول): الَّذِي كَتَبَ الْكِتَابَ = Kitabı yazan kişi (هُوَ ima edilir).', ar: 'جملة صلة الموصول (صلة الموصول) تحتوي على ضمير (عائد) يعود على الاسم الموصول: الَّذِي كَتَبَ الْكِتَابَ = الذي كتب الكتاب (هُوَ مضمر).' } },
          { type: 'translation', q: { en: 'Translate: الَّذِي خَلَقَ فَسَوَّى', tr: 'Çevir: الَّذِي خَلَقَ فَسَوَّى', ar: 'ترجم: الَّذِي خَلَقَ فَسَوَّى' }, expected: { en: 'The One who created and proportioned (Surah Al-A\'la 87:2)', tr: 'Yaratan ve düzenleyen (A\'la Suresi 87:2)', ar: 'الذي خلق فسوى (سورة الأعلى 87:2).' } },
          { type: 'grammar', q: { en: 'Why is الَّذِي considered mabni (indeclinable)?', tr: 'الَّذِي neden مبني (çekimlenemeyen) kabul edilir?', ar: 'لماذا يعتبر الَّذِي اسمًا مبنيًا؟' }, expected: { en: 'Its ending does not change regardless of its grammatical role: رَأَيْتُ الَّذِي كَتَبَ (object) vs. جَاءَ الَّذِي كَتَبَ (subject) — الَّذِي stays the same.', tr: 'Dilbilgisel rolü ne olursa olsun sonu değişmez: رَأَيْتُ الَّذِي كَتَبَ (nesne) ile جَاءَ الَّذِي كَتَبَ (özne) karşılaştırıldığında — الَّذِي aynı kalır.', ar: 'لأن نهايته لا تتغير بغض النظر عن دوره الإعرابي: رَأَيْتُ الَّذِي كَتَبَ (مفعول به) مقابل جَاءَ الَّذِي كَتَبَ (فاعل) — الَّذِي يبقى كما هو.' } },
        ]
      },
      {
        week: 11, pdf: 'Level-3/39th Lesson Line Spacing 2.0.pdf',
        title: { en: 'Exception (Istithna) and Absolute Object (Maf\'ul Mutlaq)', tr: 'İstisna ve Mef\'ul Mutlak', ar: 'الاستثناء والمفعول المطلق' },
        questions: [
          { type: 'grammar', q: { en: 'What particle introduces exception (استثناء) and what case does the exception noun typically take?', tr: 'İstisna (استثناء) bildiren edat nedir ve istisna ismi genellikle hangi hali alır?', ar: 'ما هي أداة الاستثناء (استثناء) وما هي الحالة الإعرابية التي يأخذها الاسم المستثنى عادةً؟' }, expected: { en: 'إِلَّا (except). In a complete affirmative sentence the exception (مستثنى) takes accusative: جَاءَ الطُّلَّابُ إِلَّا زَيْدًا', tr: 'إِلَّا (hariç). Tam ve olumlu bir cümlede istisna (مستثنى) nasb hali alır: جَاءَ الطُّلَّابُ إِلَّا زَيْدًا', ar: 'إِلَّا (إلا). في الجملة التامة المثبتة، يأخذ المستثنى (مستثنى) حالة النصب: جَاءَ الطُّلَّابُ إِلَّا زَيْدًا.' } },
          { type: 'translation', q: { en: 'Translate: لَا إِلَهَ إِلَّا اللَّهُ', tr: 'Çevir: لَا إِلَهَ إِلَّا اللَّهُ', ar: 'ترجم: لَا إِلَهَ إِلَّا اللَّهُ' }, expected: { en: 'There is no god except Allah (لا النافية للجنس — إِلَهَ is accusative as اسم لا; اللَّهُ is بدل or خبر)', tr: 'Allah\'tan başka ilah yoktur (لا النافية للجنس — إِلَهَ, اسم لا olarak nasb halindedir; اللَّهُ, بدل veya haberdir).', ar: 'لا إله إلا الله (لا النافية للجنس — إِلَهَ منصوب على أنه اسم لا؛ اللَّهُ بدل أو خبر).' } },
          { type: 'grammar', q: { en: 'What is the Maf\'ul Mutlaq (Ø§ÙÙÙØ¹ÙÙ Ø§ÙÙØ·ÙÙ â absolute object) and why is it used?', tr: 'Mef\'ul Mutlak (المفعول المطلق — mutlak nesne) nedir ve neden kullanılır?', ar: 'ما هو المفعول المطلق (المفعول المطلق — absolute object) ولماذا يستخدم؟' }, expected: { en: 'A masdar in the accusative from the same root as the verb, used for: 1) emphasis, 2) describing manner, 3) specifying number: ضَرَبَ ضَرْبًا شَدِيدًا (he struck a hard blow)', tr: 'Fiille aynı kökten gelen, nasb halinde bir masdardır; şu amaçlarla kullanılır: 1) vurgu, 2) tarzı açıklama, 3) sayıyı belirtme: ضَرَبَ ضَرْبًا شَدِيدًا (şiddetli bir darbe vurdu).', ar: 'هو مصدر منصوب من نفس جذر الفعل، يستخدم لـ: 1) التوكيد، 2) بيان النوع، 3) بيان العدد: ضَرَبَ ضَرْبًا شَدِيدًا (ضرب ضرباً شديداً).' } },
          { type: 'translation', q: { en: 'Translate: وَكَلَّمَ اللَّهُ مُوسَى تَكْلِيمًا', tr: 'Çevir: وَكَلَّمَ اللَّهُ مُوسَى تَكْلِيمًا', ar: 'ترجم: وَكَلَّمَ اللَّهُ مُوسَى تَكْلِيمًا' }, expected: { en: 'And Allah spoke directly to Musa (Surah An-Nisa 4:164 â ØªÙÙÙÙÙÙÙÙØ§ = maf\'ul mutlaq emphasizing the directness of speech)', tr: 'Ve Allah, Musa ile gerçekten konuştu (Nisa Suresi 4:164 — تَكْلِيمًا = konuşmanın doğrudanlığını vurgulayan mef\'ul mutlak).', ar: 'وكلم الله موسى تكليما (سورة النساء 4:164 — تَكْلِيمًا = مفعول مطلق يؤكد مباشرة الكلام).' } },
          { type: 'grammar', q: { en: 'What are the three other exception particles besides إِلَّا?', tr: 'إِلَّا dışında diğer üç istisna edatı nelerdir?', ar: 'ما هي أدوات الاستثناء الثلاث الأخرى غير إِلَّا؟' }, expected: { en: 'غَيْرُ and سِوَى (other than), خَلَا، عَدَا، حَاشَا (except — verbal exceptions)', tr: 'غَيْرُ ve سِوَى (başka), خَلَا، عَدَا، حَاشَا (hariç — fiilî istisnalar).', ar: 'غَيْرُ و سِوَى (غير)، خَلَا، عَدَا، حَاشَا (ما عدا — استثناءات فعلية).' } },
        ]
      },
      {
        week: 12, pdf: 'Level-3/40th Lesson Line Spacing2.0 .pdf',
        title: { en: 'Emphasis (Tawkid): Emphatic Lam, Emphatic Nun (Nun al-Tawkid al-Thaqila and Khafifa)', tr: 'Te\'kid: Te\'kid Lamı, Te\'kid Nunu (Ağır ve Hafif Nun)', ar: 'التوكيد: لام التوكيد ونونا التوكيد الثقيلة والخفيفة' },
        questions: [
          { type: 'grammar', q: { en: 'What is لام التوكيد (Emphatic Lam) and where is it used?', tr: 'لام التوكيد (Vurgu Lamı) nedir ve nerede kullanılır?', ar: 'ما هي لام التوكيد (Emphatic Lam) وأين تستخدم؟' }, expected: { en: 'A لـ added for emphasis, often with إِنَّ: إِنَّ اللَّهَ لَغَفُورٌ (Indeed Allah is truly All-Forgiving). Also used in oaths.', tr: 'Vurgu için eklenen bir لـ\'dir, genellikle إِنَّ ile birlikte kullanılır: إِنَّ اللَّهَ لَغَفُورٌ (Şüphesiz Allah gerçekten çok bağışlayıcıdır). Ayrıca yeminlerde de kullanılır.', ar: 'لـ تضاف للتوكيد، وغالباً مع إِنَّ: إِنَّ اللَّهَ لَغَفُورٌ (إن الله لغفور). تستخدم أيضاً في القسم.' } },
          { type: 'grammar', q: { en: 'What is نون التوكيد (Emphatic Nun) and its two forms?', tr: 'نون التوكيد (Vurgu Nunu) nedir ve iki şekli nelerdir?', ar: 'ما هي نون التوكيد (Emphatic Nun) وصيغتاها؟' }, expected: { en: 'Heavy ن (ـَنَّ) and light ن (ـَنْ) added to verbs for emphasis, often after oaths: وَاللَّهِ لَأَكْتُبَنَّ = By Allah I will surely write', tr: 'Fiillere vurgu için eklenen ağır ن (ـَنَّ) ve hafif ن (ـَنْ), genellikle yeminlerden sonra: وَاللَّهِ لَأَكْتُبَنَّ = Allah\'a yemin olsun ki kesinlikle yazacağım.', ar: 'نون التوكيد الثقيلة (ـَنَّ) والخفيفة (ـَنْ) تضافان للأفعال للتوكيد، وغالباً بعد القسم: وَاللَّهِ لَأَكْتُبَنَّ = والله لأكتبن.' } },
          { type: 'translation', q: { en: 'Translate: وَإِنَّ رَبَّكَ لَذُو فَضْلٍ عَلَى النَّاسِ', tr: 'Çevir: وَإِنَّ رَبَّكَ لَذُو فَضْلٍ عَلَى النَّاسِ', ar: 'ترجم: وَإِنَّ رَبَّكَ لَذُو فَضْلٍ عَلَى النَّاسِ' }, expected: { en: 'And indeed your Lord is full of bounty for the people (Surah An-Naml 27:73 — لَـ + إِنَّ = double emphasis)', tr: 'Ve şüphesiz Rabbin, insanlar üzerinde büyük lütuf sahibidir (Neml Suresi 27:73 — لَـ + إِنَّ = çift vurgu).', ar: 'وإن ربك لذو فضل على الناس (سورة النمل 27:73 — لَـ + إِنَّ = توكيد مزدوج).' } },
          { type: 'grammar', q: { en: 'What is the effect of combining إِنَّ and لَـ together?', tr: 'إِنَّ ve لَـ\'yı birleştirmenin etkisi nedir?', ar: 'ما هو تأثير الجمع بين إِنَّ و لَـ معاً؟' }, expected: { en: 'Double emphasis: إِنَّكَ لَعَلَى خُلُقٍ عَظِيمٍ = And indeed you are truly of great character (two emphatic particles)', tr: 'Çift vurgu: إِنَّكَ لَعَلَى خُلُقٍ عَظِيمٍ = Ve şüphesiz sen gerçekten yüce bir ahlak üzeresin (iki vurgu edatı).', ar: 'توكيد مزدوج: إِنَّكَ لَعَلَى خُلُقٍ عَظِيمٍ = وإنك لعلى خلق عظيم (اداتي توكيد).' } },
          { type: 'grammar', q: { en: 'What is tawkid with repeated nouns (التوكيد اللفظي والمعنوي)?', tr: 'Tekrarlanan isimlerle te\'kid (التوكيد اللفظي والمعنوي) nedir?', ar: 'ما هو التوكيد بالأسماء المكررة (التوكيد اللفظي والمعنوي)؟' }, expected: { en: 'Tawkid lafzi = repeating the word itself (Ø¬ÙØ§Ø¡Ù Ø¬ÙØ§Ø¡Ù Ø²ÙÙÙØ¯Ù). Tawkid ma\'nawi = using words like ÙÙÙÙÙØ ÙÙÙÙØ³ÙØ Ø¹ÙÙÙÙÙ: Ø¬ÙØ§Ø¡Ù Ø²ÙÙÙØ¯Ù ÙÙÙÙØ³ÙÙÙ (Zayd himself came)', tr: 'Lafzî te\'kid = kelimenin kendisini tekrarlamaktır (جَاءَ جَاءَ زَيْدٌ). Ma\'nevî te\'kid = كُلٌّ، نَفْسٌ، عَيْنٌ gibi kelimeleri kullanmaktır: جَاءَ زَيْدٌ نَفْسُهُ (Zeyd\'in kendisi geldi).', ar: 'التوكيد اللفظي = تكرار الكلمة نفسها (جَاءَ جَاءَ زَيْدٌ). التوكيد المعنوي = استخدام كلمات مثل كُلٌّ، نَفْسٌ، عَيْنٌ: جَاءَ زَيْدٌ نَفْسُهُ (جاء زيد نفسه).' } },
        ]
      },
      {
        week: 13, pdf: 'Level-3/41st Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Augmented (Derived) Verb Forms: Triliteral with One, Two, and Three Added Letters (Forms II–V)', tr: 'Mezid Fiiller: Bir, İki ve Üç Harfle Türetilmiş Fiil Kalıpları (II–V. Bablar)', ar: 'الفعل المزيد الثلاثي بحرف وبحرفين وبثلاثة أحرف (الأبواب الثاني حتى الخامس)' },
        questions: [
          { type: 'grammar', q: { en: 'What is the difference between a bare verb (فعل مجرد) and an augmented verb (فعل مزيد)?', tr: 'Bir فعل مجرد (yalın fiil) ile bir فعل مزيد (artırılmış fiil) arasındaki fark nedir?', ar: 'ما الفرق بين الفعل المجرد (فعل مجرد) والفعل المزيد (فعل مزيد)؟' }, expected: { en: 'Bare verb: all letters are root letters (كَتَبَ — 3 root letters). Augmented verb: extra letters added to change meaning (كَاتَبَ، تَكَاتَبَ)', tr: 'Yalın fiil (فعل مجرد): tüm harfler kök harflerdir (كَتَبَ — 3 kök harfi). Artırılmış fiil (فعل مزيد): anlamı değiştirmek için ek harfler eklenir (كَاتَبَ، تَكَاتَبَ)', ar: 'الفعل المجرد: جميع الحروف أصلية (كَتَبَ — 3 حروف أصلية). الفعل المزيد: حروف زائدة تضاف لتغيير المعنى (كَاتَبَ، تَكَاتَبَ)' } },
          { type: 'grammar', q: { en: 'What does Form II (فَعَّلَ) typically add to the meaning?', tr: 'Form II (فَعَّلَ) genellikle anlama ne katar?', ar: 'ماذا يضيف الوزن الثاني (فَعَّلَ) عادةً إلى المعنى؟' }, expected: { en: 'Causative or intensive: عَلِمَ (to know) → عَلَّمَ (to teach = cause to know); كَسَّرَ (to shatter = intensive of breaking)', tr: 'Ettirgen veya şiddetlendirme: عَلِمَ (bilmek) → عَلَّمَ (öğretmek = bilmeye neden olmak); كَسَّرَ (parçalamak = kırmanın şiddetlendirilmiş hali)', ar: 'للتعدية أو التكثير: عَلِمَ (عرف) → عَلَّمَ (درّس = جعله يعلم)؛ كَسَّرَ (حطّم = تكثيف للكسر)' } },
          { type: 'grammar', q: { en: 'What does Form III (فَاعَلَ) typically indicate?', tr: 'Form III (فَاعَلَ) genellikle neyi ifade eder?', ar: 'ماذا يدل عليه الوزن الثالث (فَاعَلَ) عادةً؟' }, expected: { en: 'Mutual/reciprocal action between two parties: قَاتَلَ (to fight each other), كَاتَبَ (to correspond/write to each other), جَالَسَ (to sit with)', tr: 'İki taraf arasında karşılıklı/mütekabil eylem: قَاتَلَ (birbirleriyle savaşmak), كَاتَبَ (birbirleriyle yazışmak), جَالَسَ (biriyle oturmak)', ar: 'الفعل المتبادل بين طرفين: قَاتَلَ (قاتل بعضهم بعضاً)، كَاتَبَ (تراسل/كتب لبعضهم البعض)، جَالَسَ (جلس مع)' } },
          { type: 'grammar', q: { en: 'What does Form IV (أَفْعَلَ) typically mean?', tr: 'Form IV (أَفْعَلَ) genellikle ne anlama gelir?', ar: 'ماذا يعني الوزن الرابع (أَفْعَلَ) عادةً؟' }, expected: { en: 'Causative: خَرَجَ (to go out) → أَخْرَجَ (to bring out/expel); سْلَمَ → أَسْلَمَ (to submit/become Muslim)', tr: 'Ettirgen: خَرَجَ (çıkmak) → أَخْرَجَ (çıkarmak/kovmak); سْلَمَ → أَسْلَمَ (teslim olmak/Müslüman olmak)', ar: 'للتعدية: خَرَجَ (خرج) → أَخْرَجَ (أخرج/طرد)؛ سْلَمَ → أَسْلَمَ (أسلم/أصبح مسلماً)' } },
          { type: 'grammar', q: { en: 'What does Form V (تَفَعَّلَ) typically mean in relation to Form II?', tr: 'Form V (تَفَعَّلَ) genellikle Form II ile ilişkili olarak ne anlama gelir?', ar: 'ماذا يعني الوزن الخامس (تَفَعَّلَ) عادةً بالنسبة للوزن الثاني؟' }, expected: { en: 'Reflexive of Form II: عَلَّمَ (to teach) → تَعَلَّمَ (to learn = teach oneself); كَسَّرَ → تَكَسَّرَ (to be shattered)', tr: 'Form II\'nin dönüşlüsü: عَلَّمَ (öğretmek) → تَعَلَّمَ (öğrenmek = kendi kendine öğretmek); كَسَّرَ → تَكَسَّرَ (parçalanmak)', ar: 'مطاوعة الوزن الثاني: عَلَّمَ (علّم) → تَعَلَّمَ (تعلّم = علّم نفسه)؛ كَسَّرَ → تَكَسَّرَ (تكسّر)' } },
        ]
      },
      {
        week: 14, pdf: 'Level-3/42nd Lesson Line Spacing 2.0 .pdf',
        title: { en: 'Derived Verb Forms (Augmented Triliteral and Quadriliteral): Forms VII, VIII, X, and Quadriliteral Patterns', tr: 'Türetilmiş Fiil Kalıpları: VII., VIII., X. Bablar ve Dörtlü Kök Fiiller', ar: 'الفعل المجرد والفعل المزيد: الأبواب السابع والثامن والعاشر والرباعي المزيد' },
        questions: [
          { type: 'grammar', q: { en: 'What does Form VI (تَفَاعَلَ) typically mean?', tr: 'Form VI (تَفَاعَلَ) genellikle ne anlama gelir?', ar: 'ماذا يعني الوزن السادس (تَفَاعَلَ) عادةً؟' }, expected: { en: 'Reflexive of Form III — mutual action between parties: تَقَاتَلَ (to fight each other), تَعَاوَنَ (to cooperate), تَكَاتَبَ (to write to each other)', tr: 'Form III\'ün dönüşlüsü — taraflar arasında karşılıklı eylem: تَقَاتَلَ (birbirleriyle savaşmak), تَعَاوَنَ (işbirliği yapmak), تَكَاتَبَ (birbirlerine yazmak)', ar: 'مطاوعة الوزن الثالث — فعل متبادل بين الطرفين: تَقَاتَلَ (تقاتلوا)، تَعَاوَنَ (تعاون)، تَكَاتَبَ (تراسلوا/كتبوا لبعضهم البعض)' } },
          { type: 'grammar', q: { en: 'What does Form VII (اِنْفَعَلَ) typically mean?', tr: 'Form VII (اِنْفَعَلَ) genellikle ne anlama gelir?', ar: 'ماذا يعني الوزن السابع (اِنْفَعَلَ) عادةً؟' }, expected: { en: 'Passive or reflexive of Form I: كَسَرَ (to break sth) → اِنْكَسَرَ (to break — intransitive/be broken); انقلب (to be overturned)', tr: 'Form I\'in pasifi veya dönüşlüsü: كَسَرَ (bir şeyi kırmak) → اِنْكَسَرَ (kırılmak — geçişsiz/kırılmış olmak); انقلب (tersine dönmek)', ar: 'مطاوعة أو لازم الوزن الأول: كَسَرَ (كسر شيئاً) → اِنْكَسَرَ (انكسر — فعل لازم/تكسر)؛ انقلب (انقلب)' } },
          { type: 'grammar', q: { en: 'What does Form VIII (اِفْتَعَلَ) typically mean?', tr: 'Form VIII (اِفْتَعَلَ) genellikle ne anlama gelir?', ar: 'ماذا يعني الوزن الثامن (اِفْتَعَلَ) عادةً؟' }, expected: { en: 'Reflexive with variety of meanings: جَمَعَ → اِجْتَمَعَ (to gather/assemble), كَسَبَ → اِكْتَسَبَ (to earn/acquire), قَرَبَ → اِقْتَرَبَ (to draw near)', tr: 'Çeşitli anlamlara sahip dönüşlü: جَمَعَ → اِجْتَمَعَ (toplamak/bir araya gelmek), كَسَبَ → اِكْتَسَبَ (kazanmak/edinmek), قَرَبَ → اِقْتَرَبَ (yaklaşmak)', ar: 'للمطاوعة بمعانٍ متنوعة: جَمَعَ → اِجْتَمَعَ (اجتمع/تجمّع)، كَسَبَ → اِكْتَسَبَ (اكتسب/نال)، قَرَبَ → اِقْتَرَبَ (اقترب)' } },
          { type: 'grammar', q: { en: 'What does Form X (اِسْتَفْعَلَ) typically mean?', tr: 'Form X (اِسْتَفْعَلَ) genellikle ne anlama gelir?', ar: 'ماذا يعني الوزن العاشر (اِسْتَفْعَلَ) عادةً؟' }, expected: { en: 'To seek, request, or consider: غَفَرَ → اِسْتَغْفَرَ (to seek forgiveness), خَرَجَ → اِسْتَخْرَجَ (to extract), عْمَلَ → اِسْتَعْمَلَ (to use/employ)', tr: 'İstemek, talep etmek veya düşünmek: غَفَرَ → اِسْتَغْفَرَ (bağışlanma dilemek), خَرَجَ → اِسْتَخْرَجَ (çıkarmak), عْمَلَ → اِسْتَعْمَلَ (kullanmak/işe almak)', ar: 'للطلب أو الطلب أو الاعتبار: غَفَرَ → اِسْتَغْفَرَ (طلب المغفرة)، خَرَجَ → اِسْتَخْرَجَ (استخرج)، عْمَلَ → اِسْتَعْمَلَ (استخدم/وظّف)' } },
          { type: 'translation', q: { en: 'Translate: اسْتَعِينُوا بِاللَّهِ وَاصْبِرُوا', tr: 'Çevirin: اسْتَعِينُوا بِاللَّهِ وَاصْبِرُوا', ar: 'ترجم: اسْتَعِينُوا بِاللَّهِ وَاصْبِرُوا' }, expected: { en: 'Seek help from Allah and be patient (Surah Al-A\'raf 7:128 â Ø§Ø³ÙØªÙØ¹ÙÙÙÙÙØ§ = Form X imperative plural of Ø¹ÙØ§ÙÙ)', tr: 'Allah\'tan yardım isteyin ve sabırlı olun (A\'raf Suresi 7:128 — اسْتَعِينُوا = عَانَ fiilinin X. kalıbı emir çoğuludur)', ar: 'اطلبوا العون من الله واصبروا (سورة الأعراف 7:128 — اسْتَعِينُوا = صيغة الأمر الجمع من الوزن العاشر للفعل عَانَ)' } },
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
    id: 'learn-deep',
    icon: '🎓',
    learnDeep: true,
    group: 'power',
    title: { en: 'Deep Learn', tr: 'Derinlemesine Öğren', ar: 'تعلّم بعمق' },
    desc: {
      en: 'Browse every grammar concept across all 42 lessons. Pick a level, lesson, and concept to get a guided explanation in your language plus worked examples in i\'rab style.',
      tr: '42 dersin tüm gramer konularını gez. Bir seviye, ders ve konu seç; seçtiğin dilde rehberli açıklama ve i\'rab tarzında çözümlü örnekler al.',
      ar: 'تصفّح كل المفاهيم النحوية في الدروس الـ ٤٢. اختر مستوى ودرساً ومفهوماً لتحصل على شرح موجَّه بلغتك وأمثلة محلولة بأسلوب الإعراب.'
    },
    pdfs: []
  },
  {
    id: 'irab',
    icon: '📖',
    irab: true,
    group: 'power',
    title: { en: 'Verse Analysis (I\'rab)', tr: 'Ayet İ\'rabı', ar: 'إعراب الآية' },
    desc: { en: 'Paste any Quranic verse to get a word-by-word grammatical analysis. Each grammar phenomenon links back to the relevant lesson in the 42-lesson curriculum.', tr: 'Kelime kelime gramer analizi için herhangi bir Kur\'an ayetini yapıştırın. Her gramer olgusu, 42 derslik müfredattaki ilgili derse bağlanır.', ar: 'الصق أي آية لتحليلها نحوياً كلمة بكلمة. كل ظاهرة نحوية مرتبطة بالدرس المعني من بين الـ ٤٢ درساً.' },
    pdfs: []
  },
  {
    id: 'content-mgr',
    icon: '🗂️',
    contentMgr: true,
    adminOnly: true,
    group: 'power',
    title: { en: 'Content Manager', tr: 'İçerik Yönetimi', ar: 'إدارة المحتوى' },
    desc: {
      en: 'Admin-only. Add per-lesson resources (PDFs, images, audio, links, notes) that students see in their unlocked lessons.',
      tr: 'Yalnızca yönetici. Her ders için ek kaynak (PDF, görsel, ses, bağlantı, not) ekle. Öğrenciler kilidi açık derslerde bunları görür.',
      ar: 'للمشرف فقط. أضف موارد لكل درس (PDF، صور، صوت، روابط، ملاحظات). يراها الطلاب في الدروس المفتوحة لهم.'
    },
    pdfs: []
  },
  {
    id: 'irab-compare',
    icon: '🔀',
    irabCompare: true,
    group: 'power',
    title: { en: 'I\'rab AI Compare', tr: 'İ\'rab Yapay Zekâ Karşılaştırma', ar: 'مقارنة الإعراب بالذكاء الاصطناعي' },
    desc: {
      en: 'Run the same verse through Gemini and Claude (and ChatGPT later) side-by-side. See where the models agree and where they differ — useful for cross-checking grammatical analysis.',
      tr: 'Aynı ayeti Gemini ve Claude (ileride ChatGPT de) ile yan yana analiz et. Modellerin nerede aynı, nerede farklı sonuç verdiğini gör — gramer analizini çapraz kontrol için kullanışlı.',
      ar: 'حلّل نفس الآية بمحركَي Gemini و Claude (و ChatGPT لاحقاً) جنباً إلى جنب. شاهد أين تتفق النماذج وأين تختلف — مفيد للتحقق المتقاطع للتحليل النحوي.'
    },
    pdfs: []
  },
  {
    id: 'irab-compare-grounded',
    icon: '🎓',
    irabCompare: true,
    irabCompareGrounded: true,
    group: 'power',
    title: { en: 'Curriculum-Limited I\'rab', tr: 'Müfredatla Sınırlı İ\'rab', ar: 'الإعراب ضمن المنهج' },
    desc: {
      en: 'I\'rab analysis powered by Gemini, locked to ONLY the 42-week curriculum via a context cache — no outside grammatical knowledge. Targeted and consistent with exactly what students are taught.',
      tr: 'Gemini ile İ\'rab analizi — bağlam önbelleği sayesinde YALNIZCA 42 haftalık müfredatla sınırlı, dışarıdan gramer bilgisi yok. Öğrencilere öğretilenle birebir tutarlı, hedefli sonuç.',
      ar: 'تحليل الإعراب بمحرك Gemini، محصور في منهج الـ ٤٢ أسبوعاً فقط عبر ذاكرة سياق مخزّنة — دون معرفة نحوية خارجية. نتائج مركّزة ومتوافقة تماماً مع ما يتعلمه الطلاب.'
    },
    pdfs: []
  },
  {
    id: 'self-check',
    icon: '✍️',
    selfCheck: true,
    group: 'power',
    title: { en: 'I\'rab Self Check', tr: 'İ\'rab Kendini Kontrol Et', ar: 'إعراب بالتدقيق الذاتي' },
    desc: {
      en: 'Practice mode: pick a verse, click Self Fill to get blank word boxes, write your own meaning / role / notes for each word, then click Analyze — the AI compares your answers to the correct analysis and tells you exactly what to fix and what you nailed.',
      tr: 'Pratik modu: bir ayet seç, Kendi Doldur\'a tıklayarak boş kelime kutuları al, her kelime için anlam / rol / notu kendin yaz, sonra Analiz et — yapay zeka cevaplarını doğru analizle karşılaştırır ve neyi düzeltmen gerektiğini, neyi doğru yaptığını söyler.',
      ar: 'وضع التدريب: اختر آية، اضغط "املأ بنفسك" للحصول على صناديق فارغة لكل كلمة، اكتب المعنى / الموقع الإعرابي / الملاحظات بنفسك، ثم اضغط حلّل — سيقارن الذكاء الاصطناعي إجاباتك بالتحليل الصحيح ويبيّن لك بالضبط ما يحتاج تعديلاً وما أصبتَ فيه.'
    },
    pdfs: []
  },
  {
    id: 'vocab-quiz',
    icon: '🧠',
    quiz: true,
    group: 'power',
    title: { en: 'Vocabulary Quiz', tr: 'Kelime Sınavı', ar: 'اختبار المفردات' },
    desc: { en: 'Multiple-choice quiz drawn from the entire vocabulary pool extracted from all 98 vocabulary PDFs.', tr: '98 kelime PDF\'sinden çıkarılan tüm kelime havuzundan çoktan seçmeli sınav.', ar: 'اختبار اختيار من متعدد من مجمل المفردات المستخرجة من جميع ملفات الـ ٩٨ PDF.' },
    pdfs: []
  },
  {
    id: 'flashcards',
    icon: '🃏',
    flashcards: true,
    group: 'power',
    title: { en: 'Flashcards', tr: 'Kelime Kartları', ar: 'بطاقات المفردات' },
    desc: { en: 'Flip-card drill on the same vocabulary pool as the quiz: see the Arabic word, then tap to reveal its meaning.', tr: 'Kelime Sınavı ile aynı kelime havuzundan kart çalışması: Arapça kelimeyi gör, dokunarak anlamını ortaya çıkar.', ar: 'بطاقات تعلّم من نفس مجموعة مفردات الاختبار: شاهد الكلمة العربية ثم انقر لكشف معناها.' },
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
