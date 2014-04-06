package sorts;

public class QuickSort {

    public void sort(int[] array) {
        sort(array, 0, array.length  - 1);
    }

    private void sort(int[] array, int start, int end) {
        if ((end - start) < 1) {
            return;
        }
        int pivot = array[end];
        int index = start;
        for (int i = start; i < end; i++) {
            if (array[i] < pivot) {
                int tmp = array[i];
                array[i] = array[index];
                array[index] = tmp;
                index++;
            }
        }
        array[end] = array[index];
        array[index] = pivot;
        sort(array, start, index - 1);
        sort(array, index + 1, end);
    }

	public static void main(String args[]) {
		int arr[] = new int[]{5,2,4,1,3};
		QuickSort qs = new QuickSort();
		System.out.println(java.util.Arrays.toString(arr));
		qs.sort(arr);
		System.out.println(java.util.Arrays.toString(arr));
	}

}
