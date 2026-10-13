from dataclasses import dataclass

from .corpus import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    text: str


def split_text_with_overlap(text: str, chunk_size: int = 140, overlap: int = 30) -> list[str]:
    """Split normalized text into readable, overlapping character windows.

    ``chunk_size`` and ``overlap`` are measured in characters.  When possible,
    a chunk ends and the next chunk begins on a whitespace boundary so that a
    retrieved snippet does not start or end halfway through a word.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))

        # Prefer a complete word when there is a useful boundary in this
        # window.  A single long token still falls back to a hard split, which
        # guarantees progress for inputs such as a long URL or identifier.
        if end < len(cleaned):
            boundary = cleaned.rfind(" ", start + 1, end + 1)
            if boundary > start:
                end = boundary

        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break

        next_start = end - overlap
        if next_start <= start:
            # A word boundary can make this window shorter than the requested
            # overlap. Do not jump past its end and lose unread characters.
            next_start = min(end, start + step)

        # Start the following chunk at a word boundary when overlap lands in
        # the middle of a token.  This can make the effective overlap slightly
        # smaller, but keeps every snippet readable.
        if next_start < len(cleaned) and cleaned[next_start] == " ":
            next_start += 1
        elif next_start > 0 and cleaned[next_start - 1] != " ":
            # Preserve the word that contains the overlap boundary when one
            # is available. Otherwise keep the hard split: moving to the next
            # space would discard the rest of a long token.
            previous_space = cleaned.rfind(" ", start + 1, next_start)
            if previous_space != -1:
                next_start = previous_space + 1

        start = next_start

    return chunks


def build_chunks(documents: list[Document], chunk_size: int = 140, overlap: int = 30) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        parts = split_text_with_overlap(doc.text, chunk_size=chunk_size, overlap=overlap)
        for i, part in enumerate(parts):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}-chunk-{i}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    text=part,
                )
            )
    return chunks
