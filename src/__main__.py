import fire
import sys
from typing_extensions import Any, Dict
from .exceptions import RagError
from .indexing import index
from .search import search


# FIRE COMMANDS
def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:
    pass


def answer(query: str, k: int) -> None:
    pass


def answer_dataset(student_search_results_path: str, save_directory: str) -> None:
    pass


def evaluate(student_search_results_path: str, dataset_path: str) -> None:
    pass


if __name__ == "__main__":
    commands: Dict[str, Any] = {
        "index": index,
        "search": search,
        "search_dataset": search_dataset,
        "answer": answer,
        "answer_dataset": answer_dataset,
        "evaluate": evaluate
    }

    try:
        fire.Fire(component=commands)
    except RagError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
