import getopt
import sys
import config
import set_factory
import string

set_type = config.set_type
prog_name = config.prog_name
DEFAULT_DICT_FILE = config.DEFAULT_DICT_FILE

# reading words from a file **************************************************/

WORD_SIZE = 50
line_count = 0
first_word_on_line = True

def init_get_next_lower_word():
    global line_count
    line_count = 0
    global first_word_on_line
    first_word_on_line = True

def get_next_lower_word(source):
    # reads next word from source.
    # A word consists of a sequence of alphabetic characters.
    # Returns the word, or NULL if no further words can be found.
    # Converts upper-case letters to lower-case.
    #
    word = ''
    done= False
    word_len= 0;
    global first_word_on_line
    global line_count
    global WORD_SIZE
    # on seeing a '\n', need to increment line_count at the *next* word,
    # even if the '\n' terminated *this* word,
    # so that line-numbers are reported correctly
    while (not done):
        ch = source.read(1)
        if(word_len >= WORD_SIZE):
            max_word_size = WORD_SIZE - 1
            sys.stderr.write("Cannot handle words longer than %d characters" % max_word_size)
            sys.exit(4);
 
        if not ch:
            break

        if (ch.isalpha()):
            # || ch=='-') ?
            if (first_word_on_line):
                line_count = line_count + 1
                first_word_on_line= False
            word_len = word_len + 1
            word += ch.lower()
        else:
            # non-alphabetic
            if (word_len > 0):
                #// non-alphabetic terminates the word
                # word[word_len]= 0
                done= True
      
            if (ch == '\n'):
                # Can't just add one to line count,
                # since last word on line might be reported
                if (first_word_on_line): # already seen one '\n'
                    line_count = line_count + 1
                first_word_on_line= True
        
    if (word_len):
        return word
        
    else:
        return None


def usage():
    # reports the usage of the program
    sys.stderr.write(
          "Usage: %s [-d dictionary] [-s dict_init_size] [-m mode] [-v] [-h] text_file\n" % prog_name);
    sys.stderr.write("\ts: set initial dictionary size to arg\n");
    sys.stderr.write("\td: dictionary name (default %s)\n" % DEFAULT_DICT_FILE);
    sys.stderr.write("\tv: verbose - extra v's increase reporting level\n");
    sys.stderr.write("\th: help - output this message\n");
    sys.stderr.write("\ttext_file: file to spell-check\n");
    exit(1);

def process_args(args):
    if (len(args) < 1):
        usage ()
    try:
        opts, other_args = getopt.getopt(args, "s:d:m:vh")
    except getopt.GetoptError as err:
        print(err)
        usage()
        
    for o, a in opts:
        if (o == '-s'):
            config.init_size = int(a)
        elif (o == '-d'):
            global dict_file_name
            dict_file_name = a
        elif (o == '-m'):
            config.mode = int(a)
        elif (o == '-v'):
            config.verbose+=1
        elif (o == '-h'):
            usage()
            break
        else:
            # Don't think we ever get here before exception thrown earlier.
            printf ("didn't expect program parameter %c [0%o]\n" % (o, o))
            usage ()
 
 
    if (len(other_args) > 0):
        global file_name
        file_name= other_args[0]
    else:
        # no file  name given
        usage()

def spelling(args):
    word_count = 0

    prog_name = args[0]
    args.pop(0)
    global dict_file_name 
    dict_file_name = DEFAULT_DICT_FILE
    process_args(args)
    
    if (config.verbose > 0):
        sys.stderr.write("Using dictionary `%s'\n" % dict_file_name)
        sys.stderr.write("Checking text file `%s'\n" % file_name)
        sys.stderr.write("Using mode %d\n" % config.mode)
        
    dict_file = open(dict_file_name)
    text_file = open(file_name)
    
    words = set_factory.initialise_set()
    
    if (config.verbose > 0):
        sys.stderr.write("Reading dictionary\n")
        
    init_get_next_lower_word()
    while True:
        word = get_next_lower_word (dict_file)
        if (word == None):
            break
        words.insert(word)
        word_count = word_count + 1
        if ((config.verbose > 0) and (word_count % 100 == 0)):
           sys.stderr.write(".")
           
    if (config.verbose > 0):
        sys.stderr.write("\nDictionary read\n")

    if (config.verbose > 1):
        # call with option -vv to get this
        if (config.verbose > 2):
            # call with option -vvv to get this
            words.print_set()

    print("Spellchecking:\n")

    init_get_next_lower_word ();
    while True:
        word= get_next_lower_word (text_file)
        if (word == None):
            break
        if (not words.find(word)):
            print("%d: %s\n" % (line_count, word));

    print("Usage statistics:\n");
    words.print_stats ()

    # Now tidy everything up
    dict_file.close()
    text_file.close()


        
    

