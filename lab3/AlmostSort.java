/**
 * Uses Bubble Sort to 'almost' sort a file. The idea is to perform sorting for a reduced number of
 * operations. The program takes a file name for the file to be sorted and a divisor d such that we
 * perform n/d iterations instead of n.
 *
 * A d value of 10 seems to work okay for large files. 
 *
 * If your input is already sorted or almost sorted then bubble sort might finish before the reduced
 * number of iterations that you specify.
 *
 * We're still O(n^2) so be patient for large files.
 *
 * Giles Reger, 2020
 */
import java.lang.RuntimeException;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;


public class AlmostSort {

   public static void main(String[] args) throws FileNotFoundException
    {
        if(args.length != 2){ throw new RuntimeException("Give me exactly one input file and one divisor"); }
        Scanner sc = new Scanner(new File(args[0]));
        int divisor = Integer.parseInt(args[1]);
        ArrayList<String> lines = new ArrayList<String>();
        while (sc.hasNextLine()) {
            lines.add(sc.nextLine());
        }
        bubbleSort(lines,lines.size()/divisor);
        for(String s : lines){ System.out.println(s); }
    }

    static void bubbleSort(ArrayList<String> arr, int iterations) 
    { 
        if(iterations > arr.size() - 1){
          throw new RuntimeException("Iterations cannot be larger than array (-1)");
        } 
        boolean swapped; 
        for (int i = 0; i < iterations; i++)  
        { 
            swapped = false; 
            for (int j = 0; j < arr.size() - i - 1; j++)  
            { 
                if (arr.get(j + 1).compareTo(arr.get(j)) < 0)  
                { 
                    // swap arr[j] and arr[j+1] 
                    String temp = arr.get(j); 
                    arr.set(j, arr.get(j + 1)); 
                    arr.set(j + 1, temp); 
                    swapped = true; 
                } 
            } 
  
            if (!swapped) 
                break; 
        } 
    } 
}
