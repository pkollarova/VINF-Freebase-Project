# VINF-Freebase-Project


####O projekte####

Našou úlohou bolo spracovať dáta z Freebase tak, aby sme vedeli vyhľadávať vzťah Artist + Track + Award. Sústredili sme sa čisto na hudobnú doménu. Motiváciou k výberu tohto zadania bol samozrejme pozitívny vzťah k hudbe.

Nás vyhľadávač je možné využiť na čiastkové vyhľadávanie informácií na základe mien artistov, názvov trackov alebo názvov ocenení. Okrem informácií o menách a názvoch poskytne aj informáciu o artistovi, jeho narodení, dĺžke tracku a roku udelenia ocenenia. Ak sa nám nejaký údaj nepodarilo získať, štandardne sa zobrazí hodnota "None".


####Postup pri vypracovávaní####

Na začiatku sme samozrejme pracovali lokálne na našom notebooku a celé spracovanie Freebase súboru, indexovanie a vyhľadávanie sa odohrávalo v 1 dlhom a jednoduchom Python skripte. V tejto fáze sme pracovali samozrejme iba s malými ukážkovými Freebase súbormi a všetky dáta sme si udržiavali iba v pamäti.

Následne sme sa snažili začať pracovať s väčšími súbormi a uvedomili sme si, že nemôžeme všetko držať v pamäti, takže sme začali pracovať so súbormi a všetko si do nich ukladať.

Nakoniec sme svoj zdrojový kód museli preklopiť do clustera. Táto časť nás dosť potrápila najmä kvôli do dnešného dňa nepochopeného problému s Hadoop containermi, takže sme celé "joby" spracovávali len pomocou pipes. Spracovávanie dát sme celkovo rozdelili do 8 jobov, pričom niektoré joby používajú len mapper alebo reducer. Následne sme dáta pomocou PyLucene indexovali a napísali si vyhľadávač, ktorý s týmto indexom pracuje. 

Celému projektu sme sa venovali pravidelne, preto sme mali čas na prácu vždy pekne rozvrhnutý a nestalo sa, že by sme niečo na základe pripomienok z konzultácií nestíhali zapracovať.


####Overenie výsledkov####

Výsledky nášho vyhľadávania sme si na konkrétnych príkladoch overovali pomocou Freebase Easy a aj Googlenia informácií, ktoré nám boli vyhľadané.

__Príklad artistu - Ken Yokoyama__

Výsledky vyhľadávania nám pre všetko korektne sedeli s Freebase Easy aj googlením. Čo sme dokázali dohľadať cez Freebase Easy sme cez to dohľadali a zvyšok sme overili manuálne prostredníctvo Google.

__Príklad tracku - Falling__

Výsledky vyhľadávania boli celkom rozsiahle, nakoľko skladby s týmto názvom boli aj remixované, čiže nám našlo aj remixy. Vybrali sme si skladbu Falling od artistu Ben Westbeech a výsledky sme opäť dokázali úspešne overiť, okrem roku narodenia, ktorý sme my nenašli avšak Freebase Easy vykazuje rok 1981.

__Príklad awardu - a*__

V tomto prípade sme nechalli vyhľadávanie voľnejšie a vyhľadali sme informácie okomkoľvek, kto získal nejaké ocenenie začínajúce na písmeno "a". Výsledkov vyhľadávania bolo samozrejme mnoho a tak sme mali bohatý výber na overenie. Vybrali sme si jeden výsledok vyhľadávania a porovnali ho. V tomto prípade nám opäť sedeli výsledky vyhľadávania až na zopár "None" údajov, ktoré sa nám nepodarilo identifikovať.

Jednotlivé výsledky nášho vyhľadávania sme zároveň aj hodnotili podľa relevantnosti. Naše vyhľadávanie sme mali ohraničené nízkou bodovou hranicou a tým pádom boli všetky naše výsledky vyhľadávania pomerne relevantné. Samozrejme, pri všeobecných vyhľadávaniach (napríklad iba podľa krstného mena) sme stále dostali vysoký počet výsledkov. Pri konkrétnejších dopytoch sa nám výsledky samozrejme rapídne zúžili a mali sme len malé množstvo FalsePositive prípadov.


####Inštalácia####

Inštalácia je veľmi jednoduchá, nevyžaduje inštaláciu žiadnych krkolomných Python knižníc ani nič podobného. Stačí rozbaliť všetky zdrojové súbory do nejakého priečinka. Je však potrebné dokázať spustiť Hadoop joby na clusteri, pretože Freebase dump, s ktorým pracujeme má 250GB.


####Spustenie a použitie####

Spracovanie súborov do podoby pre prácu s indexom je nasledovný:
1.  skopírovať všetky súbory do Hadoop fs
2.  spustiť hadoop fs -cat freebase-data | python3 mapper.py | sort -k1,1 | python3 reducer.py > job_1
3.  skopírovať súbor job_1 do Hadoop fs
4.  hadoop fs -cat freebase-data | python3 mapper_2.py | sort -k1,1 | python3 reducer_2.py > job_2
5.  skopírovať súbor job_2 do Hadoop fs
6.  hadoop fs -cat freebase-data | python3 mapper_3.py | sort -k1,1 | python3 reducer_3.py > job_3
7.  skopírovať súbor job_3 do Hadoop fs
8.  hadoop fs -cat job_1 | python3 mapper_4.py | sort -k1,1 > job_4
9.  skopírovať súbor job_4 do Hadoop fs
10. hadoop fs -cat job_2 | python3 mapper_5.py | sort -k1,1 | python3 reducer_5.py > job_5
11. skopírovať súbor job_5 do Hadoop fs
12. hadoop fs -cat job_3 | python3 mapper_6.py | sort -k1,1 | python3 reducer_6.py > job_6
13. skopírovať súbor job_6 do Hadoop fs
14. hadoop fs -cat job_4 job_5 job_6 | python3 mapper_7.py | sort -k1,1 | python3 reducer_7.py > job_7
15. skopírovať súbor job_7 do Hadoop fs
16. hadoop fs -cat job_7 | python3 reducer_8.py > final_jobs_output
17. skopírovať súbor final_jobs_output do Hadoop fs

Indexovanie:
1.  spustiť python3 indexer.py v priečinku so súbrom "final_jobs_output"
2.  vytvorí sa "index" v priečinku, kde bol indexer spustený

Vyhľadávanie:
1.  spustiť python3 searcher.py "query" v priečinku s indexom
2.  príklad python3 searcher.py "artist_name:ken"
3.  zobrazia sa výsledky vyhľadávania

Vyhľadávať je možné prostredníctvom fieldov "artist_name", "track_names" a "award_names". Okrem toho disponuje aj fieldami "artist_description", "artist_bday", "track_datas" a "award_datas" (cez tie sa však štandardne nevyhľadáva).


####Záver####

Myslíme si, že naše vypracovanie projektu celkom pekne spracováva Freebase dáta napriek rozdeleniu do viacerých jobov. S výsledkami vyhľadávania sme pomerne spokojní, i ked nás mrzí, že obsahuje niektoré "None" hodnoty, či už preto lebo sa v dátach nenachádzali alebo sme ich nejakou chybou nezaregistrovali a nepozbierali. Myslíme si ale, že je možné naše riešenie využiť na také rýchle a čiastkové vyhľadávanie. Ak by sa malo naše riešenie v budúcnosti využívať, bolo by potrebné v určitých intervaloch indexovať nové a nové dáta a upraviť indexer tak, aby pracoval otvorením a dopĺňaním dát do indexu, pretože momentálne pracuje vždy vytvorením úplne nových dát.
