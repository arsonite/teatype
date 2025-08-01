package _debug.test;

import java.io.PrintWriter;

import game.asset.core.Attributes;

import teaType.data.BiPrimitive;

import teaType.util.StreamBuffer;

public class AssetTest_Lethargy {
	public static void main(String[] args) throws Exception {
		StreamBuffer.fixConsole();
		PrintWriter out = new PrintWriter(System.out, true);

		Attributes att = new Attributes();
		Attributes att2 = new Attributes();
		att.random(10);
		att2.random(10);

		out.println("Player:\n-------");
		for(BiPrimitive si : att.getAttributes(true)) {
			out.println(si.getFirst() + ": " + si.getSecond());
		}
		out.println();

		out.println("Enemy:\n------");
		for(BiPrimitive si : att2.getAttributes(true)) {
			out.println(si.getFirst() + ": " + si.getSecond());
		}
		out.println();

		int bcount = 0;
		int ecount = 0;
		for(int i = 1; i < 100; i++) {
			if(i % att.getLethargy() == 0 && i % att2.getLethargy() == 0) {
				System.err.print("Both hit their lethargy! Let's roll: ");
				double random = Math.random();
				out.print(random);
				out.flush();
				if(random < 0.5) {
					out.println("! It's Burak's turn! " + i);
					bcount++;
				} else {
					out.println("! It's Enemy's turn! " + i);
					ecount++;
				}
			} else if(i % att.getLethargy() == 0) {
				out.println("It's Burak's turn! " + i);
				bcount++;
			} else if(i % att2.getLethargy() == 0) {
				out.println("It's Enemy's turn! " + i);
				ecount++;
			}
		}
		System.err.println("\nBurak's turns: " + bcount + "\nEnemy's turns: " + ecount);
	}
}