package _debug.test;

import java.io.PrintWriter;

import game.asset.core.Item;

public class Item_Random_Creation {
	public static void main(String[] args) throws Exception {
		PrintWriter out = new PrintWriter(System.out, true);
		
		Item i = new Item("Sword of the Sun", "A magnificient sword, allegedly forged in the warmth of a distant star.");
		i.setUsability(true, false, false, false, false, true, false, false, false, false);
		i.setEquipCode(11);
		i.setDamageStats(1000, 35, 300);
		i.setRarity(1);
		out.println(i.retrieveStats());
		
		/*
		Appearance app = new Appearance();
		app.setRandom("Male");
		Attributes att = new Attributes();
		att.random(10);
		Mind mnd = new Mind();
		mnd.random();
		
		NPC n = NPC_Generator.generateNPC();
		n.addItem(i);
		n.equipItem(i);
		out.println(n.retrieveStats());
		*/
	}
}