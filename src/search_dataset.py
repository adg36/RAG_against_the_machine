from .exceptions import ParseError
from .loader import load_answered_questions, load_unanswered_questions
from .search import load_index, perform_search, validate_int_input


def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:

    validate_int_input(k, name="k")
    if not dataset_path:
        raise ParseError("Invalid argument. "
                         "The dataset_path must be a valid path.")

    # verify if save_directory is valid
    # save directory should be data/output/search_results/<DatasetScope>/
    # e.g. data/output/search_results/UnansweredQuestions/dataset_docs_public.json

    loaded_index = load_index()

    if k > len(loaded_index.corpus):
        k = len(loaded_index.corpus)

    load_unanswered_questions()
    # for each question in the dataset:
    perform_search(loaded_index, query, k)

    print(f"Saved student_search_results to {save_directory}")

    # write a StudentSearchResults JSON file, validated with pydantic
