package sorts;

public class InsertionSort {

    public int[] sort(int[] array) {
        for (int i = 1; i < array.length; i++) {
            int value = array[i];
            int index = i;
            for (int j = i - 1; j >= 0; j--) {
                if (value < array[j])  {
                    array[j+1] = array[j];
                    index = j;
                } else {
                    break;
                }
            }
            array[index] = value;
        }
        return array;
    }

    public static void main(String args[]) {
        int arr[] = new int[]{5,2,4,1,3};
        InsertionSort sorter = new InsertionSort();
        System.out.println(java.util.Arrays.toString(arr));
        System.out.println(java.util.Arrays.toString(sorter.sort(arr)));
    }

}
