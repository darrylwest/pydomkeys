# PyDomKeys

```bash
 _____                        __          __  __
|     \.-----.--------.---.-.|__|.-----. |  |/  |.-----.--.--.-----.
|  --  |  _  |        |  _  ||  ||     | |     < |  -__|  |  |__ --|
|_____/|_____|__|__|__|___._||__||__|__| |__|\__||_____|___  |_____|
                                                       |_____|
```

_A python library for domain entity key generation identifiers e.g., user, provider, inventory item, etc. based on the [rust project](https://github.com/darrylwest/domain-keys/tree/main)._

### Overview

#### Domain Routing Key Features...

* fast, uniformly distributed random number generation based on large range (10^40?) of values
* time based to the microsecond
* base62 encoded for size reduction: `[0-9][A-Z][a-z]`
* routing key is always 16 characters, 9 date and 7 random including routing key (first two chars)
* similar to UUID V7 where a timestamp is mixed with random, specifically random + timestamp(micros) + random
* route-able, not sortable (_although sort_by could be implemented for the timestamp portion of the key_)
* short, time based keys from _txkey_ generate 12 character keys.

The goal of the random number generation is speed and uniformity--not security.  Domain keys are suitable for identifying elements in a specific domain.  Uniformaty is important for routing to insure equally.

### When to use

When you...

* need to create unique identifiers for specified domains e.g. users with the minimum key size that will support billions of entities without collision. You also may want to extract the UTC datetime from the key.
* need to decode a portion of the key to implement data routing to dozens of destinations or database shards.
* generate your keys on the rust (or other) application's server side.

### When not to use

If you need to generate a key that is truely globally unique, then use v4 UUID.  You also are not concerned with key size or being compatible with RFC4122 (UUID standard).

### Installation

NOTE: _this package is still in development and not available yet_

`pip install pydomkeys`

### Use

Examples for time based generator `txkey()`...

```python
    >>> from pydomkeys.keys import KeyGen
    >>> keygen = KeyGen()
    >>> keygen.txkey()
    '7l0QKqIlDTME'
    >>> key = keygen.txkey()
    >>> assert len(key) == 12
    >>> key2 = keygen.txkey()
    >>> assert key2 > key
```

Examples for routing key generator `rtkey()`...

```python
    >>> from pydomkeys.keys import KeyGen, DomainRouter
    >>> router = DomainRouter("us")
    >>> keygen = KeyGen(router=router)
    >>> keygen.rtkey()
    'usH67l0fKBYkbOc1'
    >>> key = keygen.txkey()
    >>> assert len(key) == 16
```

### References

* [Base62 Defined](https://en.wikipedia.org/wiki/Base62)
* [UUID RFC4122](https://datatracker.ietf.org/doc/html/rfc4122.html)
* [PCG Fast Algos for Random Number Generation](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf)
* [Redis serialization protocol spec](https://redis.io/docs/reference/protocol-spec/)
* [Using Numpy Random Generator](https://realpython.com/numpy-random-number-generator/)
* [NumPy Random](https://numpy.org/doc/stable/reference/random/index.html)

## License

Except where noted (below and/or in individual files), all code in this repository is dual-licensed under either:

* MIT License ([LICENSE-MIT](LICENSE-MIT) or [http://opensource.org/licenses/MIT](http://opensource.org/licenses/MIT))
* Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0))

###### darryl.west | 2023.09.05
