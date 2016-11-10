package sample.pckg;

import static java.lang.System.out;

import java.io.Serializable;
import java.util.function.Function;

public class SampleClass implements Serializable {
	
	private static final long serialVersionUID = 747474L;
	
	protected static final int value1 = 123;
	static final double value2;
	final int value3;
	int value4;
	int[] value5 = new int[10];
	
	static {
		value2 = 0.987;
	}

	public static void main(String[] args) {
		final SampleClass sc = new SampleClass(100);
		out.println(sc.apply(x -> x*2));
	}
	
	public SampleClass() {
		out.println("Default constructor");
		value3 = 12;
	}
	
	public SampleClass(int k) {
		this();
		value4 = k;
	}
	
	public int apply(Function<Integer, Integer> f) {
		return f.apply(value4);
	}

}
