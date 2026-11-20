import bm25s
import os
from tqdm import tqdm
from .arg_validation import validate_int_input
from .exceptions import LoadingError, ParseError
from .loader import load_rag_dataset
from .models import MinimalSearchResults, MinimalSource
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

    query_tokens = [tokenize(query)]

    if len(query_tokens) == 0:
        raise ParseError("Invalid query.")

    results, scores = loaded_index.retrieve(query_tokens, k=k)

    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        if i == 0 and score == 0:
            raise ParseError("Invalid query.")
        print(
            f"{doc['path']} [{doc['first_character_index']}:"
            f"{doc['last_character_index']}]")


def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:

    validate_int_input(k, name="k")
    dataset = load_rag_dataset(dataset_path)
    loaded_index = load_index()

    if k > len(loaded_index.corpus):
        k = len(loaded_index.corpus)

    t = tqdm(
            bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
            desc=f"{'Searching:':<12}", total=len(dataset.rag_questions),
            unit=" questions")

    search_results = []

    for item in dataset.rag_questions:
        query = item.question
        print("Query: ", query)
        retrieved_sources = []
        search_result = MinimalSearchResults(item.question_id, item.question, retrieved_sources)
        query_tokens = [tokenize(query)]
        if len(query_tokens) == 0:
            # decide what to do for an empty question
        results, scores = loaded_index.retrieve(query_tokens, k=k)
        for i in range(results.shape[1]):
            doc, score = results[0, i], scores[0, i]
            if i == 0 and score == 0:
                # decide what to do if the first result has score 0
            minimal_source = MinimalSource(
                doc['path'],
                doc['first_character_index'],
                doc['last_character_index']
            )
            retrieved_sources.append(minimal_source)
        
        t.update(1)
    t.close()

    print(f"Saved student_search_results to {save_directory}")

    # write a StudentSearchResults JSON file, validated with pydantic
