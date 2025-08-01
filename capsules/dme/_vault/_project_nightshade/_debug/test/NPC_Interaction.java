package _debug.test;

import game.asset.NPC;
import game.asset.Player;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Mind;

import game.engine.npc.Interact;

import teaType.util.StreamBuffer;

import teaType.util.rigid.Parse;

public class NPC_Interaction {
	public static void main(String[] args) throws Exception {
		StreamBuffer.fixConsole();

		Appearance app = new Appearance();
		app.setRandom("Male");
		Attributes att = new Attributes();
		att.random(85);
		Mind mnd = new Mind();
		mnd.random();
		Player p = new Player("Burak Günaydin", "Eastern", "Male", 23, app, att, mnd);
		p.addArmor(300);

		Appearance nApp = new Appearance();
		nApp.setRandom("Female");
		Attributes nAtt = new Attributes();
		nAtt.random(15);
		Mind nMnd = new Mind();
		nMnd.random();
		NPC n = new NPC("Jack", "The Ripper", "Male", 25, nApp, nAtt, nMnd, false);
		
		while(true) {
			String input = Parse.parseUserInput(true);
			System.err.println("You typed: \"" + input + "\"");
			Interact.choose(input, p, n);
			if(input.equals("q")) {
				break;
			}
		}
	}
}