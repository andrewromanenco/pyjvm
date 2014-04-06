package langfeatures;

public class ExCatch {

    public static void main(String args[]) {
        int i = 100;
        ExCatch o = new ExCatch();

        System.out.println("Case 1 (local)");
        try {
            i = o.raiseLocal();
        } catch (LocalException e) {
            System.out.println("Handle local");
            e.printStackTrace();
        } catch (RuntimeException e) {
            System.out.println("Handle runtime");
            e.printStackTrace();
        }

        System.out.println("Case 2 (runtime)");
        try {
            i = o.raiseRE();
        } catch (LocalException e) {
            System.out.println("Handle local");
            e.printStackTrace();
        } catch (RuntimeException e) {
            System.out.println("Handle runtime");
            e.printStackTrace();
        }

        if (System.currentTimeMillis() > 0) {
            o = null;
        }

        System.out.println("Case 3 (NPE)");
        try {
            i = o.raiseRE();
        } catch (LocalException e) {
            System.out.println("Handle local");
            e.printStackTrace();
        } catch (NullPointerException e) {
            System.out.println("Handle NPE");
            e.printStackTrace();
        } catch (RuntimeException e) {
            System.out.println("Handle runtime");
            e.printStackTrace();
        }

        try {
            i = o.raiseRE();
        } finally {
            System.out.println("i = " + i);
        }
    }

    private int raiseRE() {
        if (System.currentTimeMillis() > 0) {
            throw new RuntimeException("this is runtime ex");
        }
        return -9;
    }

    private int raiseLocal() {
        if (System.currentTimeMillis() > 0) {
            throw new LocalException("this is local");
        }
        return -10;
    }

    static class LocalException extends RuntimeException {
        public LocalException(String m) {
            super(m);
        }
    }

}