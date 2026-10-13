# Nedeljni izveštaj

## 1. Osnovne informacije

| Polje | Odgovor |
| --- | --- |
| Ime i prezime | Goran Suvačarev |
| Adresa e-pošte | goran.suvacarev@gmail.com |
| Discord korisničko ime | thescriptum |
| Nedelja | Week 6 — RAG homework |
| Par / tim | Tim Quattro: Sara Trnjakov (driver/developer) i Goran Suvačarev (observer/reviewer i demo lead) |
| Moj konkretan doprinos / uloga | Ručno sam pregledao kod i testove i uz Codex uradio naknadnu proveru i manje ispravke pre predaje rada. |
| Datum predaje | 2026-10-13 |
| Reference na rad i dokaze | `evidence.md`, `docs/handoff-review.md`, naknadne izmene `19cb22e` i `1a5b16c`; Codexova provera od 2026-10-13: `17 passed`. |

## 2. Moj status

**Status:** Završeno

Naknadna provera i manje ispravke za Week 6 RAG zadatak su završene. Dokazi za tražene ishode i rezultat aktuelnih testova zabeleženi su u projektu. Sledeći korak mi je priprema za izlaganje.

## 3. Rad ove nedelje

Na Week 6 RAG zadatku Sara je bila driver/developer, a ja observer/reviewer. Ona je radila na prvobitnoj implementaciji, dok sam ja ručno pregledao kod i testove i zatim uradio dodatni checkup pred primopredaju. Proveravao sam rad u odnosu na tražene ishode: poređenje podešavanja za chunking, rangiranje top-k rezultata, odgovor sa citatom, odbijanje pitanja bez dovoljno dokaza i prikaz tih primera u `evidence.md`.

U naknadnoj proveri uočena su dva konkretna problema: jedan rubni slučaj u chunking-u mogao je da izgubi deo teksta, a upit za godinu koja ne postoji u korpusu mogao je da dobije odgovor iako za njega nije bilo oslonca u dokazima. Uz Codex sam napravio manje ispravke i dopunio testove i evidenciju.

Codex je nakon ispravki pokrenuo testove i CLI primere. U `evidence.md` zabeležen je rezultat te provere, `17 passed`, kao i izlaz za podržane i nepodržane upite. Sistem i dalje ima ograničenje: leksičko poklapanje može da odbije ispravno preformulisano pitanje, a samo poklapanje reči ne dokazuje uvek da je odgovor činjenično podržan.

Ranije se nisam susretao sa RAG sistemima, a kroz ovaj zadatak naučio sam kako funkcionišu. Codex mi je pomogao pri naknadnim izmenama i proveri; rezultate sam pregledao kroz kod, testove i zabeležene primere. Pomoć tutora mi trenutno nije potrebna.

## 4. Sledeći korak

Pripremiću se za izlaganje u sredu, kada kao demo lead treba da predstavim projekat.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
