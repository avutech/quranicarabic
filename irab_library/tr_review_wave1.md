# Türkçe okuma — 1. dalga gözden geçirme listesi (2026-10-03)

**Kapsam:** Fâtiha (6 kitabın tamamı) + Amme cüzü (Ferrâ, Ahfeş, Zeccâc, Nahhâs İ'râb).
1142 girdi, hepsi çevrildi, hepsi `reviewed: false`. Her çeviri kaynak girdisini ve
Arapça metnin sha1 özetini taşır (bkz. `tr_parts/<kitap>/sNNN.json` → `src`).

Kalite kontrolü: tüm girdilerde otomatik kapsam/uzunluk/ayet-parantezi/terim
kontrolleri; 20 girdi Arapça-Türkçe karşılaştırmalı okundu. Özet ve terim
tercihleri için: `glossary_tr.md`.

## Hocanın karar vermesi gerekenler

1. **Parantez içi eklemeler.** Kısa Nahhâs ve Ferrâ girdilerinin başına, i'rabı
   yapılan kelime parantezle eklendi; ör. «(يَزَّكَّى):». Öğrenciye yardımcı oluyor,
   ama "ekleme yapma" kuralının dışında. Kalsın mı?
2. **İşaretsiz düzeltmeler**
   - akhfash 81:6: سُجِرِّتْ → سُجِّرَتْ
   - akhfash 90:11: يَقَتْحِمْ → يَقْتَحِمْ
   - nahhas-irab 85:15: «الجواب» → «الجوار» olarak okundu
   - semin-durr 1:6: [الأعراف: 56] → 156
3. **Kıraatleri ayırt etmek için eklenen harekeler.** Kontrol edilenler doğru.
   - nahhas 1:2, 84:19, 86:4, 88:11, 89:8, 89:25, 90:12-13, 97, 104:9
   - farraa 89:25
4. **Kaynak metinde kesik veya bozuk yerler**
   - Not düşüldü: nahhas-irab 100:9, 113:5, 92:15-16, 108:2; zajjaj 82:19, 91:11; farraa 90:11
   - Not düşülmedi: farraa 78:1-4, nahhas-irab 85:19-20
5. **Şüpheli okumalar**
   - nahhas-irab 90:12-13: «لا يجوز» büyük ihtimalle «يجوز» olmalı (metinde notu var)
   - zajjaj 89:3: ilk «الوتر» için «الشفع» notu eklendi
   - nahhas-irab 83:3: Ebû Zeyd beytindeki mantar adları
   - farraa 91:12: Ebü'l-Kamkâm beytinin anlamı
6. **Not etiketleri farklı:** «[metinde böyledir…]», «[Metin burada eksik…]»,
   «[Mütercim notu: …]». İstenirse tek biçime getirilebilir.

## Onaylama

Bir girdi onaylandığında, ilgili `tr_parts/<kitap>/sNNN.json` dosyasında
`"reviewed": true` yapılır ve `venv/bin/python build_irab_library.py` çalıştırılır.
Sitede "hoca tarafından gözden geçirildi" olarak görünür.
