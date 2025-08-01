package _debug.test;

import java.io.PrintWriter;

import game.asset.core.Mind;

public class AssetTest_Mind {
	public static void main(String[] args) {
		PrintWriter out = new PrintWriter (System.out, true);
		Mind m = new Mind();
		
		out.printf("%d %s %d %s%n", m.getMentalState(), m.getMentalStateToString(), m.getProgress(), m.getProgressToString());
		
		m.debug();
		for(int i = 0; i < 9; i++) {
			out.printf("%n%d %s	- %d %s", m.getMentalState(), m.getMentalStateToString(), m.getProgress(), m.getProgressToString());
			m.addMadness(250);
		}
	}
}
