package comp26120;

import java.io.OutputStreamWriter;
import java.io.OutputStream;
import java.io.IOException;

/// Weight and distance.

/*
 * We provide a weight-type, that implements integers with +infinity and -infinity, and provides
 * overflow-checked operations, which fail on underflows or overflows.
 *
 * It is wrapped into a struct, to prevent accidental access to the raw integer.
 */
public class weight_t {
    static Long _WINF=Long.MAX_VALUE;
    static Long _WNINF=Long.MIN_VALUE;
    public static Long WEIGHT_MIN = Long.MIN_VALUE + 1;
    public static Long WEIGHT_MAX = Long.MAX_VALUE - 1;
    
    long __w;

    public weight_t() {
    }

    public weight_t(long w) {
	if (w==_WINF || w==_WNINF) {
	    System.err.println("Weight overflow");
	    System.exit(-1);
	}
	__w = w;
    }

    public weight_t(double w) throws Exception {
	this(Math.round(w));
    }

    /// +infinity
    static class weight_inf extends weight_t {
	public weight_inf() {
	    __w = _WINF;
	}
    }

    /// - infinity
    static class weight_neg_inf extends weight_t {
	public weight_neg_inf() {
	    __w = _WNINF;
	}
    }

    /// Zero weight
   static class weight_zero extends weight_t {
	public weight_zero()  {
	    super(0);
	}

   }

    /// Check for +infinity
    public boolean weight_is_inf() {
	return __w == _WINF;
    }

    /// Check for -infinity
    public boolean weight_is_neg_inf() {
	return __w == _WNINF;
    }

    /// Check that weight is finite, i.e., not +inf nor -inf
    public boolean weight_is_finite() {
	return !weight_is_inf() && !weight_is_neg_inf();
    }

    public long weight_to_int() {
	assert (weight_is_finite()) : "Weight must be finite";
	return __w;
    }

    /**
     * Add weights. Adding to +inf or -inf will n ot change the weight.
     * Adding +inf and -inf is undefined!
     * @pre {a,b} != {+inf,-inf}
     */
    public static final weight_t weight_add(weight_t a, weight_t b) {
	if (a.weight_is_inf()) {
	    assert(! b.weight_is_neg_inf()): "inf + -inf undefined";
	    return new weight_inf();
	} else if (a.weight_is_neg_inf()) {
	    assert(! b.weight_is_inf()): "-inf + inf undefined";
	    return new weight_neg_inf();
	} else if (b.weight_is_inf()) {
	    return new weight_inf();
	} else if (b.weight_is_neg_inf()) {
	    return new weight_neg_inf();
	} else{
	    long res = a.__w + b.__w;
	    try {
		weight_t res_w = new weight_t(res);
		return res_w;
	    } catch (Exception e) {
		System.err.println("Sum of weights exceeded int max value");
		System.exit(-1);
	    }
	    return null;
	}
    }

    /**
     * Subtract weights.
     *
     *    a     b     result
     *    ----------------
     *    inf   inf   undef
     *    inf   *     inf
     *    -inf  -inf  unfef
     *    -inf  *     -inf
     *    fin   inf   -inf
     *    fin   -inf  inf
     *
     */
    public weight_t weight_sub(weight_t a, weight_t b) {
	if (a.weight_is_inf()) {
	    assert(! b.weight_is_inf()): "inf -inf undefined";
	    return new weight_inf();
	} else if (a.weight_is_neg_inf()) {
	    assert(! b.weight_is_neg_inf()): "-inf - -inf undefined";
	    return new weight_neg_inf();
	} else if (b.weight_is_inf()) {
	    return new weight_neg_inf();
	} else if (b.weight_is_neg_inf()) {
	    return new weight_inf();
	} else{
	    long res = a.__w - b.__w;
	    try {
		weight_t res_w = new weight_t(res);
		return res_w;
	    } catch (Exception e) {
		System.err.println("Sub of weights exceeded int max value");
		System.exit(-1);
	    }
	    return null;
	}
    }

    /// Compare <
    public static boolean weight_less(weight_t a, weight_t b) {
	return a.__w < b.__w;
    }

    /// Compare ==
    public static boolean weight_eq(weight_t a, weight_t b) {
	return a.__w == b.__w;
    }

    public void print_weight(OutputStreamWriter writer) {
	try {
	    if (weight_is_inf()) {
		writer.write("inf");
	    } else if (weight_is_neg_inf()) {
		writer.write("-inf");
	    } else {
		String s = String.format("%d", weight_to_int());
		writer.write(s);
	    }
	    // writer.close();
	} catch (IOException e) {
	    System.err.println("Error Message: " + e.getMessage());
	    System.exit(-1);
	}
    }

    public void print_weight() {
	if (weight_is_inf()) {
	    System.err.println("inf");
	} else if (weight_is_neg_inf()) {
	    System.err.println("-inf");
	} else {
	    String s = String.format("%d", weight_to_int());
	    System.err.println(s);
	}
    }


}
