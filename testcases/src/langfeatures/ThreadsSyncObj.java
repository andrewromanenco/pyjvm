package langfeatures;

public class ThreadsSyncObj implements Runnable {
    
    private String name;
    private int base;
    private int pause;
    private Locker locker;

    public static void main(String[] args) {
        ThreadsSyncObj t1 = new ThreadsSyncObj("first");
        ThreadsSyncObj t2 = new ThreadsSyncObj("second");

        Locker l = new Locker();
        t1.locker = l;
        t2.locker = l;

        t1.base = 100;
        t2.base = -100;

        t1.pause = 1000;
        t2.pause = 2000;
        
        Thread tt1 = new Thread(t1);
        Thread tt2 = new Thread(t2);
        
        System.out.println("About to start two threads");

        tt1.start();
        tt2.start();
        
        try {
            tt1.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        try {
            tt2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Done");
    }
    
    ThreadsSyncObj(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            int b = base++;
            int r = locker.method(b);
            System.out.println(name + " base: " + b + " =*10: " + r);
            try {
                Thread.sleep(pause);
            } catch (Exception e) {
                //nothing
            }
        }
    }

    static class Locker {

        static int value;

        synchronized int method(int v) {
            value = v;
            try {
                Thread.sleep(2000);
            } catch (Exception e) {
                //nothing
            }
            return value * 10;
        }

    }

}
