# Introduction

There can be at most 3 contiguous integers with exactly 2 prime factors
counting with multiplicity.  The first example of such a three-some is
33=3\*11, 34=2\*17, 35=5\*7.  Every multiple of 4 greater than 4 has at least 3
prime factors since there are at least 2 factors with the prime 2 and some
additional factor.  Therefore any series of contiguous integers with exactly 2
prime factors cannot include a multiple of 4 larger than 4.  Hence 3 is the
most.

In a similar way there can be sets of 7 contiguous integers with exactly 3
prime factors.  Generally for some integer $n>1$ there probably exists $2^n-1$
contiguous integers with exactly $n$ prime factors.

This repository searches for such integer sets.  The search seems stymied
computationally for $n>4$ but we show here a sequence of 15 integers with
exactly 4 prime factors.
