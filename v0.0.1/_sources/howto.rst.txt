When to use
===========

When you...

* need to create unique identifiers for specified domains e.g. users with the minimum key size that will support billions of entities without collision. You also may want to extract the UTC datetime from the key.
* need to decode a portion of the key to implement data routing to dozens of destinations or database shards.
* generate your keys on the rust (or other) application's server side.

When not to use
===============

If you need to generate a key that is truely globally unique, then use v4 UUID.  You also are not concerned with key size or being compatible with RFC4122 (UUID standard).

Installation
============

NOTE: this package is still in development and not available yet

``pip install pydomkeys``

Use
===

Examples for time based generator ``txkey()``...

.. code-block::python
    >>> from pydomkeys.keys import KeyGen
    >>> keygen = KeyGen()
    >>> keygen.txkey()
    '7l0QKqIlDTME'
    >>> key = keygen.txkey()
    >>> assert len(key) == 12
    >>> key2 = keygen.txkey()
    >>> assert key2 > key


Examples for routing key generator ``route_key()``...

.. code-block::python
    >>> from pydomkeys.keys import KeyGen, DomainRouter
    >>> router = DomainRouter("us")
    >>> keygen = KeyGen(router=router)
    >>> keygen.route_key()
    'usH67l0fKBYkbOc1'
    >>> key = keygen.route_key()
    >>> assert len(key) == 16


Or, use the factory method ``create`` to get a new instance...

.. code-block::python
    >>> from pydomkeys.keys import KeyGen
    >>> keygen = KeyGen.create("US")
    >>> keygen.route_key()
    'USH67l0fKBYkbOc1'
    >>> key = keygen.route_key()
    >>> route_number = int(key[2:4], 16)
    >>> assert route_number < 256




Contribute to ``pydomkeys``
---------------------------

Interested in contributing to this project?  If so, check our our [contributing guidelines](./CONTRIBUTING.md) document as well as our [code of conduct](./CODE_OF_CONDUCT.md).


