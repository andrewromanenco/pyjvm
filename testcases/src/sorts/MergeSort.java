package sorts;

public class MergeSort {

    public int[] sort(int[] array) {
        if (array.length < 2) return array;
        int middle = array.length >> 1;
        int[] left = new int[middle];
        int right[] = new int[array.length - middle];
        System.arraycopy(array, 0, left, 0, left.length);
        System.arraycopy(array, left.length, right, 0, right.length);
        left = sort(left);
        right = sort(right);
        int[] result = new int[left.length + right.length];
        int leftIndex = 0;
        int rightIndex = 0;
        int index = 0;
        while ((leftIndex < left.length)&&(rightIndex < right.length)) {
            if (left[leftIndex] < right[rightIndex]) {
                result[index++] = left[leftIndex++];
            } else {
                result[index++] = right[rightIndex++];
            }
        }
        for (int i = leftIndex; i < left.length; i++) result[index++] = left[i];
        for (int i = rightIndex; i < right.length; i++) result[index++] = right[i];
        return result;
    }

    public static void main(String args[]) {
        int arr[] = new int[]{5,2,4,1,3};
        MergeSort sorter = new MergeSort();
        System.out.println(java.util.Arrays.toString(arr));
        System.out.println(java.util.Arrays.toString(sorter.sort(arr)));
    }

}