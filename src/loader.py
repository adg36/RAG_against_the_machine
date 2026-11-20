from pydantic import ValidationError
from .exceptions import LoadingError
from .models import RagDataset


def load_rag_dataset(filepath: str) -> RagDataset:

    try:
        with open(filepath, "r") as file:
            json_dataset = file.read()
    except PermissionError as e:
        raise LoadingError(
            "Dataset file does not have reading permissions."
        ) from e
    except FileNotFoundError as e:
        raise LoadingError(
            "Dataset file could not be found."
        ) from e

    try:
        validated_dataset = RagDataset.model_validate_json(json_dataset)
    except ValidationError as e:
        print(f"{e.error_count()} error(s) detected:")
        for error in e.errors():
            print(error['msg'], error['type'])
        raise LoadingError(
            "Could not validate JSON file."
        ) from e

    return validated_dataset
