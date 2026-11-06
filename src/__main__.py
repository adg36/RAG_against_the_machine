from pathlib import Path
import fire
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document

corpus = Path("data/raw")


def index(max_chunk_size: int) -> None:

    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be greater than zero.")
    elif max_chunk_size > 2000:
        raise ValueError("max_chunk_size cannot be greater than 2000")

    py_count = 0
    md_count = 0

    collection: list[Document] = []

    for file_contents in corpus.rglob("*.py"):
        code_text = file_contents.read_text()
        py_docs = perform_doc_chunking(code_text, "python", max_chunk_size)
        collection.extend(py_docs)
        py_count += 1

    for file_contents in corpus.rglob("*.md"):
        md_text = file_contents.read_text()
        md_docs = perform_doc_chunking(md_text, "markdown", max_chunk_size)
        collection.extend(md_docs)
        md_count += 1

    largest_chunk_len = 0
    for doc in collection:
        if len(doc.page_content) > largest_chunk_len:
            largest_chunk_len = len(doc.page_content)

    print(f"Total Python files: {py_count}\n"
          f"Total Markdown files: {md_count}")
    print(f"Created collection of {len(collection)} documents")
    print(f"Length of the longest chunk is {largest_chunk_len}")
    print(f"Example of one document: {collection[0]}")


def perform_doc_chunking(
        file: str,
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

    documents = doc_splitter.create_documents([file])

    print(f"Total documents: {len(documents)}")
    return documents


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
    except ValueError as e:
        print(f"ERROR: {e}")
