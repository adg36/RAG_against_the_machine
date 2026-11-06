import fire


# FIRE COMMANDS
def search(query: str, k: int) -> None:
    print(f"Query: {query}\nk: {k}")


def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:
    pass


def answer(query: str, k: int) -> None:
    pass


def answer_dataset(student_search_results_path: str, save_directory: str) -> None:
    pass


def evaluate(student_search_results_path: str, dataset_path: str) -> None:
    pass


if __name__ == "__main__":
    try:
        fire.Fire()
    except (ValueError, TypeError) as e:
        print(f"ERROR: {e}")
