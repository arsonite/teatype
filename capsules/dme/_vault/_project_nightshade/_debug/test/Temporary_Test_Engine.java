package _debug.test;

import java.io.PrintWriter;

import java.util.Scanner;

import game.asset.Player;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Mind;

import game.engine.Match;

public class Temporary_Test_Engine {
	final static String MARK = "> ";
	private static PrintWriter out;
	private static Player p;

	public static void main(String[] args) throws Exception {
		out = new PrintWriter(System.out, true);
		Match m = new Match();
		p = null;
		System.out.println("Your options:" +
				"\n0. Exit = 'exit'" +
				"\n1. Character-Creation = 'cc'" + 
				"\n2. Loadline = 'load'" + 
				"\n3. " + 
				"\n4. " + 
				"\n5. "
				);
		while(true) {
			String input = new Scanner(System.in).nextLine();
			System.err.println("You typed: " + input + "\n");

			if(input.equals("create player") && p != null) {
				if(p != null) {
					String name, orig, sex;
					int age;
					Appearance app;
					Attributes att;
					Mind mnd;

					//p = new Player(name, orig, sex, age, app, att, mnd);
				} else {
					System.err.println("You already created a player! " + p.getName() + ".");
				}
			}

			if(input.equals("take")) {

			}

			if(m.suicide(input)) {
				System.exit(0);
			}
		}
	}

	final static int parseInteger(String input) {
		return new Integer(Integer.parseInt(input.replaceAll("\\S+s+", "")));
	}
}