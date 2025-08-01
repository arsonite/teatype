package _debug.test;

import game.asset.Player;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Conjuration;
import game.asset.core.Item;
import game.asset.core.Mind;

public class Player_Creation {
	public static void main(String[] args) throws Exception {
		Appearance app = new Appearance();
		
		Attributes att = new Attributes();
		att.random(100);

		Conjuration blast = new Conjuration("Blast", "Non-lethal blast.", 0);
		blast.setValues(100, 0, 5, 3);

		Item sword = new Item("Sword", "A plain old sword.");
		sword.setUsability(true, false, false, false, false, false, false, false, false, false);
		sword.setDamageStats(12, 0.325, 0.575);
		sword.setRarity(2);

		Mind m = new Mind();
		m.randomStats();
		m.randomCivic();

		Player b = new Player("Burak Günaydin", "Eastern", "Male", 23, app, att, m);
		app.setRandom(b.getSex());
		app.setBodyMeasurements(183, 81500);
		b.addArmor(150);
		b.addItem(sword);
		b.equipItem(sword);
		b.addConjuration(blast);
		att.random(b.getLevel());
		System.out.println(b.retrieveStats());
	}
}