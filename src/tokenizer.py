from typing_extensions import List
import re


def _is_camel_case(s: str) -> bool:
    return (
        s != s.lower() and s != s.upper()
        and "_" not in s and "." not in s
        and "-" not in s and sum(i.isupper() for i in s[1:-1]) >= 1)


def _camel_case_split(s: str) -> List[str]:
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


def tokenize(string: str) -> List[str]:
    # First pass to get broader tokens

    pattern = r"\w+(?:[-.]\w+)*"
    tokenized_string = re.findall(pattern, string)

    # Second pass to strip leading and trailing punctuation

    tokenized_string = [token.strip("._-") for token in tokenized_string]

    # Third pass to split CamelCase, underscores, dots and hyphens,
    # keeping all previously created tokens

    separators = r"[_.\-]+"
    for token in tokenized_string:
        if "_" in token or "-" in token or "." in token:
            split_token = re.split(separators, token)
            tokenized_string.extend(split_token)
        elif _is_camel_case(token):
            tokenized_string.extend(_camel_case_split(token))
        else:
            continue

    # Fourth and final pass to lowercase all tokens

    tokenized_string = [token.lower() for token in tokenized_string]

    return tokenized_string
