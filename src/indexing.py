from pathlib import Path
from tqdm import tqdm
from langchain_core.documents import Document
from .chunking import perform_doc_chunking
from .tokenizer import tokenize


corpus = Path("data/raw")

def get_filepaths(corpus: Path) -> list[Path]:

    all_filepaths: list[Path] = []
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

    collection: list[Document] = []

    t = tqdm(total=len(all_filepaths), desc="Chunking", ncols=80, unit=" file")

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

    tokenize(collection)
    print("Tokenization completed")
    # print(f"Created collection of {len(collection)} documents")
    # print(f"Example of one chunk: {collection[0]}. Chunk length: {len(collection[0].page_content)}")
