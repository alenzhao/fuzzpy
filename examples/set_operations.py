"""\
Set Operations - This example demonstrates the various possible operations on
fuzzy sets.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from common import fuzz

# Let's create a couple fuzzy sets.
A = fuzz.FuzzySet()
A.add_fuzzy('a', 1.0)
A.add_fuzzy('b', 0.5)
A.add_fuzzy('c', 0.8)
B = fuzz.FuzzySet()
B.add_fuzzy('b', 0.8)
B.add_fuzzy('c', 0.2)
B.add_fuzzy('d', 0.6)
B.add_fuzzy('e', 0.0)

print "A = %s" % str(A)
print "B = %s" % str(B)

# First, some basic properties.
print "A has kernel %s and support %s." % (str(A.kernel), str(A.support))
print "B has height %f and scalar cardinality %f." % (B.height, B.cardinality)

# What if we look at the kernel and support of B?
print "B has kernel %s and support %s." % (str(B.kernel), str(B.support))

# Did you notice that 'e' is not in B's support? Actually, if you iterate over
# the elements of B like so...
print "Elements in B are %s" % str([element for element in B])

# ...you will not see 'e'. You can still access it using keys.
print "B has keys %s." % str(B.keys())
print "mu_B(e) = %f" % B['e'].mu

# There is an easier way to check mu values than this, though.
print "mu_B(b) = %f, mu_B(e) = %f" % (B.mu('b'), B.mu('e'))

# It works equally well for objects that don't have a key in the set at all.
print "mu_B(j) = %f" % B.mu('j')

# Alpha cuts return normal (crisp) Python sets.
print "(0.5)B = %s" % str(B.alpha(0.5))
print "(0.5+)A = %s" % str(B.salpha(0.5))

# Standard fuzzy complements are available, but the behaviour is a bit weird:
# the universal set is considered to be the set's keys (it's the best we can
# do), so if you're using this, one approach might be to make sure all your
# sets have keys for every object in the universal set, with mu = 0 unless
# otherwise specified.
print "B' = %s" % str(B.complement())

# Standard fuzzy union and intersection are supported via the | and & operators
# as with Python sets.
print "A | B = %s (standard union)" % str(A | B)
print "A & B = %s (standard intersection)" % str(A & B)

# Other t-conorm and t-norm types are available for unions...
print "A | B = %s (algebraic sum union)" % str(A.union(B, fuzz.FuzzySet.NORM_ALGEBRAIC))
print "A | B = %s (bounded sum union)" % str(A.union(B, fuzz.FuzzySet.NORM_BOUNDED))
print "A | B = %s (drastic union)" % str(A.union(B, fuzz.FuzzySet.NORM_DRASTIC))

# ...and intersections.
print "A & B = %s (algebraic product intersection)" % str(A.intersection(B, fuzz.FuzzySet.NORM_ALGEBRAIC))
print "A & B = %s (bounded difference intersection)" % str(A.intersection(B, fuzz.FuzzySet.NORM_BOUNDED))
print "A & B = %s (drastic intersection)" % str(A.intersection(B, fuzz.FuzzySet.NORM_DRASTIC))

# Of course, this can be done in-place.
A |= B
print "After annexing B, A = %s" % str(A)
if A > B:
    print "A is now a superset of B."

# We can check if a fuzzy set is normalized...
if A.normal:
    print "A is normal."
if B.normal:
    print "B is normal."

# ...and we can normalize a fuzzy set.
B.normalize()
print "After normalization, B = %s (with height %f)." % (str(B), B.height)
if not B < A:
    print "B is no longer a subset of A."

# We can prune zero-valued objects from the set.
print "Before pruning, B has keys %s." % str(B.keys())
B.prune()
print "After pruning, B has keys %s." % str(B.keys())