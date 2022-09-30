import sys

import general

WEIGHT_MIN = -sys.maxsize
WEIGHT_MAX = sys.maxsize - 1

_WINF = sys.maxsize
_WNINF = -sys.maxsize - 1

#/// Weight and distance type.

#
 # We provide a weight-type, that implements integers with +infinity and -infinity, and provides
 # overflow-checked operations, which fail on underflows or overflows.
 #
 # It is wrapped into a struct, to prevent accidental access to the raw integer.
 #/
class weight_t:
    def __init__(self,w):
        if (w == _WINF or w == _WNINF):
            general.error("Weight overflow")
        self.w = w

    # Check for +infinity
    def weight_is_inf(self):
        return self.w == _WINF

    # Check for -infinity
    def weight_is_neg_inf(self):
        return self.w == _WNINF

    # Check that weight is finite, i.e., not +inf nor -inf
    def weight_is_finite(self):
        return (not self.weight_is_inf() and not self.weight_is_neg_inf())
        
    def weight_to_int(self):
        assert self.weight_is_finite(), "Weight must be finite"
        return self.w
        
    def print_weight(self, f):
        if (self.weight_is_inf()):
            f.write("inf")
        elif (self.weight_is_neg_inf()):
            f.write("-inf")
        else:
            f.write("%d" % (self.weight_to_int()))

# + infinity
class weight_inf(weight_t):
    def __init__(self):
        self.w = _WINF

# -infinity
class weight_neg_inf(weight_t):
    def __init__(self):
        self.w = _WNINF

# Zero weight
def weight_zero():
    return weight_t(0)

##
 # Add weights. Adding to +inf or -inf will n ot change the weight.
 # Adding +inf and -inf is undefined!
 # @pre {a,b} != {+inf,-inf}
 #/
def weight_add(a, b):
    if (a.weight_is_inf()):
        assert (not b.weight_is_neg_inf()), "inf + -inf undefined"
        return weight_inf()
    elif (a.weight_is_neg_inf()):
        assert(not b.weight_is_inf()), "-inf + inf undefined"
        return weight_neg_inf()
    elif (b.weight_is_inf()):
        return weight_inf()
    elif (b.weight_is_neg_inf()):
        return weight_neg_inf()
    else:
        res = a.w + b.w
        return weight_t(res)

##
 # Subtract weights.
 #
 #    a     b     result
 #    ----------------
 #    inf   inf   undef
 #    inf   *     inf
 #    -inf  -inf  unfef
 #    -inf  *     -inf
 #    fin   inf   -inf
 #    fin   -inf  inf
 #
 #/
def weight_sub(a, b):
    if (a.weight_is_inf()):
        assert (not b.weight_is_inf()), "inf - inf undefined"
        return weight_inf()
    elif (a.weight_is_neg_inf()):
        assert (not b.weight_is_neg_inf()), "-inf - -inf undefined"
        return weight_neg_inf()
    elif (b.weight_is_inf()):
        return weight_neg_inf()
    elif (b.weight_is_neg_inf()):
        return weight_inf()
    else:
        res = a.w - b.w
        return weight_t(res)

# Compare <
def weight_less(a, b):
    return a.w < b.w

# Compare ==
def weight_eq(a, b):
    return a.w == b.w
    
