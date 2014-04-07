package io;

import java.io.*;

public class FilePrint {

    public static void main(String args[]) throws Exception {
        String fileName = "resources/file2read.txt";
        System.out.println("Processing file: " + fileName);
        File file = new File(fileName);
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }
        br.close();
    }

}