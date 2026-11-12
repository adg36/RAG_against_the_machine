from langchain_core.documents import Document
import re

def is_camel_case(s: str) -> bool:
    return s != s.lower() and s != s.upper() and "_" not in s and "." not in s and "-" not in s and sum(i.isupper() for i in s[1:-1]) >= 1


def camel_case_split(s: str) -> list[str]:
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


def tokenize(collection: list[Document]) -> list[list[str]]:

    # First pass to get broader tokens

    pattern = r"\w+(?:[-.]\w+)*"
    tokenized_collection = [re.findall(pattern, chunk.page_content) for chunk in collection]

    # Second pass to strip leading and trailing punctuation

    tokenized_collection = [[token.strip("._-") for token in chunk] for chunk in tokenized_collection]

    # Third pass to split CamelCase, underscores, dots and hyphens, keeping all previously created tokens

    separators = r"[_.\-]+"
    for chunk in tokenized_collection:
        for token in chunk:
            if "_" in token or "-" in token or "." in token:
                split_token = re.split(separators, token)
                chunk.extend(split_token)
            elif is_camel_case(token):
                chunk.extend(camel_case_split(token))
            else:
                continue

    # Fourth and final pass to lowercase all tokens

    tokenized_collection = [[token.lower() for token in chunk] for chunk in tokenized_collection]

    # print(tokenized_collection[0])
    # print("\n")
    # print(tokenized_collection[1])
    # print("\n")
    # print(tokenized_collection[2])

    return tokenized_collection
