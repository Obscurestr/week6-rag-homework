# Week 6 RAG Evidence

These commands were run from the project directory on Windows PowerShell with Python 3.12.10. On macOS or Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

1. Outcome 1: Chunking impact

- Config A: `.\.venv\Scripts\python.exe -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 140 --overlap 30 --top-k 3`

  ```text
  Question:
  How do chunk size and overlap improve retrieval quality?

  Chunking:
  chunk_size=140, overlap=30, chunks=6

  Retrieved chunks:
  1. [doc-2-chunk-0] score=0.806 coverage=100% | Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source
  2. [doc-1-chunk-0] score=0.157 coverage=17% | Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than

  Answer:
  Good chunk size and overlap improve retrieval quality. [doc-2-chunk-0]

  Citations: [doc-2-chunk-0]

  Corpus profile: default

  Refused: False
  Citations: doc-2-chunk-0
  ```

- Config B: `.\.venv\Scripts\python.exe -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 3`

  ```text
  Question:
  How do chunk size and overlap improve retrieval quality?

  Chunking:
  chunk_size=80, overlap=20, chunks=9

  Retrieved chunks:
  1. [doc-2-chunk-1] score=0.900 coverage=100% | chunk size and overlap improve retrieval quality. Metadata helps filtering and
  2. [doc-2-chunk-0] score=0.440 coverage=50% | Chunking splits documents into smaller parts. Good chunk size and overlap
  3. [doc-1-chunk-0] score=0.202 coverage=17% | Retrieval augmented generation combines retrieval with text generation. The

  Answer:
  chunk size and overlap improve retrieval quality. [doc-2-chunk-1]

  Citations: [doc-2-chunk-1]

  Corpus profile: default

  Refused: False
  Citations: doc-2-chunk-1
  ```

- Retrieval difference summary: Config B creates three more chunks. Its highest-ranked chunk contains all six meaningful query terms in a shorter passage, while the larger Config A chunk includes more surrounding text. The score rises from 0.806 to 0.900 because the lexical scorer rewards term density. This demonstrates a more focused retrieved passage for this question; the score alone is not an independent quality measure. The overlap keeps nearby context retrievable in `doc-2-chunk-0`.

2. Outcome 2: Top-k retrieval

- Query: `How do chunk size and overlap improve retrieval quality?`
- Top-k output: `.\.venv\Scripts\python.exe -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 2`

  ```text
  Question:
  How do chunk size and overlap improve retrieval quality?

  Chunking:
  chunk_size=80, overlap=20, chunks=9

  Retrieved chunks:
  1. [doc-2-chunk-1] score=0.900 coverage=100% | chunk size and overlap improve retrieval quality. Metadata helps filtering and
  2. [doc-2-chunk-0] score=0.440 coverage=50% | Chunking splits documents into smaller parts. Good chunk size and overlap

  Answer:
  chunk size and overlap improve retrieval quality. [doc-2-chunk-1]

  Citations: [doc-2-chunk-1]

  Corpus profile: default

  Refused: False
  Citations: doc-2-chunk-1
  ```

  The Config B command above shows `--top-k 3`: its third result is `[doc-1-chunk-0] score=0.202 coverage=17%`. The results are ordered 0.900, 0.440, 0.202. Retrieval returns up to `k` positive matches, so Config A displays only two results despite `--top-k 3`.

- Why ranking is correct: the score weights distinct meaningful-query-term coverage (70%) and term density in the chunk (30%). The first Config B chunk covers all six terms; the second covers three; the third covers one. Equal scores are ordered by chunk ID.

3. Outcome 3: Citation quality

- Supported query: `Why do citations improve transparency and trust?`
- Answer with citations: `.\.venv\Scripts\python.exe -m src.cli --corpus-profile training-rag --question "Why do citations improve transparency and trust?" --chunk-size 140 --overlap 30 --top-k 2`

  ```text
  Question:
  Why do citations improve transparency and trust?

  Chunking:
  chunk_size=140, overlap=30, chunks=7

  Retrieved chunks:
  1. [tr-doc-1-chunk-1] score=0.820 coverage=100% | the answer. Citations improve transparency and trust because users can verify evidence.
  2. [tr-doc-1-chunk-0] score=0.419 coverage=50% | RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve

  Answer:
  Citations improve transparency and trust because users can verify evidence. [tr-doc-1-chunk-1]

  Citations: [tr-doc-1-chunk-1]

  Corpus profile: training-rag

  Refused: False
  Citations: tr-doc-1-chunk-1
  ```

- Retrieved chunk IDs: `tr-doc-1-chunk-1` and `tr-doc-1-chunk-0`, shown with full text above. The cited sentence appears in `tr-doc-1-chunk-1`. The lower-ranked chunk lacks a complete supporting sentence, so it is not cited.

4. Outcome 4: Refusal behavior

- Unsupported query: `Who won the World Cup in 1958?`
- Retrieved context: `None`
- Refusal output: `.\.venv\Scripts\python.exe -m src.cli --question "Who won the World Cup in 1958?" --chunk-size 100 --overlap 20 --top-k 2`

  ```text
  Question:
  Who won the World Cup in 1958?

  Chunking:
  chunk_size=100, overlap=20, chunks=6

  Retrieved chunks:
  None

  Answer:
  I do not have enough grounded evidence in the provided corpus to answer that question.

  Corpus profile: default

  Refused: True
  Citations: None
  ```

  No meaningful question terms occur in the corpus, so retrieval returns no chunks and the system refuses rather than inventing an answer.

5. Outcome 5: Final evidence pair

- Supported case command + output (complete retrieval and output appear in Outcome 3)

  ```text
  .\.venv\Scripts\python.exe -m src.cli --corpus-profile training-rag --question "Why do citations improve transparency and trust?" --chunk-size 140 --overlap 30 --top-k 2
  -> Retrieved chunks: tr-doc-1-chunk-1, tr-doc-1-chunk-0
  -> Refused: False
  -> Citations: tr-doc-1-chunk-1
  -> Citations improve transparency and trust because users can verify evidence. [tr-doc-1-chunk-1]
  ```

- Unsupported case command + output (complete retrieval and output appear in Outcome 4)

  ```text
  .\.venv\Scripts\python.exe -m src.cli --question "Who won the World Cup in 1958?" --chunk-size 100 --overlap 20 --top-k 2
  -> Retrieved chunks: None
  -> Refused: True
  -> Citations: None
  -> I do not have enough grounded evidence in the provided corpus to answer that question.
  ```

## Validation and limits

On 2026-10-13, `.\.venv\Scripts\python.exe -m pytest -q` returned:

```text
.................                                                        [100%]
17 passed in 0.04s
```

Additional unsupported-question check: `.\.venv\Scripts\python.exe -m src.cli --corpus-profile training-rag --question "What year do citations improve transparency and trust?" --chunk-size 140 --overlap 30 --top-k 2`

```text
Question:
What year do citations improve transparency and trust?

Chunking:
chunk_size=140, overlap=30, chunks=7

Retrieved chunks:
1. [tr-doc-1-chunk-1] score=0.680 coverage=80% | the answer. Citations improve transparency and trust because users can verify evidence.
2. [tr-doc-1-chunk-0] score=0.349 coverage=40% | RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: training-rag

Refused: True
Citations: None
```

Retrieval is lexical and the answer is extractive. Requiring all meaningful question terms in one sentence reduces unsupported answers but can refuse valid paraphrases. Matching terms is not a general proof of factual support.
