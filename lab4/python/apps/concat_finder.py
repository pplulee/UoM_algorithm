import sys

def tidy_up(pq):
    while(not pq.is_empty()):
        pq.pop_min()
        
def concat_finder(args, initialize_pq):
    prog_name = args.pop(0)
    
    pq = initialize_pq(1000)
    
    search = input()
    sys.stdout.write("Searching for %s\n" % search)
    
    n_string = input()
    n = int(n_string)
    
    for i in range(n):
        tmp = input()
        if (tmp == search):
            print("Found\n")
            tidy_up(pq)
        if (len(tmp) < len(search)):
            pq.insert(tmp, len(tmp))
            
    pq.print()
    
    done = initialize_pq(1000)
     
    while (not pq.is_empty()):
        next = pq.pop_min()
        sys.stdout.write("Pop %s\n" % next)
        rebuild = initialize_pq(1000)
        while (not done.is_empty()):
            s = done.pop_min()
            rebuild.insert(s, len(s))
            # sys.stdout.write("Try with %s\n" % s)
            if (len(s) + len(next) <= len(search)):
                left = next + s
                right = s + next
                if (left == search or right == search):
                    print("Found")
                    tidy_up(pq)
                    tidy_up(done)
                    tidy_up(rebuild)
                    return 0
                pq.insert(left, len(left))
                pq.insert(right, len(right))
        # Can remove conditional if PriorityQueue does not contain duplicates
        # sys.stdout.write("Done with %s\n" % next)
        if (not rebuild.contains(next, len(next))):
            # sys.stdout.write("Using %s\n" & next)
            rebuild.insert(next, len(next))
        done = rebuild
    
    tidy_up(pq)
    tidy_up(done)
    print("Not Found")
    return 0
    
