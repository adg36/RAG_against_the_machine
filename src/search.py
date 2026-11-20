import bm25s
import os
from .arg_validation import validate_int_input
from .exceptions import LoadingError, ParseError
from .tokenizer import tokenize


def load_index():
    if not os.path.exists("data/processed/"):
        raise LoadingError("Unable to find data/processed/ directory. "
                           "Run the index command first.")
    try:
        reloaded_retriever = bm25s.BM25.load(
            "data/processed/", load_corpus=True)
    except FileNotFoundError:
        raise LoadingError("No index found in data/processed/. "
                            "Run the command index again.")
    except PermissionError:
        raise LoadingError("Index file does not have the required permissions")
    if reloaded_retriever.corpus is None:
        raise LoadingError("The index in data/processed/ has no chunk data. "
                            "Run the command index again.")
    return reloaded_retriever


def search(query: str, k: int) -> None:

    validate_int_input(k, name="k")
    if not query:
        raise ParseError("Invalid argument. "
                         "The query must be a valid question.")

    loaded_index = load_index()

    if k > len(loaded_index.corpus):
        k = len(loaded_index.corpus)

    perform_search(loaded_index, query, k)


def perform_search(index: bm25s.BM25, query: str, k: int) -> None:

    query_tokens = [tokenize(query)]

    if len(query_tokens) == 0:
        raise ParseError("Invalid query.")

    results, scores = index.retrieve(query_tokens, k=k)

    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        if i == 0 and score == 0:
            raise ParseError("Invalid query.")
        print(
            f"{doc['path']} [{doc['first_character_index']}:"
            f"{doc['last_character_index']}]")
