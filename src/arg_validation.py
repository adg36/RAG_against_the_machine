from .exceptions import ParseError

def validate_int_input(input: int, name: str) -> None:
    if not isinstance(input, int):
        raise ParseError(f"{name} must be an integer. Got '{input}' ({type(input).__name__})")
    if isinstance(input, bool):
        raise ParseError(f"{name} must be a positive integer, but got True. "
                         f"If you wrote --{name} with nothing after it, add a number, like --{name} [number].")

    if input <= 0:
        raise ParseError(f"{name} must be an integer between 1 and 2000. Got {input}")
    if name == "max_chunk_size":
        if input > 2000:
            raise ParseError(f"{name} must be an integer between 1 and 2000. Got {input}")
