from typing import Any
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document


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
