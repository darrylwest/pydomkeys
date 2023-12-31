from typing import Optional, Self

from _typeshed import Incomplete

from .base62 import Base62 as Base62

DEFAULT_ALPHABET: Incomplete
dflt_rng: Incomplete

class Counter:
    count: Incomplete
    def __init__(
        self,
        x_min: int = ...,
        x_max: int = ...,
        start: int = ...,
    ) -> None: ...
    def next_count(self) -> int: ...
    def reset(self) -> int: ...

class DomainRouter:
    domain_key: Incomplete
    max_route_size: int
    shard_count: Incomplete
    def __init__(self, domain: str, shard_count: int) -> None: ...
    def domain(self) -> str: ...
    def route(self) -> str: ...

class KeyGen:
    domain_router: Incomplete
    base62: Incomplete
    counter: Incomplete
    def __init__(
        self,
        domain_router: DomainRouter,
        base62: Optional[Base62] = ...,
        counter: Optional[Counter] = ...,
    ) -> None: ...
    @classmethod
    def create(cls, domain: str, shard_count: Optional[int] = ...) -> Self: ...
    def txkey(self, milliseconds: Optional[int] = ...): ...
    def route_key(self, milliseconds: Optional[int] = ...): ...
    def parse_route(self, key: str) -> int: ...
