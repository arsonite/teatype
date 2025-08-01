package game.asset;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Blood;
import game.asset.core.Character;
import game.asset.core.Mind;

public class Creature extends Character {
	public Creature(String name, String orig, String sex, int age, Appearance app, Attributes att, Mind mnd)
			throws Exception {
		super(name, orig, sex, age, app, att, mnd);
		// TODO Auto-generated constructor stub
	}
	protected String name;
	protected int age;
	
	//public Creature(String name, int age, Appearance app, Attributes att, Blood bld) {
	//}
}