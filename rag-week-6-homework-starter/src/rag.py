from dataclasses import dataclass

from .chunking import Chunk
from .retrieval import retrieve_top_k


REFUSAL_MESSAGE = "I do not have enough grounded evidence in the provided corpus to answer that question."
MIN_GROUNDING_SCORE = 0.25
MIN_QUERY_COVERAGE = 0.60


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]
    refused: bool


def build_grounded_answer(question: str, chunks: list[Chunk], top_k: int = 2) -> RagAnswer:
    results = retrieve_top_k(question, chunks, k=top_k)
    if not results:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    best = results[0]
    # One incidental keyword is not enough evidence for a claim.  Require a
    # reasonably focused top result that covers most meaningful question terms.
    if best.score < MIN_GROUNDING_SCORE or best.query_coverage < MIN_QUERY_COVERAGE:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    # Cite only chunks that independently meet the grounding bar.  Lower-ranked
    # lexical matches remain visible in CLI retrieval evidence, but do not get
    # presented as support for the answer.
    grounded_results = [
        item
        for item in results
        if item.score >= MIN_GROUNDING_SCORE
        and item.query_coverage >= MIN_QUERY_COVERAGE
    ]

    supporting_points = []
    citations = []
    for item in grounded_results:
        citations.append(item.chunk.chunk_id)
        supporting_points.append(f"[{item.chunk.chunk_id}] {item.chunk.text}")

    answer = (
        "Grounded response based on retrieved context:\n"
        + "\n".join(supporting_points)
        + "\n\nCitations: "
        + ", ".join(f"[{citation}]" for citation in citations)
    )
    return RagAnswer(answer=answer, citations=citations, refused=False)
