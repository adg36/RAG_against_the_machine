from pathlib import Path
import fire
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

corpus = Path("data/raw")


def index(max_chunk_size: int) -> None:

    # for file in corpus.rglob("*.py"):
    python_files = list(corpus.rglob("*.py"))
    print(f"First file: {python_files[0]}")

    code_text = python_files[0].read_text()

    perform_doc_chunking(code_text)

    # py_count = len(list(corpus.rglob("*.py")))
    # md_count = len(list(corpus.rglob("*.md")))

    # print(f"Number of .py files: {py_count}\n"
    #       f"Number of .md files: {md_count}")


def perform_doc_chunking(
        file: str,
        language: str = "python",
        chunk_size: int = 100,
        chunk_overlap: int = 15,
        add_start_index: bool = True) -> list[str]:

    if language.lower() == "python":
        doc_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True
        )
    elif language.lower() == "markdown":
        doc_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True
        )

    chunks = doc_splitter.create_documents([file])
    print(chunks)
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
    fire.Fire()
