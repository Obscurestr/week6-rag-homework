import pytest

from src.chunking import split_text_with_overlap


def test_split_text_with_overlap_returns_multiple_chunks() -> None:
    text = "abcdefghijklmnopqrstuvwxyz" * 4
    chunks = split_text_with_overlap(text, chunk_size=30, overlap=10)
    assert len(chunks) >= 3


def test_split_text_with_overlap_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        split_text_with_overlap("abc", chunk_size=10, overlap=10)


def test_split_text_with_overlap_keeps_word_boundaries_when_possible() -> None:
    chunks = split_text_with_overlap(
        "alpha bravo charlie delta echo foxtrot", chunk_size=18, overlap=6
    )
    assert chunks == [
        "alpha bravo",
        "bravo charlie",
        "charlie delta echo",
        "delta echo foxtrot",
    ]


def test_split_text_with_overlap_does_not_drop_end_of_long_word() -> None:
    chunks = split_text_with_overlap("abcd efgh", chunk_size=2, overlap=1)
    assert "cd" in chunks
    assert "gh" in chunks


def test_split_text_with_overlap_does_not_jump_past_short_first_word() -> None:
    chunks = split_text_with_overlap("a abcdefghijklmnopqrst end", chunk_size=20, overlap=1)
    assert chunks[0] == "a"
    assert chunks[1].startswith("abcdefghijklmnopqr")
    assert chunks[-1].endswith("end")
