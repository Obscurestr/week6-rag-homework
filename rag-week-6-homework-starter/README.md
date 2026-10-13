# Week 6 RAG Homework Starter

This starter app helps students practice Week 6 concepts from the RAG lecture:

- corpus preparation
- chunking with overlap
- simple retrieval
- answer generation with citations
- refusal behavior when evidence is missing

## Learning goals

By the end of this homework, a student pair should be able to:

1. Explain how chunking strategy affects retrieval quality.
2. Implement a retrieval pipeline that returns top-k relevant chunks.
3. Return answers with explicit citations to source chunks.
4. Refuse unsupported questions instead of hallucinating.
5. Show evidence for one supported and one unsupported question.

## Project structure

```text
rag-week-6-homework-starter/
  .codex/skills/student-weekly-report/
    student-weekly-report/
      INSTALL.md
      SKILL.md
      agents/
      assets/
      references/
  src/
    corpus.py
    chunking.py
    retrieval.py
    rag.py
    cli.py
  tests/
    test_chunking.py
    test_corpus.py
    test_retrieval.py
    test_rag.py
  docs/
    homework-checklist.md
    handoff-review.md
  scripts/
    run_tests.sh
  evidence.md
  weekly-report-SaraTrnjakov.md
  weekly-report-GoranSuvacarev.md
  Week 6 RAG Homework Starter.pdf
  requirements.txt
```

## Setup

Use Python 3.12. From this directory on macOS or Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create the environment locally; it is not part of the repository.

## Run tests

```bash
.venv/bin/python -m pytest -q
```

On Windows PowerShell, run `.\.venv\Scripts\python.exe -m pytest -q`.

## Run demo CLI

Use the environment's Python from the project directory:

```bash
.venv/bin/python -m src.cli --question "What is retrieval augmented generation?"
.venv/bin/python -m src.cli --question "Who won the world cup in 1958?"
.venv/bin/python -m src.cli --corpus-profile training-rag --question "Why do citations improve transparency and trust?"
```

On Windows PowerShell, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`.

## Corpus profiles

- `default`: compact baseline corpus for Week 6 fundamentals.
- `training-rag`: profile mirroring examples with focus on citations, references, and LLM-as-a-judge framing.

The answer builder selects a cited sentence only when that sentence contains every meaningful query term. It refuses questions without such a sentence. This deliberately conservative lexical rule can refuse valid paraphrases, and matching words alone cannot prove that a sentence fully answers every possible question.

## Homework tasks for students

1. **Outcome 1 (chunking impact):** tune chunking parameters in `src/chunking.py` and compare retrieval quality for the same query.
2. **Outcome 2 (top-k retrieval):** verify `src/retrieval.py` returns correctly ordered top-k relevant chunks.
3. **Outcome 3 (citations):** ensure `src/rag.py` returns grounded answers with explicit citations to chunk IDs.
4. **Outcome 4 (refusal):** ensure unsupported questions trigger refusal instead of hallucinated answers.
5. **Outcome 5 (evidence):** document one supported and one unsupported query with full retrieval and output evidence.

## Recommended evidence template (`evidence.md`)

Use this exact structure for easy review:

1. **Outcome 1: Chunking impact**
  - Config A:
  - Config B:
  - Retrieval difference summary:
2. **Outcome 2: Top-k retrieval**
  - Query:
  - Top-k output:
  - Why ranking is correct:
3. **Outcome 3: Citation quality**
  - Supported query:
  - Answer with citations:
  - Retrieved chunk IDs:
4. **Outcome 4: Refusal behavior**
  - Unsupported query:
  - Retrieved context:
  - Refusal output:
5. **Outcome 5: Final evidence pair**
  - Supported case command + output
  - Unsupported case command + output

Use `docs/homework-checklist.md` as submission guidance.
