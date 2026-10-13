# Week 6 RAG handoff review

Reviewed on 2026-10-13 against `Week 6 RAG Homework Starter.pdf` and `docs/homework-checklist.md`.

## Roles and history

- Sara was the driver/developer for the original homework work. Goran was the observer/reviewer and is the designated demo lead because Sara will not attend the lecture.
- The repository's original `9708deb` commit was a single upload authored by Sara. It does not provide a step-by-step record of each person's work.
- Goran's later handoff check identified and addressed a chunking data-loss edge case and an unsupported-answer case with Codex assistance. The changes and current verification should be described as later review work, separate from Sara's original account.

## Assignment check

| Outcome | Handoff evidence |
| --- | --- |
| Chunking impact | Two configurations, complete CLI output, and a comparison for the same question in `evidence.md`. |
| Top-k retrieval | Top-2 and top-3 results are shown in descending score order. |
| Citations | The supported answer uses a sentence present in its cited retrieved chunk. |
| Refusal | The World Cup query retrieves nothing and refuses; an overlapping query asking for an absent year also refuses. |
| Evidence pair | Full supported and unsupported CLI output, source text, commands, and a current test result are recorded. |

During Goran's handoff review, Codex ran Python 3.12.10 on Windows with a fresh local environment. `python -m pytest -q` passed all 17 tests on 2026-10-13. Codex reran the CLI outputs in `evidence.md` after the review fixes. The answer builder is a small lexical, extractive demonstration: it requires one retrieved sentence to contain every meaningful query term. It can refuse valid paraphrases, and word matching alone cannot guarantee factual support for arbitrary questions.

## Weekly report alignment

- Sara's `weekly-report.md` remains a draft in her voice. Its `12 passed` statement records her earlier reported run; Codex observed `17 passed` during the later review after adding regression tests. Git history alone does not verify the earlier run or individual authorship.
- The draft now records Sara as driver/developer and Goran as observer/reviewer and demo lead. Sara should confirm her own personal account before the draft is finalized.
- Goran's report will be prepared later from his own account. It should distinguish observation and review of Sara's original work from his subsequent handoff check and the changes made with Codex, and use the current evidence and test result when describing this review.
