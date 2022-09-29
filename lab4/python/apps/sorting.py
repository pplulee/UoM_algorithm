import sys

# set to 1 to print debug lines
# ensure this is 0 when submitting
DEBUG = 0

# Let's do some weirdly complicated ranking of works
# based on their first five characters.   You do't need
# to understand this but we're mapping all characters to
# 0-26 and then subdividing the integers into five levels of
# width 27, so every string with a different first five
# characters gets a different ode

def offset(n):
    res = 27
    while (n > 0):
        new_n = res*27
        # Should not happens as n shold be < 6
        if (new_n < res):
            print("OVERFLOW in offset")
            sys.exit(-1)
        res = new_n
        n = n - 1
    return res
    
def get_bucket(c):
    if (c < 65):
        return 0
    if (c > 122):
        return 0
    if (c > 90):
        c = c - 32
    b = (c - 64)
    return b
    
def get_code(str):
    len_s = len(str)
    
    # What  would happen if we just returned len as the code?
    # What impact would this have on the operations we perform
    # on our data structures?
    
    res = 0
    MAX = 5
    end = MAX
    if (len_s <= MAX):
        end = len_s
    for i in range(end - 1, -1, -1):
        c = ord(str[i])
        new = res+(offset((MAX-1)-i)*get_bucket(c))
        # Should not happen as 27^6 < 2^32
        if (new < res):
            print("OVERFLOW in get_code")
            sys.exit(-1)
        res = new
    return res
    
def sorting(args, initialize_pq):
    prog_name = args.pop(0)
        
    n_string = input()
    n = int(n_string)
    pq = initialize_pq(n)
    
    print("INSERTING...")
    for i in range(n):
        # print(i)
        tmp = input()
        p = get_code(tmp)
        if (DEBUG == 1):
            sys.stdout.write("Insert %s with priority %d" % ( tmp, p))
        pq.insert(tmp, p)
        if (DEBUG == 1):
            print("==============")
            pq.print()
            print("==============")
        
    print("POPPING...")
    while(not pq.is_empty()):
        tmp = pq.pop_min()
        print(tmp)
        if (DEBUG == 1):
            print("==============")
            pq.print()
            print("==============")

