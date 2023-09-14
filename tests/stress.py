#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-09-12 18:16:26

import sys
from rich import print
from pydomkeys.keys import KeyGen
import time
import schedule

shard_count = 4
keygen = KeyGen.create("T1", shard_count)

# TODO(dpw): add thread pool workers with mpire


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time_ns()
        result = func(*args, **kwargs)
        end_time = time.time_ns()
        elapsed = (end_time - start_time) / 1_000_000_000
        name = func.__name__[5:]
        print(f"[green3]{name} took {elapsed} seconds to run, Ok.")
        return result

    return wrapper


@timer_decorator
def test_txkey(max_count: int) -> bool:
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
def test_route_key(max_count: int) -> bool:
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


def run_loops(max_count: int = 500_000, loops: int = 8):
    # print(f'{args}')

    loops = range(1, loops + 1)

    for loop in loops:
        print(f"{loop}) [yellow]Testing txkey with {max_count} rounds: ", end="")
        test_txkey(max_count)
        # print(f"[green3]Ok")

        print(f"{loop}) [yellow]Testing route_key with {max_count} rounds: ", end="")
        test_route_key(max_count)

    print(f"[green3]Stress tests completed without error...")

def main(args: list) -> None:
    if '--at' in args:
        schedule.every().minute.at(':15').do(run_loops)
        print("waiting for scheduled time...")
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        max_count = 500_000
        loops = 5

        run_loops(max_count, loops)


if __name__ == "__main__":
    main(sys.argv[1:])
