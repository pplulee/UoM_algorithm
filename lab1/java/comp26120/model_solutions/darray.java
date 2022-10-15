package comp26120;

import java.util.ArrayList;

public class darray implements set<String> {
    private ArrayList<String> list = new ArrayList<String>();
    private boolean sorted = false;

    SearchModes mode;
    int verbose;

    public darray(speller_config config) {
	mode = SearchModes.getSearchMode(config.mode);
	verbose = config.verbose;
    }
    
    public void insert(String value) {
        list.add(value);
        
        // changing the array means it may no longer be sorted
        sorted = false;
    }
    
    public boolean find(String value) {
        if (mode == SearchModes.LINEAR_SEARCH) {
	    for(int i=0;i<list.size();i++){
		if(value.equals(list.get(i))){
		    return true;
		}
	    }
	    return false;
        } else { //Binary Search
            if (! sorted) {
                if (verbose > 0) {
                    System.out.println("Dynamic Array not sorted, sorting... \n");
                }
                
                sort(mode);
                if (verbose > 0) {
                    System.out.println("Dynamic Array sorted\n");
                }
                
                sorted = true;
            }
	    int first = 0;
	    int last = list.size() - 1;
	    int middle = (first+last)/2;

	    while(first <= last){
		int search = list.get(middle).compareTo(value);
		if(search < 0){
		    first = middle+1;
		}
		else if(search == 0){
		    return true;
		}
		else{
		    last = middle - 1;
		}
		middle = (first + last)/2;
	    }
	}
	return false;
    }
    
    public void print_set ()
    {
	System.out.print("DArray:\n");
	for(int i=0;i<list.size();i++){
	    System.out.format("\t%s\n",list.get(i));
	}
    }

    public void print_stats()
    {
	System.out.format("Dynamic array contains %d elements\n",list.size());
    }



    // Sorting Methods

    public enum SearchModes   { LINEAR_SEARCH,  // =0 in mode flag 
				BINARY_SEARCH_ONE,  // = 1
				BINARY_SEARCH_TWO, // = 2
				BINARY_SEARCH_THREE, // =3
				BINARY_SEARCH_FOUR, // = 4
				BINARY_SEARCH_FIVE; // =5

	public static SearchModes getSearchMode(int i) {
	    switch (i) {
	    case 1:
		return BINARY_SEARCH_ONE;
	    case 2:
		return BINARY_SEARCH_TWO;
	    case 3:
		return BINARY_SEARCH_THREE;
	    case 4:
		return BINARY_SEARCH_FOUR;
	    case 5:
		return BINARY_SEARCH_FIVE;
	    default:
		return LINEAR_SEARCH;
		
	    }
	}
 };

    private void sort(SearchModes select){

	switch(select){
	case BINARY_SEARCH_ONE   : insertion_sort(); break;
	case BINARY_SEARCH_TWO   : quick_sort(); break;
	case BINARY_SEARCH_THREE :
	case BINARY_SEARCH_FOUR  :
	case BINARY_SEARCH_FIVE  :  // Add your own choices here
	default: 
	    System.err.format("The value %d is not supported in sorting.c\n",
              select);
	    // Keep this exit code as the tests treat 23 specially
	    System.exit(23);
	}
    }


    // You may find this helpful
    private void swap(int a, int b)
    {
        String temp = list.get(a);
        list.set(a, list.get(b));
        list.set(b, temp);
    }


    private void insertion_sort(){
        int n = list.size();
        int i, j;
        String key;
        for (i = 1; i < n; i++)
        {
	    key = list.get(i);
            j = i-1;
            while (j >= 0 && list.get(j).compareTo(key)>0)
                {
		    list.set(j+1, list.get(j));
                    j = j-1;
                }
	    list.set(j+1, key);
        }

    }


    private void quick_sort_recursive(int start, int end) {
        if (start >= end)
                return;
        String mid = list.get(end);
        int left = start, right = end - 1;
        while (left < right) {
	    while (list.get(left).compareTo(mid) < 0 && left < right)
                        left++;
	    while (list.get(right).compareTo(mid) >= 0 && left < right)
                        right--;
            swap(left, right);
        }
        if (list.get(left).compareTo(list.get(end)) >=0)
	    swap(left, end);
        else
            left++;
	
        if (left != 0)
            quick_sort_recursive(start, left - 1);
        quick_sort_recursive(left + 1, end);
    }

    private void quick_sort() {

	quick_sort_recursive(0, list.size() - 1);
    }

    private void bucket_sort() { System.exit(-1);}
    private void merge_sort() { System.exit(-1); }


}
