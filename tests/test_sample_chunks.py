from src.chunking import perform_doc_chunking
from pathlib import Path

def test_sample_chunks():

    corpus = Path("tests/fixtures")

    for filepath in corpus.rglob("*"):
        code_text = filepath.read_text()
        docs = perform_doc_chunking(
            code_text, filepath)
        for chunk in docs:
            start_index = chunk.metadata["start_index"]
            end_index = chunk.metadata["start_index"] + len(chunk.page_content)
            slice = code_text[start_index:end_index]

    assert slice == chunk.page_content
