import bm25s
import os
from pathlib import Path
from typing_extensions import List
from tqdm import tqdm
from .arg_validation import validate_int_input
from .exceptions import LoadingError, ParseError
from .loader import load_rag_dataset
from .models import MinimalSearchResults, MinimalSource, StudentSearchResults
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
    output_dir = Path(save_directory)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f"Error: path invalid or general system I/O error.")
        raise LoadingError #FILL IN THE REST
    filename = Path(dataset_path).name

    if k > len(loaded_index.corpus):
        k = len(loaded_index.corpus)

    search_results: List[MinimalSearchResults] = []

    for item in tqdm(dataset.rag_questions,
                     bar_format="{desc}{percentage:3.0f}%|{bar:30}{r_bar}",
                     desc=f"{'Searching:':<12}",
                     unit=" questions"):
        query = item.question
        query_tokens = [tokenize(query)]
        # if len(query_tokens) == 0:
            # decide what to do for an empty question
        retrieved_sources: List[MinimalSource] = []
        results, scores = loaded_index.retrieve(query_tokens, k=k)
        for i in range(results.shape[1]):
            doc, score = results[0, i], scores[0, i]
            # if i == 0 and score == 0:
                # decide what to do if the first result has score 0
            # else:
            minimal_source = MinimalSource(
                file_path=doc['path'],
                first_character_index=doc['first_character_index'],
                last_character_index=doc['last_character_index']
            )
            retrieved_sources.append(minimal_source)
        search_result = MinimalSearchResults(
            question_id=item.question_id,
            question=item.question,
            retrieved_sources=retrieved_sources)
        search_results.append(search_result)

    output_text = StudentSearchResults(search_results=search_results, k=k)
    filepath = output_dir / filename
    json_text = output_text.model_dump_json(indent=2)
    try:
        filepath.write_text(json_text)
    except PermissionError as e:
        raise LoadingError("Cannot write to output file.") from e

    print(f"Saved student_search_results to {filepath}")
