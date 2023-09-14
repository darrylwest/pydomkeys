#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-09-12 18:16:26

import sys
from rich import print
from pydomkeys.keys import KeyGen
import time

shard_count = 4
keygen = KeyGen.create("T1", shard_count)
max_count = 250_000

# TODO(dpw): add thread pool workers with mpire


def test_txkey():
    keys = (keygen.txkey() for _ in range(max_count))

    for key in keys:
        assert len(key) == 12, f"key: {key} has incorrect length {len(key)}"

        # TODO(dpw): test for uniqueness

    return True


def test_route_key():
    keys = (keygen.route_key() for _ in range(max_count))

    for key in keys:
        assert (
            len(key) == 16
        ), f"ERROR! route key: {key} has incorrect length {len(key)}"
        shard = keygen.parse_route(key)
        assert (
            shard < shard_count
        ), f"[red] ERROR! route key has a bad shard parse {shard}"

        # TODO(dpw): test for uniqueness


def main(args: list) -> None:
    # print(f'{args}')

    t0 = time.time_ns()
    test_txkey()
    test_route_key()
    t1 = time.time_ns()
    elapsed = (t1 - t0) / 1_000_000_000

    print(f"[green3]stress tests completed {max_count} rounds without error, time: {elapsed} seconds...")


if __name__ == "__main__":
    main(sys.argv[1:])
