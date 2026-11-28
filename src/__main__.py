import fire
import sys
from typing_extensions import Any, Dict
from .answer import answer
from .evaluate import evaluate
from .exceptions import RagError
from .index import index
from .search import search, search_dataset


# FIRE COMMANDS
def answer_dataset(student_search_results_path: str, save_directory: str) -> None:
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
