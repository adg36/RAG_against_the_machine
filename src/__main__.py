import fire

def index(max_chunk_size: int) -> None:
    print(f"Max chunk size: {max_chunk_size}")

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
    fire.Fire()
