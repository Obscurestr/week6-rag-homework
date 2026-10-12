from dataclasses import dataclass
import re

from .chunking import Chunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")

# These words occur in many natural-language questions but do not identify a
# subject in this small lexical retriever.  Ignoring them prevents a question
# such as "Who was emperor of Mars?" from matching a chunk merely because both
# contain "was" or "of".
STOP_WORDS = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for",
        "from", "how", "i", "in", "is", "it", "of", "on", "or", "the", "to",
        "was", "what", "when", "where", "which", "who", "why", "with", "would",
    }
)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float
    query_coverage: float


def lexical_score(query: str, chunk_text: str) -> float:
    q_tokens = [token for token in tokenize(query) if token not in STOP_WORDS]
    c_tokens = [token for token in tokenize(chunk_text) if token not in STOP_WORDS]
    if not q_tokens or not c_tokens:
        return 0.0

    q_set = set(q_tokens)
    matched_terms = q_set.intersection(c_tokens)
    coverage = len(matched_terms) / len(q_set)
    density = sum(1 for token in c_tokens if token in q_set) / len(c_tokens)

    # Coverage rewards chunks that address more of the question; density
    # breaks ties in favor of chunks focused on those terms.
    return 0.7 * coverage + 0.3 * density


def query_coverage(query: str, chunk_text: str) -> float:
    """Return the fraction of meaningful question terms found in a chunk."""
    q_terms = {token for token in tokenize(query) if token not in STOP_WORDS}
    if not q_terms:
        return 0.0
    c_terms = set(token for token in tokenize(chunk_text) if token not in STOP_WORDS)
    return len(q_terms.intersection(c_terms)) / len(q_terms)


def retrieve_top_k(query: str, chunks: list[Chunk], k: int = 3, min_score: float = 0.01) -> list[RetrievalResult]:
    if k <= 0:
        raise ValueError("k must be > 0")

    scored = [
        RetrievalResult(
            chunk=chunk,
            score=lexical_score(query, chunk.text),
            query_coverage=query_coverage(query, chunk.text),
        )
        for chunk in chunks
    ]
    filtered = [item for item in scored if item.score >= min_score]
    # chunk_id makes ties reproducible across runs and Python versions.
    filtered.sort(key=lambda item: (-item.score, item.chunk.chunk_id))
    return filtered[:k]
