package langfeatures;

public class PrintOut {

    public static void main(String args[]) {
        (new PrintOut()).printAll();
    }

    void printAll() {
        String s = "This is string";
        int iVal = 100;
        long lVal = 999;
        Object o = null;
        Object o2 = new Object();
        float fVal = 0.56f;
        double dVal = -98.56;
        boolean yes = true;
        boolean no = false;
        char c = 'X';
        short sVal = 50;
        byte bVal = 8;

        System.out.println("String = " + s);
        System.out.println("int = " + iVal);
        System.out.println("long = " + lVal);
        System.out.println("o(null) = " + o);
        System.out.println("o2(not null) = " + o2);
        //System.out.println("float = " + fVal);
        //System.out.println("double = " + dVal);
        System.out.println("yes = " + yes);
        System.out.println("no = " + no);
        System.out.println("char = " + c);
        System.out.println("short = " + sVal);
        System.out.println("byte = " + bVal);
    }

}