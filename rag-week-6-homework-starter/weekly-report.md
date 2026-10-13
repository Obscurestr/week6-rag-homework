# Nedeljni izveštaj — NACRT

## 1. Osnovne informacije

| Polje | Odgovor |
| --- | --- |
| Ime i prezime | Sara Trnjakov |
| Adresa e-pošte | saratrnjakov6@gmail.com |
| Discord korisničko ime | saratrnjakov |
| Nedelja | Week 6 — RAG homework |
| Par / tim | Tim Quattro: Sara je driver/developer; Goran je observer/reviewer, uradio je naknadnu proveru rada i biće demo lead jer Sara neće prisustvovati predavanju. |
| Moj konkretan doprinos / uloga | Bila sam driver. Radila sam na svih pet ishoda: chunking poređenju, top-k retrieval-u, citatima, refusal ponašanju i dokumentovanju dokaza. |
| Datum predaje | 2026-10-12 |
| Reference na rad i dokaze | `evidence.md` sa poređenjem chunking konfiguracija, rangiranim rezultatima, podržanim primerom sa citatima i nepodržanim primerom sa refusal izlazom; ručno pokrenut test paket sa rezultatom `12 passed`. |

## 2. Moj status

**Status:** Završeno

Implementirala sam svih pet traženih ishoda za Week 6 RAG zadatak. Ručno sam pokrenula testove i svih 12 testova je prošlo.

## 3. Rad ove nedelje

Ove nedelje sam radila na RAG homework zadatku kao driver u timu Quattro, u paru sa Goranom. Moj doprinos je obuhvatio svih pet traženih ishoda.

Za prvi ishod radila sam na chunking parametrima u `src/chunking.py` i uporedila kvalitet retrieval-a za isti upit sa dve konfiguracije. Poređenje pokazuje kako veličina chunk-a i overlap menjaju broj chunk-ova, rangiranje i količinu relevantnog konteksta u najboljem rezultatu.

Za drugi ishod radila sam na top-k retrieval-u u `src/retrieval.py`. Rezultati se vraćaju prema opadajućem relevance score-u, a redosled je prikazan u `evidence.md` za različite vrednosti parametra `top_k`. Za treći ishod radila sam na `src/rag.py`, tako da podržani odgovor sadrži eksplicitne citate sa chunk ID-jevima. Citirani ID-jevi odgovaraju chunk-ovima prikazanim u retrieval rezultatu.

Za četvrti ishod obuhvatila sam refusal ponašanje. Kada pitanje nema dovoljno podrške u lokalnom korpusu, sistem vraća jasnu poruku da nema dovoljno grounded dokaza, bez izmišljanja odgovora i bez citata. Za peti ishod pripremila sam `evidence.md`, u kojem se nalaze chunking poređenje, top-k izlazi, podržan primer sa citatom i nepodržan primer sa refusal izlazom.

Koristila sam Codex, OpenAI AI asistenta, za pomoć pri implementaciji. Rezultat sam proverila tako što sam ručno pokrenula testove; svih 12 testova je prošlo. Naučila sam koncept RAG-a i kako se praktično implementiraju chunking, retrieval, odgovor sa citatima i odbijanje pitanja kada nema dovoljno dokaza. Pomoć tutora mi trenutno nije potrebna.

## 4. Sledeći korak

Trenutno ne planiram dodatni korak pre druge sesije.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
