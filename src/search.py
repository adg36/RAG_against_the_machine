
import bm25s
from .tokenizer import tokenize
from .exceptions import ParseError

def _is_input_valid(query: str, k: int) -> bool:
    if not isinstance(k, int):
        return False
    if isinstance(k, bool):
        return False

    try:
        int(k)
    except ValueError:
        return False

    if k <= 0:
        return False

    if not query:
        return False
    return True


def search(query: str, k: int) -> None:
    if not _is_input_valid(query, k):
        raise ParseError("Invalid argument(s). The query must be a valid question and k must be a positive integer.")

    print(f"Query: {query}\nk: {k}")

    reloaded_retriever = bm25s.BM25.load("data/processed/", load_corpus=True)
    query_tokens = [tokenize(query)]

    results, scores = reloaded_retriever.retrieve(query_tokens, k=k)

    for i in range(results.shape[1]):
        doc, _ = results[0, i], scores[0, i]
        print(f"{doc['path']} [{doc['first_character_index']}:{doc['last_character_index']}]")
