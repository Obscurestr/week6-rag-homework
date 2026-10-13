from dataclasses import dataclass
import re

from .chunking import Chunk
from .retrieval import lexical_score, query_coverage, retrieve_top_k


REFUSAL_MESSAGE = "I do not have enough grounded evidence in the provided corpus to answer that question."
MIN_GROUNDING_SCORE = 0.25
MIN_QUERY_COVERAGE = 1.0


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]
    refused: bool


def build_grounded_answer(question: str, chunks: list[Chunk], top_k: int = 2) -> RagAnswer:
    results = retrieve_top_k(question, chunks, k=top_k)
    # Check a sentence rather than an entire chunk. Terms scattered across
    # unrelated sentences cannot support a single extractive answer.
    candidates: list[tuple[float, int, str, str]] = []
    for rank, item in enumerate(results):
        for sentence in re.split(r"(?<=[.!?])\s+", item.chunk.text):
            sentence = sentence.strip()
            if not sentence:
                continue
            coverage = query_coverage(question, sentence)
            score = lexical_score(question, sentence)
            if coverage >= MIN_QUERY_COVERAGE and score >= MIN_GROUNDING_SCORE:
                candidates.append((score, rank, item.chunk.chunk_id, sentence))

    if not candidates:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    _, _, citation, sentence = min(candidates, key=lambda item: (-item[0], item[1], item[2]))
    answer = f"{sentence} [{citation}]\n\nCitations: [{citation}]"
    return RagAnswer(answer=answer, citations=[citation], refused=False)
