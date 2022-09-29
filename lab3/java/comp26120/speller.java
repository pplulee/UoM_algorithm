package comp26120;

import comp26120.set;
import comp26120.set_factory;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.lang.Character;
import java.io.FileNotFoundException;


public abstract class speller {
    int word_count = 0;
    String word;
    String prog_name = "speller";
    speller_config config;
    int line_count = 0;
    boolean first_word_on_line = true;
    static int WORD_SIZE = 50;

    public speller () {
	config = new speller_config();
    }

    public int verbose() {
	return config.verbose;
    }

    public String dict_file_name() {
	return config.dict_file_name;
    }

    public String file_name() {
	return config.file_name;
    }

    public int mode() {
	return config.mode;
    }

    public abstract set_factory.SetType data_structure();

    public String get_next_lower_word(BufferedReader source) 
    {
	/* reads next word from source.
	 * A word consists of a sequence of alphabetic characters.
	 * Returns the word, or NULL if no further words can be found.
	 * Converts upper-case letters to lower-case.
	 */
	char[] word = new char[WORD_SIZE];
	char ch;
	int c;
	boolean done= false;
	int word_len= 0;
     	// on seeing a '\n', need to increment line_count at the *next* word,
	// even if the '\n' terminated *this* word,
	// so that line-numbers are reported correctly
	try {
	    while (!done && ((c = source.read()) != -1))
		{
		    ch = (char) c;
		    if(word_len >= WORD_SIZE){
			System.err.format("Cannot handle words longer than %d characters",
					  WORD_SIZE-1);
			System.exit(4);
		    }
		    if (Character.isLetter(ch)) 
			{   // || ch=='-') ?  
			    if (this.first_word_on_line) 
				{
				    this.line_count++; this.first_word_on_line= false;
				}
			    word[word_len++]= Character.toLowerCase(ch);
			}
		    else 
			{ // non-alphabetic
			    if (word_len > 0) 
				{ // non-alphabetic terminates the word
				    word[word_len]= 0;
				    done= true ;
				}
			    if (ch == '\n') 
				{ // Can't just add one to line count,
				    // since last word on line might be reported
				    if (this.first_word_on_line) // already seen one '\n'         
					{  
					    this.line_count++;
					}
				    this.first_word_on_line= true;
				}
			}
		} //while
	} catch (IOException e) {
		return null;
	}
	if (word_len > 0)
	    {
		return new String(word,0,word_len);
	    }
	else
	    {
		return null;
	    }
    }


    public static void spelling(speller speller, String[] args) {
        speller.process_args(args);
        
	if (speller.verbose() > 0) {
            System.err.format("Using dictionary `%s'\n", speller.dict_file_name());
            System.err.format("Checking text file `%s'\n", speller.file_name());
            System.err.format("Using mode %d\n", speller.mode());
        }

	try {
	    FileReader dict_file = new FileReader(speller.dict_file_name());
	    BufferedReader dict_scanner = new BufferedReader(dict_file);

	    try {
		FileReader text_file = new FileReader(speller.file_name());
		BufferedReader text_scanner = new BufferedReader(text_file);
	
		set_factory set_factory = new set_factory(speller.data_structure(), speller.config);
        
		set<String> words = set_factory.initialise_set();
        
		if (speller.config.verbose > 0) {
		    System.err.println("Reading dictionary\n");
		}

		boolean done = false;
		while (!done) {
		    speller.word = speller.get_next_lower_word(dict_scanner);
		    if (speller.word == null) {
			done = true;
		    } else {
			words.insert(speller.word);
			speller.word_count++;
			if ((speller.verbose() > 0) && (speller.word_count % 100 == 0)) {
			    System.err.println(".");
			} 
		    }
		}

		if (speller.verbose() > 0) {
		    System.err.println("\nDictionary read\n");
		}
        
		if (speller.verbose() > 1) {
		    // call with option -vv to get this
		    if (speller.verbose() > 2) {
			// call with optin -vvv to get this
			words.print_set();
		    }
		}
		System.out.println("Spellchecking:\n");

		done = false;
		speller.line_count = 0;
		while (!done) {
		    speller.word = speller.get_next_lower_word(text_scanner);
		    if (speller.word == null) {
			done = true;
		    } else {
			String word_string = new String(speller.word);
			if (!words.find(word_string)) {
			    System.out.format("%d: %s\n", speller.line_count, word_string);
			}
		    }
		}
        
		System.out.println("Usage statistics:\n");
		words.print_stats();
        
		//Now tidy everything up
		dict_scanner.close();
		text_scanner.close();
	    } catch (FileNotFoundException e) {
		System.err.format("%s: Can't find %s \n", speller.prog_name, speller.file_name());
		System.exit(3);
	    } catch (Exception e) {
		System.err.format("%s: Error \n", speller.prog_name);
		e.printStackTrace();
		System.exit(3);
	    }
	} catch (FileNotFoundException e) {
	    System.err.format("%s: Can't find %s\n", speller.prog_name, speller.dict_file_name());
	    System.exit(3);
	} catch (Exception e) {
	    System.err.format("%s: Error \n", speller.prog_name);
	    e.printStackTrace();
	    System.exit(3);
       }

        
        /* return 0; */
        
    }

    public int process_args(String[] args) {
        if (args.length < 1)
          usage ();

	int index = 0;

        while (index < (args.length - 1))
        {
	    String c= args[index];
	    String optarg;
	    System.out.println(c);

         if (c.equals("-s")) {
	      index++;
	      optarg = args[index];
              config.init_size= Integer.parseInt(optarg);
	      index++;
	 } else if (c.equals("-d")) { // dictionary name given
	      index++;
              optarg = args[index];
              config.dict_file_name= optarg;
	      index++;
	 } else if (c.equals("-m")) {  // algorithm mode given
	      index++;
              optarg = args[index];
              config.mode= Integer.parseInt(optarg);
	      index++;
	 } else if (c.equals("-v")) {  
	      index++;
	      config.verbose++; 
	 } else if (c.equals("-vv")) {  
	      index++;
	      config.verbose++; 
	      config.verbose++; 
	 } else if (c.equals("-vvv")) {  
	      index++;
	      config.verbose++; 
	      config.verbose++; 
	      config.verbose++; 
	 } else if (c.equals("-h")) {  // Help!
	      usage ();
	 } else { // report error
	     System.out.println("Didn't expect argument:");
	     System.out.println(args[index]);
	     usage();
	     break;
          }
        }
        /* All being well we've only the file name left.
           We'll ignore any other args
         */
        if (index < args.length)
        {
          config.file_name= args[index];
        }
        else
            { // no file name given
              usage();
            }
            return (0);
    }

    public void usage() {
	System.err.format("Usage: %s [-d dictionary] [-s dict_init_size] [-m mode] [-v] [-h] text_file\n", prog_name);
	System.err.format("\ts: set initial dictionary size to arg\n");
	System.err.format("\td: dictionary name (default %s)\n", config.dict_file_name);
	System.err.format("\tv: verbose - extra v's increase reporting level\n");
	System.err.format("\th: help - output this message\n");
	System.err.format("\ttext_file: file to spell-check\n");
	System.exit(1);
    }
    
}
