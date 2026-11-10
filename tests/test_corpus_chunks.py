from src.chunking import perform_doc_chunking
from pathlib import Path


def test_corpus_chunks():

    corpus = Path("data/raw")

    py_fails = []
    md_fails = []
    py_files = 0
    md_files = 0
    total_chunks = 0
    largest_span = 0

    for filepath in corpus.rglob("*.py"):
        py_files += 1
        code_text = filepath.read_text()
        py_docs = perform_doc_chunking(
            code_text, filepath, "python")
        for chunk in py_docs:
            total_chunks += 1
            start_index = chunk.metadata["start_index"]
            end_index = chunk.metadata["start_index"] + len(chunk.page_content)
            slice = code_text[start_index:end_index]
            if slice != chunk.page_content:
                py_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Wrong slice")
            elif end_index - start_index > 2000:
                py_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Chunk is larger than 2000 characters")
            elif start_index < 0 or end_index > len(code_text):
                py_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Indices are outside the file")
            elif end_index - start_index > largest_span:
                largest_span = end_index - start_index

    for filepath in corpus.rglob("*.md"):
        md_files += 1
        md_text = filepath.read_text()
        md_docs = perform_doc_chunking(
            md_text, filepath, "markdown")
        for chunk in md_docs:
            total_chunks += 1
            start_index = chunk.metadata["start_index"]
            end_index = chunk.metadata["start_index"] + len(chunk.page_content)
            slice = md_text[start_index:end_index]
            if slice != chunk.page_content:
                md_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Wrong slice")
            elif end_index - start_index > 2000:
                md_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Chunk is larger than 2000 characters")
            elif start_index < 0 or end_index > len(md_text):
                md_fails.append(f"Path: {filepath}, Chunk start: {start_index}, Error: Indices are outside the file")
            elif end_index - start_index > largest_span:
                largest_span = end_index - start_index

    print(f"\nTotal .py files: {py_files}")
    print(f"Total .md files: {md_files}")
    print(f"Total chunks: {total_chunks}")
    print(f"Largest span: {largest_span}")
    assert len(py_fails) == 0 and len(md_fails) == 0
