package langfeatures;

public class Threads implements Runnable {
    
    private String name;

    public static void main(String[] args) {
        Threads t1 = new Threads("first");
        Threads t2 = new Threads("second");
        
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
    
    Threads(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.print(name + " - " + i + "\n");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
