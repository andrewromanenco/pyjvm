package bytecode;

public class ArraysTest {


    public static void main(String args[]) {
        int result = 0;

        
        int[] iArray = new int[] {0,1,2};
        iArray[0] = 9;
        if (iArray[0] == 9) {
            result++; //1
        }
        try {
            iArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//2
        }
        try {
            iArray[99] = 9;
        } catch (ArrayIndexOutOfBoundsException e) {
            iArray = null;
            result++;//3
        }
        try {
            iArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//4
        }

        char[] cArray = new char[] {'a', 'b', 'c'};
        cArray[0] = 'd';
        if (cArray[0] == 'd') {
            result++; //5
        }
        try {
            cArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//6
        }
        try {
            cArray[99] = 'x';
        } catch (ArrayIndexOutOfBoundsException e) {
            cArray = null;
            result++;//7
        }
        try {
            cArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//8
        }

        byte[] bArray = new byte[] {1, 2, 3, 4};
        bArray[0] = 99;
        if (bArray[0] == 99) {
            result++; //9
        }
        try {
            bArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//10
        }
        try {
            bArray[99] = 99;
        } catch (ArrayIndexOutOfBoundsException e) {
            bArray = null;
            result++;//11
        }
        try {
            bArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//12
        }

        short[] sArray = new short[] {1, 2, 3, 4};
        sArray[0] = 99;
        if (sArray[0] == 99) {
            result++; //13
        }
        try {
            sArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//14
        }
        try {
            sArray[99] = 99;
        } catch (ArrayIndexOutOfBoundsException e) {
            sArray = null;
            result++;//15
        }
        try {
            sArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//16
        }

        long[] lArray = new long[] {1, 2, 3, 4};
        lArray[0] = 99;
        if (lArray[0] == 99) {
            result++; //17
        }
        try {
            lArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//18
        }
        try {
            lArray[99] = 99;
        } catch (ArrayIndexOutOfBoundsException e) {
            lArray = null;
            result++;//19
        }
        try {
            lArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//20
        }

        float[] fArray = new float[] {1, 2, 3, 4};
        fArray[0] = 99;
        if (fArray[0] == 99) {
            result++; //21
        }
        try {
            fArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//22
        }
        try {
            fArray[99] = 99;
        } catch (ArrayIndexOutOfBoundsException e) {
            fArray = null;
            result++;//23
        }
        try {
            fArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//24
        }

        double[] dArray = new double[] {1, 2, 3, 4};
        dArray[0] = 99;
        if (dArray[0] == 99) {
            result++; //25
        }
        try {
            dArray[99]++;
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//26
        }
        try {
            dArray[99] = 99;
        } catch (ArrayIndexOutOfBoundsException e) {
            dArray = null;
            result++;//27
        }
        try {
            dArray[0] = 9;
        } catch (NullPointerException e) {
            result++;//28
        }

        boolean[] bbbArray = new boolean[] {true, true};
        bbbArray[0] = false;
        if (bbbArray[0] == false) {
            result++; //29
        }
        try {
            bbbArray[99] = !bbbArray[100];
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//30
        }
        try {
            bbbArray[99] = true;
        } catch (ArrayIndexOutOfBoundsException e) {
            bbbArray = null;
            result++;//31
        }
        try {
            bbbArray[0] = true;
        } catch (NullPointerException e) {
            result++;//32
        }

        Object[] oArray = new Object[] {null, null};
        Object o = new Object();
        oArray[0] = o;
        if (oArray[0] == o) {
            result++; //33
        }
        try {
            if (oArray[99] == null) {
                oArray[199] = null;
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            result++;//34
        }
        try {
            oArray[99] = null;
        } catch (ArrayIndexOutOfBoundsException e) {
            oArray = null;
            result++;//35
        }
        try {
            oArray[0] = null;
        } catch (NullPointerException e) {
            result++;//36
        }

        System.out.println("Expected/Result: [ARRAYSTEST:36/" + result + "]");
    }

}