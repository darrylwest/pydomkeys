#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-09-12 18:16:26

import sys
from rich import print
from pydomkeys.keys import KeyGen
import time

shard_count = 4
keygen = KeyGen.create("T1", shard_count)

# TODO(dpw): add thread pool workers with mpire

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time_ns()
        result = func(*args, **kwargs)
        end_time = time.time_ns()
        elapsed = (end_time - start_time) / 1_000_000_000
        print(f"{func.__name__} took {elapsed} seconds to run.")
        return result
    return wrapper

max_count = 250_000

@timer_decorator
def test_txkey():
    kset = set()

    keys = (keygen.txkey() for _ in range(max_count))

    count = 0
    for key in keys:
        count += 1
        kset.add(key)
        assert len(kset) == count, f"key: {key} was not unique, count: {count}"
        assert len(key) == 12, f"txkey: {key} has incorrect length {len(key)}"

    return max_count == len(kset)


@timer_decorator
def test_route_key():
    kset = set()
    keys = (keygen.route_key() for _ in range(max_count))

    count = 0
    for key in keys:
        count += 1
        kset.add(key)
        assert len(kset) == count, f"route_key: {key} was not unique, count: {count}"

        assert (
            len(key) == 16
        ), f"ERROR! route key: {key} has incorrect length {len(key)}"
        shard = keygen.parse_route(key)
        assert (
            shard < shard_count
        ), f"[red] ERROR! route key has a bad shard parse {shard}"

    return max_count == len(kset)
    


def main(args: list) -> None:
    # print(f'{args}')

    test_txkey()
    test_route_key()

    # print(f"[green3]stress tests completed {max_count} rounds without error, time: {elapsed} seconds...")


if __name__ == "__main__":
    main(sys.argv[1:])
