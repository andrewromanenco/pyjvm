package langfeatures;

public class ThreadsDaemons {
    
    public static void main(String[] args) {
        T t1 = new T();
        T t2 = new T();
        t1.p = 1000;
        t2.p = 4000;
        t2.setDaemon(true);
        t1.start();
        t2.start();
        System.out.println("Done with main");
    }
    
    static class T extends Thread {

        int p = 0;

        public void run() {
            for (int i = 0; i < 10; i ++) {
                System.out.println("From " + p + " daemon " + i);
                try {
                    Thread.sleep(p);
                } catch (Exception e) {
                    // nothing
                }
            }
        }

    }
}
