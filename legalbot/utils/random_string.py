import random
import string


def generate_random_string(length: int) -> int:
    """
    Returns a random string
    """
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for _ in range(length))
    return result_str
