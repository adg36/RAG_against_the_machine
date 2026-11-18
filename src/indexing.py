import bm25s
from pathlib import Path
from tqdm import tqdm
from langchain_core.documents import Document
from typing_extensions import List
from .chunking import compute_chunk_overlap, perform_doc_chunking
from .exceptions import ParseError
from .tokenizer import tokenize


corpus = Path("data/raw")


def get_filepaths(corpus: Path) -> List[Path]:

    all_filepaths: List[Path] = []
    all_filepaths.extend(list(corpus.rglob("*.py")))
    all_filepaths.extend(list(corpus.rglob("*.md")))
    all_filepaths.extend(list(corpus.rglob("*.txt")))

    return all_filepaths


def _validate_int_input(input: int) -> bool:
    if not isinstance(input, int):
        raise ParseError(f"max_chunk_size must be an integer. Got '{input}' ({type(input).__name__})")
    if isinstance(input, bool):
        raise ParseError(f"max_chunk_size must be an integer. Got '{input}' ({type(input).__name__})")

    if input <= 0:
        raise ParseError(f"max_chunk_size must be an integer between 1 and 2000. Got {input}")
    elif input > 2000:
        raise ParseError(f"max_chunk_size must be an integer between 1 and 2000. Got {input}")


def index(max_chunk_size: int) -> None:

    if not _validate_int_input(max_chunk_size):
        raise ParseError

    chunk_overlap = compute_chunk_overlap(max_chunk_size)

    all_filepaths = get_filepaths(corpus)

    collection: List[Document] = []

    t = tqdm(
        bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
        desc=f"{'Chunking:':<12}", total=len(all_filepaths), unit=" file")

    for filepath in all_filepaths:
        text = filepath.read_text()
        if filepath.name.endswith(".py"):
            chunks = perform_doc_chunking(
                text, filepath, "python", max_chunk_size, chunk_overlap)
        elif filepath.name.endswith(".md"):
            chunks = perform_doc_chunking(
                text, filepath, "markdown", max_chunk_size, chunk_overlap)
        else:
            chunks = perform_doc_chunking(
                text, filepath, "markdown", max_chunk_size, chunk_overlap)
        collection.extend(chunks)
        t.update(1)
    t.close()

    tokenized_collection: List[List[str]] = []

    t = tqdm(
            bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
            desc=f"{'Tokenizing:':<12}", total=len(collection), unit=" chunk")

    for doc in collection:
        chunk = doc.page_content
        tokenized_chunk = tokenize(chunk)
        tokenized_collection.append(tokenized_chunk)
        t.update(1)
    t.close()

    chunk_store = [
        {"path": doc.metadata["file_path"],
         "first_character_index": doc.metadata["start_index"],
         "last_character_index": doc.metadata["excl_end_index"]
        } for doc in collection]

    output_dir = "data/processed/"
    retriever = bm25s.BM25(corpus=chunk_store)
    retriever.index(tokenized_collection)

    # Save index
    retriever.save(output_dir, corpus=chunk_store)

    print(
        f"Ingestion complete! Indexed {len(collection)}"
        f" chunks under {output_dir}.")
