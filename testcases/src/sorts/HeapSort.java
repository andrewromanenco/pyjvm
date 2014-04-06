package sorts;

public class HeapSort {

    public void sort(int[] array) {

        for (int i = array.length - 1; i >=0; i--) {
            heapify(array, i, array.length);
        }

        for (int i = 0; i < array.length - 1; i++) {
            swap(array, 0, array.length - 1 - i);
            heapify(array, 0, array.length - 1 - i);
        }

    }

    protected void heapify(int[] array, int i, int length) {
        int left = i*2 + 1;
        int right = i*2 + 2;
        int max = i;
        if ((left < length)&&(array[left] > array[i])) {
            max = left;
        }
        if ((right < length)&&(array[right] > array[max])) {
            max = right;
        }
        if (max != i) {
            swap(array, max, i);
            heapify(array, max, length);
        }
    }

    private int parent(int i) {
        if (i%2 == 0) {
            return (i - 2)/2;
        } else {
            return (i - 1)/2;
        }
    }

    private void swap(int[] array, int i, int j) {
        int tmp = array[i];
        array[i] = array[j];
        array[j] = tmp;
    }

    public static void main(String args[]) {
        int arr[] = new int[]{5,2,4,1,3};
        HeapSort sorter = new HeapSort();
        System.out.println(java.util.Arrays.toString(arr));
        sorter.sort(arr);
        System.out.println(java.util.Arrays.toString(arr));
    }

}