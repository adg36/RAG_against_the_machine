from pydantic import TypeAdapter
from typing_extensions import List
from .exceptions import LoadingError
from .models import AnsweredQuestion, UnansweredQuestion


def load_unanswered_questions(filepath: str) -> List[UnansweredQuestion]:

    uq_adapter = TypeAdapter(List[UnansweredQuestion])

    try:
        with open(filepath, "r") as file:
            json_unanswered_questions = file.read()
    except PermissionError as e:
        raise LoadingError(
            "Unanswered questions file does not have reading permissions."
        ) from e
    except FileNotFoundError as e:
        raise LoadingError(
            "Unanswered questions file could not be found."
        ) from e

    try:
        validated_unanswered_questions = uq_adapter.validate_json(json_unanswered_questions)
    except ValueError as e:
        print(f"ERROR: {e}")
        raise LoadingError(
            "Could not validate JSON file."
        ) from e

    if not validated_unanswered_questions:
        raise LoadingError(
            "No questions were found in the dataset."
        )
    return validated_unanswered_questions


def load_answered_questions(filepath: str) -> List[AnsweredQuestion]:

    uq_adapter = TypeAdapter(List[AnsweredQuestion])

    try:
        with open(filepath, "r") as file:
            json_answered_questions = file.read()
    except PermissionError as e:
        raise LoadingError(
            "Answered questions file does not have reading permissions."
        ) from e
    except FileNotFoundError as e:
        raise LoadingError(
            "Answered questions file could not be found."
        ) from e

    try:
        validated_answered_questions = uq_adapter.validate_json(json_answered_questions)
    except ValueError as e:
        print(f"ERROR: {e}")
        raise LoadingError(
            "Could not validate JSON file."
        ) from e

    if not validated_answered_questions:
        raise LoadingError(
            "No questions were found in the dataset."
        )
    return validated_answered_questions
