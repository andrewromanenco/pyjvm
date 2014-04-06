package sorts;

public class BubbleSort {

    public int[] sort(int[] array) {
        boolean bubbled = true;
        while (bubbled) {
            bubbled = false;
            for (int i = 0; i < array.length - 1; i++) {
                if (array[i] > array[i+1]) {
                    int value = array[i];
                    array[i] = array[i+1];
                    array[i+1] = value;
                    bubbled = true;
                }
            }
        }
        return array;
    }

    public static void main(String args[]) {
        BubbleSort bs = new BubbleSort();
        System.out.println(java.util.Arrays.toString(bs.sort(new int[]{5,3,4,1,2})));
    }
    
}