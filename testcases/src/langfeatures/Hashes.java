package langfeatures;

public class Hashes {

    public static void main(String args[]) {
        int score = 0;

        Object o = new Object();
        String s = new String("This is string");

        int a;
        int b;

        a = o.hashCode();
        b = System.identityHashCode(o);
        System.out.println("hash/system " + a + "/" + b);

        if (a == b) score++;

        a = s.hashCode();
        b = System.identityHashCode(s);
        System.out.println("hash/system " + a + "/" + b);
        if (a == b) score++;

        System.out.println("[HASHES:2/" + score + "]");
    }

}