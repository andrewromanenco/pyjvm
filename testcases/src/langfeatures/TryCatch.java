package langfeatures;

public class TryCatch {

    public static void main(String[] args) {
        System.out.println("Test same frame");
        int a = 100;
        int b = 0;
        try {
            int c = a / b;
            System.out.println("c = " + c);
        } catch (ArithmeticException e) {
            System.out.println("Handled ArithException");
        } catch (Exception e) {
            System.out.println("Should not be called");
        }

        System.out.println("Test diff frames");
        A o = new A();
        try {
            o.action();
        } catch (ArithmeticException e) {
            System.out.println("Handled ArithException");
        } catch (Exception e) {
            System.out.println("Should not be called");
        }

        System.out.println("Test catch with finally");
        try {
            o.action();
        } catch (ArithmeticException e) {
            System.out.println("Handled ArithException with finally");
        } catch (Exception e) {
            System.out.println("Should not be called");
        } finally {
            System.out.println("Finally after catch");
        }

        System.out.println("Test with finally only");
        try {
            o.action();
        } finally {
            System.out.println("Finally only catch");
        }

        System.out.println("Will never get called");
    }

    static class A {

        public int action() {
            B b = new B();
            int i = b.action(100, 0);
            return i + 10;
        }

    }

    static class B {

        public int action(int x, int y) {
            return x / y;
        }

    }

}