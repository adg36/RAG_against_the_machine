from pathlib import Path
import fire
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document

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
        py_docs = perform_doc_chunking(code_text, filepath, "python", max_chunk_size)
        collection.extend(py_docs)
        py_count += 1

    for filepath in corpus.rglob("*.md"):
        md_text = filepath.read_text()
        md_docs = perform_doc_chunking(md_text, filepath, "markdown", max_chunk_size)
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


def perform_doc_chunking(
        file_contents: str,
        file_path: Path,
        language: str = "python",
        chunk_size: int = 500,
        chunk_overlap: int = 15,
        add_start_index: bool = True) -> list[Document]:

    if language.lower() == "python":
        doc_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=add_start_index
        )
    elif language.lower() == "markdown":
        doc_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=add_start_index
        )
    else:
        doc_splitter = RecursiveCharacterTextSplitter(
            separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=add_start_index
        )

    metadatas: dict[Any, Any] = {"file_path": str(file_path)}

    chunks = doc_splitter.create_documents([file_contents], [metadatas])

    get_end_index(chunks)
    # print(f"Total chunks: {len(chunks)}")
    # print(file_contents[chunks[5].metadata["start_index"]:chunks[5].metadata["excl_end_index"]] == chunks[5].page_content)

    return chunks


def get_end_index(chunks: list[Document]) -> list[Document]:
    for chunk in chunks:
        excl_end_index = chunk.metadata["start_index"] + len(chunk.page_content)
        chunk.metadata["excl_end_index"] = excl_end_index
    return chunks


# FIRE COMMANDS
def search(query: str, k: int) -> None:
    print(f"Query: {query}\nk: {k}")

def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:
    pass

def answer(query: str, k: int) -> None:
    pass

def answer_dataset(student_search_results_path: str, save_directory: str) -> None:
    pass

def evaluate(student_search_results_path: str, dataset_path: str) -> None:
    pass

if __name__ == "__main__":
    try:
        fire.Fire()
    except (ValueError, TypeError) as e:
        print(f"ERROR: {e}")
