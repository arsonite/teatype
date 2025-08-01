package game.engine.npc;

import game.asset.NPC;
import game.asset.Player;

import game.engine.Match;

import teaType.util.rigid.Parse;

public class Interact {
	public final static void choose(String input, Player p, NPC... arr) throws Exception {
		Match m = new Match();
		if(m.strike(input)) {
			System.err.println("Fight who?");
			for(NPC n : arr) {
				System.out.print(n.getName() + " ");
			}
			input = Parse.parseUserInput(true);
			for(NPC n : arr) {
				if(input.equals(n.getName())) {
					fight(p, n);
				}
			}
		}
	}
	
	final static void fight(Player p, NPC... arr) throws Exception {
		Fight f = new Fight(p, arr);
		f = null;
	}
}