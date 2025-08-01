package _debug.test;

import java.io.PrintWriter;

import game.asset.util.Asset_Init;

import game.engine.Match;

import teaType.util.io.Reader;

import util.Functions;

public class Temporary_Test_Environment {
	static PrintWriter out;

	public static void main(String[] args) {
		out = new PrintWriter(System.out, true);
		//grantTest();
		//tempReader();
		//levelTest();
		//levelList();
		matcherTest();
	}
	
	final static void matcherTest() {
		Match m = new Match();
		String s = "Male";
		if(m.male(s)) {
			out.println("True");
			return;
		}
		out.println("False");
	}

	final static void grantTest() {
		int GRN_MAX = 50;
		int grn = 45;
		int temp = 7;
		out.println(	temp - ((temp + grn) - GRN_MAX));
	}

	final static void tempReader() {
		Reader r = new Reader();
		String[] temp1 = r.stringArray("./src/_res/dump/#!lastnames.txt");
		String[] temp2 = new String[temp1.length];
		StringBuilder sb;
		int count = 0;
		for(String s : temp1) {
			sb = new StringBuilder(s);
			temp2[count] = sb.substring(0, 1);
			s = sb.substring(1, s.length()).toLowerCase();
			temp1[count] = temp2[count] + s;
			out.println(temp1[count]);
			count++;
		}
	}

	final static void levelTest() {
		//final int EXP_STATIC = 1425;
		//final int EXP_MAX = 128256;
		final int LVL_MAX = 90;
		double exp = 0;
		int lvl = 0;
		lvl = 1;
		exp = 0;
		for(int i = 0; i < LVL_MAX; i++) {
			out.println("-" + exp + "-");
			exp += 157.37 * Math.pow(2, lvl/16);
			lvl++;
		}
	}

	final static void levelList() {
		int[] i = Asset_Init.LVL();
		int count = 0;
		int temp = 0;
		for(Integer integer : i) {
			count++;
			temp+= integer;
			out.printf("Level: %d needs %d XP. %d <- Overall Minimum Neeeded XP%n", count, integer, temp);
		}

		int exp = 12000;
		int lvl = Functions.calculateLevel(exp);
		out.printf("%nGiven Overall XP: %d, Current Level: %d", exp, lvl);
	}
}