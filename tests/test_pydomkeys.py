#!/usr/bin/env python -m tests.test_domkey
# dpw@plaza.localdomain
# 2023-08-26 23:48:35

import sys
from rich.console import Console
from datetime import datetime

from pydomkeys.keys import KeyGen, Counter, DomainRouter
from pydomkeys.base62 import Base62
from pathlib import Path
import tomllib

console = Console()


def test_txkey():
    """Test the txkey."""
    console.rule("Default KeyGen.txkey")
    router = DomainRouter("tt", 1)
    keygen = KeyGen(domain_router=router)

    lastkey = None
    for n in range(20):
        key = keygen.txkey()
        assert len(key) == 12

        # ensure that the time has advanced...
        if lastkey is None:
            lastkey = key
        else:
            assert lastkey[0:9] != key[0:9]
            lastkey = key

        console.log(f"{n} {key=}")


def test_counter():
    """Test the counter."""
    console.rule("Default counter for large and small numbers")
    counter = Counter()
    console.log(counter)
    n = counter.next_count()
    console.log(f"initial count: {n}")

    assert n in range(counter.min, counter.max)

    n_min = 10
    n_max = 15
    start = n_min

    counter = Counter(n_min, n_max, start)
    assert counter.min == n_min
    assert counter.max == n_max

    console.log(f"{n_min=}, {n_max=}")
    for n in range(n_min, n_max):
        assert counter.count == n
        assert counter.next_count() == n + 1
        console.log(f"count: {n}")

    n = counter.next_count()
    console.log(f"count: {n}")
    assert n == n_min

    counter.next_count()
    counter.next_count()
    n = counter.reset()
    assert n == n_min


def test_domain_router():
    dom = "US"
    shard_count = 4
    domr = DomainRouter(domain=dom, shard_count=shard_count)
    console.log(domr)
    assert isinstance(domr, DomainRouter)

    assert domr.domain() == dom
    route = domr.route()
    assert len(route) == 2


def test_base62():
    """Test the base62 op."""
    console.rule("Default Base62 for min/max dates for 9 characters")

    base62 = Base62()
    console.log(base62)

    # don't forget to set the timezone to zulu/utc
    dt = datetime.fromisoformat("2000-01-01T00:00:00Z")
    ds = int(dt.timestamp()) * 1_000_000

    assert ds == 946684800000000

    enc = base62.encode(ds)
    console.log(f"min date: {dt} {ds=} = {enc} len = {len(enc)}")

    assert len(enc) == 9

    dt = datetime.fromisoformat("2390-12-01T00:00:00Z")
    ds = int(dt.timestamp() * 1_000_000)

    enc = base62.encode(ds)
    console.log(f"max date: {dt} {ds=} = {enc} len = {len(enc)}")

    assert len(enc) == 9

    n = base62.decode(enc)
    assert n == 0


def test_route_key():
    """Test the route_key."""
    router = DomainRouter("tt", 8)
    keygen = KeyGen(domain_router=router)
    key = keygen.route_key()
    assert len(key) == 16
    assert key.startswith("tt")
    route = key[2:4]
    assert int(route, 16) < 256


def test_factory_constructor():
    keygen = KeyGen.create("ZZ")
    console.log(keygen)
    key = keygen.route_key()
    assert len(key) == 16
    assert key.startswith("ZZ")
    route = key[2:4]
    assert int(route, 16) < 256


def test_parse_route():
    shard_count = 4
    keygen = KeyGen.create("us", shard_count)
    key = keygen.route_key()
    shard = keygen.parse_route(key)
    assert shard < shard_count


def test_version():
    from pydomkeys import __version__ as vers

    assert vers.startswith("0.3.")
    with Path.open(
        "./pyproject.toml",
        "rb",
    ) as f:
        project = tomllib.load(f)

    assert vers == project["tool"]["poetry"]["version"]


if __name__ == "__main__":
    args = sys.argv[1:]

    test_txkey()
    test_base62()
    test_counter()
    test_route_key()
