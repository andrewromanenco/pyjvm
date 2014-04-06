package bytecode;

public class CalcsTest {

    public static void main(String args[]) {
        int result = 0;

        int iA, iB, iR;

        iA = 23;
        iB = 47;
        iR = iA + iB;
        if (iR == 70) result++;

        iA = Integer.MAX_VALUE - 5;
        iB = 1000;
        iR = iA + iB;
        if (iR == -2147482654) result++;

        iA = 23;
        iB = 47;
        iR = iA - iB;
        if (iR == -24) result++;

        iA = Integer.MAX_VALUE - 5;
        iB = -1000;
        iR = iB - iA;
        if (iR == 2147482654) result++;

        iA = Integer.MAX_VALUE;
        iB = Integer.MIN_VALUE;
        iR = iA * iB;
        if (iR == -2147483648) result++;
        System.out.println(iR);

        iA = 23;
        iB = 47;
        iR = iA * iB;
        if (iR == 1081) result++;

        iA = Integer.MAX_VALUE - 5;
        iB = 1000;
        iR = iA * iB;
        if (iR == -6000) result++;

        iA = 23;
        iB = 47;
        iR = iA / iB;
        if (iR == 0) result++;

        iA = 50;
        iB = 5;
        iR = iA / iB;
        if (iR == 10) result++;

        iA = 54;
        iB = 5;
        iR = iA / iB;
        if (iR == 10) result++;

        iA = -51;
        iB = 5;
        iR = iA / iB;
        if (iR == -10) result++;

        iA = Integer.MIN_VALUE;
        iB = 1000;
        iR = iA / iB;
        if (iR == -2147483) result++;

        iA = -1999;
        iR = - iA;
        if (iR == 1999) result++;

        iA = Integer.MIN_VALUE;
        iR = - iA;
        if (iR == -2147483648) result++;

        iA = Integer.MAX_VALUE;
        iR = - iA;
        if (iR == -2147483647) result++;
        
        //long
        long lA, lB, lR;

        lA = 23;
        lB = 47;
        lR = lA + lB;
        if (lR == 70) result++;
        System.out.println(lR);

        lA = Long.MAX_VALUE - 5;
        lB = 1000;
        lR = lA + lB;
        if (lR == -9223372036854774814L) result++;
        System.out.println(lR);

        lA = Long.MAX_VALUE;
        lB = Long.MAX_VALUE;
        lR = lA + lB;
        if (lR == -9223372036854774814L) result++;
        System.out.println(lR);

        lA = 23;
        lB = 47;
        lR = lA - lB;
        if (lR == -24) result++;
        System.out.println("x" + lR);

        lA = Long.MAX_VALUE - 5;
        lB = -1000;
        lR = lB - lA;
        if (lR == 9223372036854774814L) result++;
        System.out.println(lR);

        lA = 23;
        lB = 47;
        lR = lA * lB;
        if (lR == 1081) result++;
        System.out.println(lR);

        lA = Long.MAX_VALUE - 5;
        lB = 1000;
        lR = lA * lB;
        if (lR == -6000) result++;
        System.out.println(lR);

        lA = 23;
        lB = 47;
        lR = lA / lB;
        if (lR == 0) result++;
        System.out.println(lR);

        lA = 50;
        lB = 5;
        lR = lA / lB;
        if (lR == 10) result++;
        System.out.println(lR);

        lA = 54;
        lB = 5;
        lR = lA / lB;
        if (lR == 10) result++;
        System.out.println(lR);

        lA = -51;
        lB = 5;
        lR = lA / lB;
        if (lR == -10) result++;
        System.out.println(lR);

        lA = Long.MIN_VALUE;
        lB = 1000;
        lR = lA / lB;
        if (lR == -9223372036854775L) result++;
        System.out.println(lR);

        lA = -1999;
        lR = - lA;
        if (lR == 1999) result++;
        System.out.println(lR);

        lA = Long.MIN_VALUE;
        lR = - lA;
        if (lR == -9223372036854775808L) result++;
        System.out.println(lR);

        lA = Long.MAX_VALUE;
        lR = - lA;
        if (lR == -9223372036854775807L) result++;
        System.out.println(lR);

        System.out.println("Expected/Result: [CALCSTEST:29/" + result + "]");
    }

}