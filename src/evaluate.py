from pathlib import Path
from pydantic import ValidationError
from typing_extensions import List
from .exceptions import LoadingError, ParseError
from .models import MinimalSource, RagDataset, StudentSearchResults


def evaluate(student_search_results_path: str, dataset_path: str) -> None:

    sr_path = Path(student_search_results_path)
    ds_path = Path(dataset_path)

    try:
        results_json = sr_path.read_text()
        dataset_json = ds_path.read_text()
    except FileNotFoundError as e:
        raise LoadingError(
            "JSON file does not exist."
        ) from e
    except PermissionError as e:
        raise LoadingError(
            "JSON file does not have the required permissions."
        )
    except OSError as e:
        raise LoadingError(
            "Unable to read JSON file."
        )

    try:
        validated_results = StudentSearchResults.model_validate_json(results_json)
        validated_dataset = RagDataset.model_validate_json(dataset_json)
    except ValidationError as e:
        print("Student data is valid: False")
        raise ParseError(
            "Unable to validate JSON file against the pydantic models."
        )
    else:
        print("Student data is valid: True")

    relevant_items = 0

    for i, result in enumerate(validated_results.search_results):
        if result.question_id == validated_dataset.rag_questions[i].question_id:
            max_iou = 0.0
            for source in result.retrieved_sources:
                if source.file_path != validated_dataset.rag_questions[i].sources[0].file_path:
                    continue
                else:
                    iou = compute_iou(source, validated_dataset.rag_questions[i].sources[0])
                    if iou > max_iou:
                        max_iou = iou
            if max_iou > 0.05:
                relevant_items += 1
    recall = relevant_items / len(validated_dataset.rag_questions) * 100
    print("Evaluation Results\n"
          "=========================================\n"
          f"Recall@{validated_results.k}: {recall:.3f}")
            # MAYBE PRESENT ALL K VALUES UNTIL THE K IN THE STUDENT SEARCH RESULT DOC


def compute_iou(retrieved_source: MinimalSource, ground_truth: MinimalSource) -> float:

    r_start = retrieved_source.first_character_index
    r_end = retrieved_source.last_character_index
    g_start = ground_truth.first_character_index
    g_end = ground_truth.last_character_index

    begin_intersection = max(r_start, g_start)
    end_intersection = min(r_end, g_end)
    intersection = end_intersection - begin_intersection
    if intersection < 0:
        intersection = 0

    union = ((r_end - r_start) + (g_end - g_start)) - intersection

    return intersection / union if union > 0 else 0.0
