import sys

def check_result(testno, expected, found):
    if (found == None):
        sys.stderr.write("Test %d Failed when %s expected and NULL found\n" % (testno,expected))
        exit(-1)

    if (not (expected == found)):
        sys.stderr.write("Test %d Failed when %s expected and %s found\n" % (testno,expected,found))
        exit(-1)
        
def assert_reason(testno, value, reason):
    if (not value):
        sys.stderr.write("Test %d Failed as %s\n" % (testno,reason))
        exit(-1)
        
def run_test0(initialize_pq):
    print("TEST 0")
    queue = initialize_pq(10)
    print("Initialised...")
    queue.insert("hello",1)
    print("Inserted hello with priority 1...")
    queue.insert("goodbye",2)
    print("Inserted goodbye with priority 2...")
    check_result(0,"hello",queue.pop_min())
    print("Popped hello...")
    check_result(0,"goodbye",queue.pop_min())
    print("Popped goodbye...")
    assert_reason(0,queue.is_empty()," queue is meant to be empty")
    print("Queue now empty")
    
prog_name=""

def run_tests(args, initialize_pq):
    prog_name = args.pop(0)

    if (len(args) != 1):
        sys.stderr.write("Supply test number\n")
        return -1
    
    test_string = args.pop(0)
    
    if (not test_string.isdigit()):
        sys.stderr.write("Supply test number as an integer\n")
        return -1
        
    test_number = int(test_string)
    
    if (test_number == 0):
        run_test0(initialize_pq)
    # elif (test_number == 1):
    #     run_test1(initialize_pq)
    else:
        sys.stderr.write("Test number %d not recognised\n" % test_number)
    return 0
        
        
