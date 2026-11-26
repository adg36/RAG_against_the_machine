import bm25s
from pathlib import Path
from tqdm import tqdm
from langchain_core.documents import Document
from typing_extensions import List
from .arg_validation import validate_int_input
from .chunk import compute_chunk_overlap, perform_doc_chunking
from .tokenizer import tokenize


corpus = Path("data/raw")


def get_filepaths(corpus: Path) -> List[Path]:

    all_filepaths: List[Path] = []
    all_filepaths.extend(list(corpus.rglob("*.py")))
    all_filepaths.extend(list(corpus.rglob("*.md")))
    all_filepaths.extend(list(corpus.rglob("*.txt")))

    return all_filepaths


def index(max_chunk_size: int) -> None:

    validate_int_input(max_chunk_size, name="max_chunk_size")

    chunk_overlap = compute_chunk_overlap(max_chunk_size)

    all_filepaths = get_filepaths(corpus)

    collection: List[Document] = []

    t = tqdm(
        bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
        desc=f"{'Chunking:':<12}", total=len(all_filepaths), unit=" files")

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

    for doc in tqdm(collection,
                    bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
                    desc=f"{'Tokenizing:':<12}", unit=" chunks"):
        chunk = doc.page_content
        tokenized_chunk = tokenize(chunk)
        tokenized_collection.append(tokenized_chunk)

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
        f" chunks under {output_dir}")
