from src.chunking import build_chunks
from src.corpus import load_default_corpus
from src.rag import build_grounded_answer


def test_build_grounded_answer_returns_citations_for_supported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("What is retrieval augmented generation?", chunks, top_k=2)
    assert result.refused is False
    assert len(result.citations) >= 1
    assert "Citations:" in result.answer
    assert f"[{result.citations[0]}]" in result.answer
    assert "Retrieval augmented generation combines retrieval with text generation." in result.answer


def test_build_grounded_answer_refuses_unsupported_query() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("Who was emperor of Mars?", chunks, top_k=2)
    assert result.refused is True
    assert result.citations == []


def test_build_grounded_answer_refuses_a_partially_matched_claim() -> None:
    chunks = build_chunks(load_default_corpus(), chunk_size=120, overlap=20)
    result = build_grounded_answer("Who invented RAG?", chunks, top_k=2)
    assert result.refused is True


def test_build_grounded_answer_refuses_missing_year_despite_keyword_overlap() -> None:
    from src.corpus import load_training_rag_corpus

    chunks = build_chunks(load_training_rag_corpus(), chunk_size=140, overlap=30)
    result = build_grounded_answer("What year do citations improve transparency and trust?", chunks, top_k=2)
    assert result.refused is True
    assert result.citations == []


def test_build_grounded_answer_cites_only_the_supporting_sentence() -> None:
    from src.corpus import load_training_rag_corpus

    chunks = build_chunks(load_training_rag_corpus(), chunk_size=140, overlap=30)
    result = build_grounded_answer("Why do citations improve transparency and trust?", chunks, top_k=2)
    assert result.refused is False
    assert result.citations == ["tr-doc-1-chunk-1"]
    assert result.answer.startswith("Citations improve transparency and trust because users can verify evidence.")
    assert "the answer." not in result.answer


def test_build_grounded_answer_refuses_terms_scattered_across_sentences() -> None:
    from src.chunking import Chunk

    chunk = Chunk(chunk_id="mixed", doc_id="d", title="Mixed", text="Alpha matters. Beta matters.")
    result = build_grounded_answer("What are alpha and beta?", [chunk], top_k=1)
    assert result.refused is True
    assert result.citations == []
