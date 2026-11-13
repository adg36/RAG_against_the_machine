import bm25s
from src.tokenizer import tokenize
from src.chunking import perform_doc_chunking
from pathlib import Path


def test_sample_chunks():

    corpus = Path("tests/fixtures")

    collection = []
    # print(f"All_chunks: {all_chunks}")

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
    # print(f"Query tokens: {query_tokens}")

    results, scores = retriever.retrieve(query_tokens, corpus=all_chunks, k=3)

    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        print(f"Rank {i+1} (score: {score:.2f}): {doc}")

    retriever.save("fake_chunks_index_2", corpus=all_chunks)
