"""A library for domain entity key generation identifiers.

Author: darryl.west
Date: 2023-08-26
"""

import string

DEFAULT_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase


class Base62:
    """Base62 uses a default alphabet to encode integers to base62.  you can pass in
    alternate alphabets to get diffent encodings.
    """

    def __init__(self, alphabet: str = DEFAULT_ALPHABET):
        """Initialize the alphabet or use the default."""
        self.alphabet = alphabet

    def __repr__(self):
        """Return the current base62 alphabet."""
        return f"base62 alphabet: {self.alphabet}"

    def encode(self, number: int) -> str:
        """Encode the integer number to base62 using the specified alphabet defined at init time."""
        radix = len(self.alphabet)
        base = []

        while True:
            idx = number % radix
            base.append(self.alphabet[idx])

            number = number // radix

            if number == 0:
                break

        base.reverse()

        key = "".join(base)
        return key

    # TODO(dpw): implement decode
    def decode(self, _b62: str) -> int:
        """Decode the base62 encoded string and return the int."""
        return 0
