"""\
Creating Sets - this example demonstrates the various ways to create and
populate fuzzy sets.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

import warnings

from common import fuzz

# By default, the constructor will create an empty fuzzy set.
A = fuzz.FuzzySet()

print "A = %s is an empty fuzzy set." % str(A)

# Fuzzy sets are composed of fuzzy elements. The most primordial way to add an
# element to a fuzzy set is to add a FuzzyElement object explicitly.
A.add(fuzz.FuzzyElement('one', 0.5))

# If an object which is not a fuzzy element is added, it will automatically be
# converted to a fuzzy element.
A.add('two')

# It is also possible to add elements in bulk using the update method (just
# like in basic Python sets).
items = [fuzz.FuzzyElement('three', 0.4), fuzz.FuzzyElement('four', 0.1)]
A.update(items)

print "A = %s now has some elements." % str(A)

# Fuzzy elements are composed of two parts: an object and a membership degree
# (or mu value). If the mu argument is left out, it will default to 1.0,
# mimicking a classic set.
e = fuzz.FuzzyElement(42, 0.3)
print "Fuzzy element %s has object %s and mu value %s." % (str(e), str(e.obj),
    str(e.mu))

# Because a fuzzy set is a subclass of IndexedSet, its fuzzy elements must be
# unique in terms of their object. Attempting to add an item with a duplicate
# object will raise a warning (and leave the set unaffected).
warnings.simplefilter('error', fuzz.DuplicateItemWarning)
try:
    A.add(fuzz.FuzzyElement('two', 0.1))
except fuzz.DuplicateItemWarning:
    print "Attempted to add an item with a duplicate object to A."

# Fuzzy elements can be added using a convenience method. Again, if the mu
# argument is left out, it will default to 1.0.
A.add_fuzzy('five', 0.6)

# Elements can be removed explicitly...
try:
    A.remove(fuzz.FuzzyElement('four', 0.3))
except KeyError:
    print "Oops, that won't work."
A.remove(fuzz.FuzzyElement('four', 0.1))

# ...but it's much more convenient in most cases to remove them by object.
A.remove('three')

print "A = %s is changing every day." % str(A)

# We can initialize a fuzzy set with an iterable (this just uses the update
# method under the hood).
B = fuzz.FuzzySet([fuzz.FuzzyElement(1), fuzz.FuzzyElement(2)])

print "B = %s is initialized." % str(B)

# This includes other fuzzy sets.
C = fuzz.FuzzySet(A)

print "C = %s is the same as A." % str(C)
