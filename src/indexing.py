import bm25s
from pathlib import Path
from tqdm import tqdm
from langchain_core.documents import Document
from typing_extensions import List
from .chunking import perform_doc_chunking
from .tokenizer import tokenize


corpus = Path("data/raw")


def get_filepaths(corpus: Path) -> List[Path]:

    all_filepaths: List[Path] = []
    all_filepaths.extend(list(corpus.rglob("*.py")))
    all_filepaths.extend(list(corpus.rglob("*.md")))

    return all_filepaths


def index(max_chunk_size: int) -> None:

    try:
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be greater than zero.")
        elif max_chunk_size > 2000:
            raise ValueError("max_chunk_size cannot be greater than 2000.")
    except TypeError:
        print("ERROR: max_chunk_size must be an integer between 1 and 2000.")

    all_filepaths = get_filepaths(corpus)

    collection: List[Document] = []

    t = tqdm(
        bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
        desc=f"{'Chunking:':<12}", total=len(all_filepaths), unit=" file")

    for filepath in all_filepaths:
        text = filepath.read_text()
        if filepath.name.endswith(".py"):
            chunks = perform_doc_chunking(
                text, filepath, "python", max_chunk_size)
        elif filepath.name.endswith(".md"):
            chunks = perform_doc_chunking(
                text, filepath, "markdown", max_chunk_size)
        else:
            chunks = perform_doc_chunking(
                text, filepath)
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

    output_dir = "data/processed/"
    retriever = bm25s.BM25()
    retriever.index(tokenized_collection)

    # Save index only
    retriever.save(output_dir)

    # Save index with corpus
    retriever.save(output_dir, corpus=corpus)
    print(
        f"Ingestion complete! Indexed {len(collection)}"
        f" chunks under {output_dir}.")
