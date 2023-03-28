from types import GeneratorType

def fetch_lines(fn: str):
    """Read a file line by line

    Positional Arguments:
    fn -- path to file to be read

    Returns:
    Generator of a files' lines
    """
    with open(fn, "r") as fp:
        for line in fp:
            yield line.strip()

def my_min(*args) -> int:
    """Utility function to compute the min of a variable amount of arguments

    Arguments:
    *args -- collection of all arguments passed to the function

    Returns:
    minimum of all function arguments

    Notes:
    Assumes data type of arguments are real numbers
    """
    assert len(args) > 0, f"IndexError: 0-length tuple passed"

    min = args[0]
    for v in args:
        if v < min:
            min = v
    
    return min

def take(iterable, size=1):
    """Build a window with specified size

    Positional Arguments:
    domains     -- iterable collection of domain names
    w           -- desired size of window

    Returns:
    Generator of domain names
    """
    assert isinstance(iterable, GeneratorType), \
            "TypeError: iterable must be a generator object" \
            f", got {type(iterable)}"

    for i in range(size):
        yield next(iterable)
