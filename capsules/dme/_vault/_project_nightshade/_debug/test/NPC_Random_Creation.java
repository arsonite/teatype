package _debug.test;

import game.asset.NPC;

import game.gen.NPC_Generator;

public class NPC_Random_Creation {
	public static void main(String[] args) {
		try {
			randomGenerateNPCs(false, "");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void randomGenerateNPCs(boolean print, String file) throws Exception {
		NPC[] list = NPC_Generator.generateNPCS(0);
		
		for(NPC n : list) {
			n.increaseIllness(true, ((int) (Math.random()*4+0)));
			n.randomArmorWithMax(250);
			System.out.println(n.retrieveStats());
		}
	}
}