"""A library for domain entity key generation identifiers.

This module supports functions that create time-based, base62 domain keys.  The keys
are based on the current time in millisecons and a 3 digit counter that increments
with each new key.  The keys are sortable based on creation date and counter.

Examples:
--------
    >>> from pydomkeys.base62 import Base62
    >>> from pydomkeys.keys import KeyGen
    >>> keygen = KeyGen("xx") # '7l0QKqIlDTME'
    >>> key = keygen.txkey()
    >>> assert len(key) == 12
    >>> key2 = keygen.txkey()
    >>> assert key2 > key
    

The module contains the following functions:
- `txkey()` - Returns a 12 character base62 txkey
- `route_key()` - Returns a 16 character base62 txkey

Author: darryl.west
Date: 2023-08-26
"""

import string
import time
from random import randint
from typing import Optional, Self

from pydomkeys.base62 import Base62

DEFAULT_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase


class Counter:
    """Counter for sufix generation."""

    def __init__(self, x_min: int = 3_850, x_max: int = 238_000, start: int = -1):
        """Initialize x_min to 3,850, x_max to 238,000, start value.

        The x_min and x_max ensure that the base62 key will always be 12 characters.
        """
        self.min, self.max = x_min, x_max

        if start < 0:
            start = randint(x_min, x_max)

        self.count = start

    def __repr__(self):
        """Show the current count, min and max."""
        return f"count: {self.count}, min: {self.min}, max: {self.max}"

    def next_count(self) -> int:
        """Increment the count and return the int; roll-over to x_min when reaching x_max."""
        count = self.count + 1
        if count > self.max:
            count = self.min

        self.count = count

        return count

    def reset(self) -> int:
        """Reset the counter to minimum and return the value."""
        self.count = self.min
        return self.count


class DomainRouter:
    """Domain Router class used to generate domain and route prefix for route_key."""

    def __init__(self, domain: str, shard_count: int):
        """Initialise DomainRouter with a two character domain label and optional route-generator."""
        self.domain_key = domain
        self.max_route_size = 256
        self.shard_count = shard_count

    def __repr__(self):
        """Show the domain key."""
        return f"domain key: {self.domain_key}, shards: {self.shard_count}"

    def domain(self) -> str:
        """Return the domain key, usually two characters."""
        return self.domain_key

    def route(self) -> str:
        """Return the random routing/shard key, usually two characters 00 through ff for one of 256 routes."""
        return f"{randint(0, self.max_route_size):02x}"


class KeyGen:
    """KeyGen class used to generate txkey and route_key."""

    def __init__(
        self,
        domain_router: DomainRouter,
        base62: Optional[Base62] = None,
        counter: Optional[Counter] = None,
    ):
        """Initialize the base62 worker and counter.

        The default constructor creates Base62 and Counter instances in thier
        default states.  See those modules for ways to change the alphabet or
        min/max counter ranges.
        """
        self.domain_router = domain_router
        base62 = Base62() if base62 is None else base62
        counter = Counter() if counter is None else counter

        self.base62 = base62
        self.counter = counter

    def __repr__(self):
        """Show the domain router, base62 and counter objects."""
        return f"router: {self.domain_router}, base62: {self.base62}, counter: {self.counter}"

    @classmethod
    def create(cls, domain: str, shard_count: Optional[int] = None) -> Self:
        """Create a standard KeyGen instance with the given domain string.

        Examples:
        --------
            >>> from pydomkeys.keys import KeyGen
            >>> keygen = KeyGen.create("CG")
            >>> keygen.base62.alphabet
            '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            >>> keygen.counter.min
            3850
            >>> keygen.counter.max
            238000
            >>> key = keygen.route_key()
            >>> assert len(key)

        """
        shard_count = 1 if shard_count is None else shard_count
        return cls(DomainRouter(domain, shard_count))

    def txkey(self, milliseconds: Optional[int] = None):
        """Generate a new 12 character txkey with the current counter."""
        milliseconds = time.time_ns() // 1_000 if milliseconds is None else milliseconds

        # get the microsecond time stamp and encode to base 64
        key = self.base62.encode(milliseconds)

        # now fill in the next 3 random numbers
        num = self.counter.next_count()
        suffix = self.base62.encode(num)

        return f"{key}{suffix}"

    def route_key(self, milliseconds: Optional[int] = None):
        """Return a routing key, always 16 characters base62 encoded.

        Routing is a way to future-proof your application by preparing for sharding.  The route key
        has two characters reserved for randomly routing between up to 256 shards.  The practical way
        to scale from no shards to mulitples, say 2, 4, 8, etc. without changing any data would be to
        intercept database reads and writes for specific domains, lets say users and use the routing
        key to point to the appropriate shard.

        Examples:
        --------
            >>> from pydomkeys.keys import KeyGen
            >>> keygen = KeyGen.create("US") # a user domain key generator
            >>> key = keygen.route_key() # USec7l4yy4kG56VN
            >>> assert len(key) == 16

        """
        milliseconds = time.time_ns() // 1_000 if milliseconds is None else milliseconds

        key = self.txkey(milliseconds)
        prefix = self.domain_router.domain()
        route = self.domain_router.route()

        return f"{prefix}{route}{key}"

    def parse_route(self, key: str) -> int:
        """Parse the route from the key and return the route number based on the number of shards.

        Parse the database shard route number as configured in the key generator.

        Examples:
        --------
            >>> from pydomkeys.keys import KeyGen
            >>> shard_count = 8
            >>> user_keygen = KeyGen.create(domain="US", shard_count=shard_count) # a user domain key generator
            >>> key = user_keygen.route_key() # US4e7l52VCYlQmbm
            >>> assert len(key) == 16
            >>> db_route = user_keygen.parse_route(key)
            >>> assert db_route < shard_count

        """
        route = int(key[2:4], 16)

        return route % self.domain_router.shard_count
