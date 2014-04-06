package langfeatures;

public class ThreadsSync implements Runnable {
    
    private String name;
    private int base;
    private int pause;

    public static void main(String[] args) {
        ThreadsSync t1 = new ThreadsSync("first");
        ThreadsSync t2 = new ThreadsSync("second");

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
    
    ThreadsSync(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            int b = base++;
            int r = Locker.method(b);
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

        static synchronized int method(int v) {
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
