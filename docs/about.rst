Project Overview
================

Key Size Reduction
------------------

Our primary objective is to minimize key sizes when used with key/value stores like Redis or even SQL databases.  Domain keys are gauranteed to be unique for a given domain.  For example, your
set of users may grow into the 10s or 100s of millions.  You need a unique identifier for each user.  But, you don't need a globally unique identifier because these keys are restricted to just
your domain of users.  Or a domain of customers, orders, etc.

Rather than use a V4 :term:`UUID` with 36 characters, it's much better to use a shorter key based on the same technology--a combination of date-time and random numbers.  If you restrict a key
to a specific domain, e.g., users, customers, businesses, etc, the key can be reduced to a combination of a millisecond time stamp and either a random number, or a counter--especially
if the counter range is in the 200K.  Add a bit of random number generation and a two character domain prefix, like `US`, `CU`, `BU`.

So, let say you do reach that 10M users goal?  If you use a UUID, the keys will consume 360,000,000+ bytes.
Compare that to 160,000,000 and you have cut your memory requirements by more than one half.

Routing for Sharding
--------------------

The composition of the DomainKey includes two character domain followed by a two character random number to provide automatic shard-routing for 256 shards, or any divisable of 256.
Lets say your user base starts to approach 1M.  If you use domain keys with random rounting, it's easy to split this into two, four, or eight shards.  With four shards, each database instance
now has 250K users--a much more manageable number.

So the idea is to start with a single instance but include the uniformally random routing as the key.  When it's time to shard, you simply implement shard-routing logic and you are good to go.
This is a life saver for startups that should think about sharding, but don't really need to shard until the time comes.

Domain Routing Key Features...
------------------------------

    * fast, uniformly distributed random number generation based on large range (10^40?) of values
    * time based to the microsecond
    * base62 encoded for size reduction: ``[0-9][A-Z][a-z]``
    * routing key is always 16 characters, 9 date and 7 random including routing key (first two chars)
    * similar to UUID V7 where a timestamp is mixed with random, specifically random + timestamp(micros) + random
    * route-able, not sortable (although sort_by could be implemented for the timestamp portion of the key)
    * short, time based keys from _txkey_ generate 12 character keys.

The goal of the random number generation is speed and uniformity-- not security.  Domain keys are suitable for identifying elements in a specific domain.  Uniformaty is important for routing to insure equally.

