# Week 6 RAG Evidence

1. Outcome 1: Chunking impact

- Config A: `python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 140 --overlap 30 --top-k 3`

  ```text
  chunk_size=140, overlap=30, chunks=6
  1. [doc-2-chunk-0] score=0.806 coverage=100% | Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source
  2. [doc-1-chunk-0] score=0.157 coverage=17% | Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than
  ```

- Config B: `python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 3`

  ```text
  chunk_size=80, overlap=20, chunks=9
  1. [doc-2-chunk-1] score=0.900 coverage=100% | chunk size and overlap improve retrieval quality. Metadata helps filtering and
  2. [doc-2-chunk-0] score=0.440 coverage=50% | Chunking splits documents into smaller parts. Good chunk size and overlap
  3. [doc-1-chunk-0] score=0.202 coverage=17% | Retrieval augmented generation combines retrieval with text generation. The
  ```

- Retrieval difference summary: Config B creates three more chunks and promotes a tighter chunk containing every meaningful query term from a score of 0.806 to 0.900. The 20-character overlap retains the preceding phrase in `doc-2-chunk-0`, so nearby context is still retrievable.

2. Outcome 2: Top-k retrieval

- Query: `How do chunk size and overlap improve retrieval quality?`
- Top-k output: `python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 2`

  ```text
  1. [doc-2-chunk-1] score=0.900 coverage=100% | chunk size and overlap improve retrieval quality. Metadata helps filtering and
  2. [doc-2-chunk-0] score=0.440 coverage=50% | Chunking splits documents into smaller parts. Good chunk size and overlap
  ```

  With `--top-k 3`, the next result is `[doc-1-chunk-0] score=0.202 coverage=17%`, confirming that the result list is ordered from highest to lowest score.

- Why ranking is correct: the score weights meaningful-query-term coverage (70%) and term density in the chunk (30%). The first chunk covers all six query terms; the second covers three; the third only one. Equal scores are ordered by chunk ID for reproducibility.

3. Outcome 3: Citation quality

- Supported query: `Why do citations improve transparency and trust?`
- Answer with citations: `python -m src.cli --corpus-profile training-rag --question "Why do citations improve transparency and trust?" --chunk-size 140 --overlap 30 --top-k 2`

  ```text
  Grounded response based on retrieved context:
  [tr-doc-1-chunk-1] the answer. Citations improve transparency and trust because users can verify evidence.

  Citations: [tr-doc-1-chunk-1]
  Refused: False
  ```

- Retrieved chunk IDs:

  ```text
  1. [tr-doc-1-chunk-1] score=0.820 coverage=100%
  2. [tr-doc-1-chunk-0] score=0.419 coverage=50%
  ```

  The answer cites only `tr-doc-1-chunk-1`, because it meets the grounding threshold. The lower-ranked partial lexical match is visible in retrieval evidence but is not presented as support.

4. Outcome 4: Refusal behavior

- Unsupported query: `Who won the World Cup in 1958?`
- Retrieved context: `None`
- Refusal output: `python -m src.cli --question "Who won the World Cup in 1958?" --chunk-size 100 --overlap 20 --top-k 2`

  ```text
  Answer:
  I do not have enough grounded evidence in the provided corpus to answer that question.

  Refused: True
  Citations: None
  ```

  No meaningful question terms occur in the corpus, so retrieval returns no chunks and the system refuses rather than inventing an answer.

5. Outcome 5: Final evidence pair

- Supported case command + output

  ```text
  python -m src.cli --corpus-profile training-rag --question "Why do citations improve transparency and trust?" --chunk-size 140 --overlap 30 --top-k 2
  -> Refused: False
  -> Citations: tr-doc-1-chunk-1
  -> Citations improve transparency and trust because users can verify evidence.
  ```

- Unsupported case command + output

  ```text
  python -m src.cli --question "Who won the World Cup in 1958?" --chunk-size 100 --overlap 20 --top-k 2
  -> Retrieved chunks: None
  -> Refused: True
  -> Citations: None
  -> I do not have enough grounded evidence in the provided corpus to answer that question.
  ```
