from pathlib import Path
from tqdm import tqdm
from langchain_core.documents import Document
from .chunking import perform_doc_chunking


corpus = Path("data/raw")


def index(max_chunk_size: int) -> None:

    try:
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be greater than zero.")
        elif max_chunk_size > 2000:
            raise ValueError("max_chunk_size cannot be greater than 2000.")
    except TypeError:
        print("ERROR: max_chunk_size must be an integer between 1 and 2000.")

    py_count = 0
    md_count = 0

    collection: list[Document] = []

    for filepath in corpus.rglob("*.py"):
        code_text = filepath.read_text()
        py_docs = perform_doc_chunking(
            code_text, filepath, "python", max_chunk_size)
        collection.extend(py_docs)
        py_count += 1

    for filepath in corpus.rglob("*.md"):
        md_text = filepath.read_text()
        md_docs = perform_doc_chunking(
            md_text, filepath, "markdown", max_chunk_size)
        collection.extend(md_docs)
        md_count += 1

    largest_chunk_len = 0
    for chunk in collection:
        if len(chunk.page_content) > largest_chunk_len:
            largest_chunk_len = len(chunk.page_content)

    print(f"Total Python files: {py_count}\n"
          f"Total Markdown files: {md_count}")
    print(f"Created collection of {len(collection)} documents")
    print(f"Length of the longest chunk is {largest_chunk_len}")
    print(f"Example of one chunk: {collection[0]}. Chunk length: {len(collection[0].page_content)}")
