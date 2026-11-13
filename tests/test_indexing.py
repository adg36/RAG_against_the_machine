import bm25s
from src.tokenizer import tokenize
from src.chunking import perform_doc_chunking
from pathlib import Path
from langchain_core.documents import Document
from typing_extensions import List


def test_sample_chunks():

    corpus = Path("tests/fixtures")

    collection: List[Document] = []

    for filepath in corpus.rglob("*"):
        code_text = filepath.read_text()
        docs = perform_doc_chunking(
            code_text, filepath)
        collection.extend(docs)

    tokenized_collection = []

    for doc in collection:
        chunk = doc.page_content
        tokenized_chunk = tokenize(chunk)
        tokenized_collection.append(tokenized_chunk)

    retriever = bm25s.BM25()
    retriever.index(tokenized_collection)

    all_chunks = [doc.page_content for doc in collection]

    query = "what is memory allocation?"
    query_tokens = [tokenize(query)]

    results, scores = retriever.retrieve(query_tokens, corpus=all_chunks, k=3)

    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        print(f"Rank {i+1} (score: {score:.2f}): {doc}")

    retriever.save("fake_chunks_index", corpus=all_chunks)

    assert "memory" in results[0, 0] or "Memory" in results[0, 0], "Top result was not the memory chunk"
    assert scores[0, 0] > scores[0, 1] and scores[0, 0] > scores[0, 2], "Top result was not the highest score"

    reloaded_retriever = bm25s.BM25.load("fake_chunks_index", load_corpus=True)

    results2, scores2 = reloaded_retriever.retrieve(query_tokens, corpus=all_chunks, k=3)

    for i in range(results2.shape[1]):
        doc, score = results2[0, i], scores2[0, i]
        print(f"Rank {i+1} (score: {score:.2f}): {doc}")

    assert (results == results2).all() and (scores == scores2).all(), "Reloading returned different results"
