package langfeatures;

public class InnerClazz {

    private int i = 999;

    public static void main(String args[]) {
        InnerClazz o = new InnerClazz();
        Inn inn = o.new Inn();
        inn.action();
        System.out.println("After: " + o.i);
        int score = 0;
        if (o.i == 111) {
            score++;
        }
        System.out.println("[INNERCLAZZ:1/" + score + "]");
    }

    class Inn {

        void action() {
            System.out.println("i = " + i);
            i = 111;
        }

    }

}