package io;

import java.io.File;

public class FileExists {

    public static void main(String args[]) {
        if (args.length < 1) {
            System.out.println("Provide command line argument: file_name");
            return;
        }
        String fileName = args[0];
        System.out.println("Processing file: " + fileName);
        File f = new File(fileName);
        if (!f.exists()) {
            System.out.println("File does not exist!");
        } else {
            System.out.println("File exists!");
        }
    }

}