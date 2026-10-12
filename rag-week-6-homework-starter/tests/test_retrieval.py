from src.chunking import Chunk
from src.retrieval import retrieve_top_k


def test_retrieve_top_k_orders_by_score_desc() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="rag retrieval citations evidence"),
        Chunk(chunk_id="b", doc_id="1", title="B", text="weather forecast rain tomorrow"),
    ]
    results = retrieve_top_k("rag citations", chunks, k=2)
    assert results
    assert results[0].chunk.chunk_id == "a"


def test_retrieve_top_k_returns_empty_for_unrelated_query() -> None:
    chunks = [
        Chunk(chunk_id="a", doc_id="1", title="A", text="vector database retrieval"),
    ]
    results = retrieve_top_k("basketball playoffs", chunks, k=2)
    assert results == []


def test_retrieve_top_k_uses_query_coverage_and_stable_ties() -> None:
    chunks = [
        Chunk(chunk_id="b", doc_id="1", title="B", text="rag retrieval"),
        Chunk(chunk_id="a", doc_id="1", title="A", text="rag retrieval"),
        Chunk(chunk_id="c", doc_id="1", title="C", text="rag only"),
    ]
    results = retrieve_top_k("rag retrieval", chunks, k=3)
    assert [item.chunk.chunk_id for item in results] == ["a", "b", "c"]
    assert results[0].query_coverage == 1.0
