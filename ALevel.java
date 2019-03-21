/*
Code to be syntax-checked for A-level Midterm project grade
*/

import java.io.*;
import java.util.Scanner;
//more than one import statement!

class ALevel{

    public static void main (String [] args){
        //now we are in main
        Scanner sc = new Scanner(System.in);
        System.out.println("What is your name?");
        String newString = sc.next();
        System.out.println("How old are you?");
        int newInt = sc.nextInt();
        
        
        int x = 5;
        String stringtrue = "String";
        System.out.println("It is true that string has 6 letters");
        boolean t = false;
        x = x + 3;
        if (x < 10){
            System.out.println("x<10");
        }
        else{
            System.out.println("x>=10");
        }
        
        while(x <= 20){
          System.out.println("the number is" + x);
          x = x + 1;
        }
        
        
        

        Person you = new Person(newInt, newString);
        you.printInfo();
        /*
        If there are other things that you want to test,
        here is a good place for them.
        */

    }

}

class Person{
    
    int age;
    String name;
    
    public Person(int a, String n){
        age = a;
        name = n;
    }
    
    public void printInfo(){
        System.out.println("Your name is " + name + " and you are " + age + " years old.");
    }

}