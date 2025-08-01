package game.asset;

import java.util.TeaType;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Character;
import game.asset.core.Focus;
import game.asset.core.Mind;
import game.asset.core.Skill;

public class Player extends Character {
	private String rep;
	private TeaType<Focus> fcs;
	private TeaType<Skill> skl;
	private String[] repArr;

	public Player(String name, String orig, String sex, int age, Appearance app,  Attributes att, Mind mnd) throws Exception {
		super(name, orig, sex, age, app, att, mnd);
		fcs = new TeaType<Focus>();
		skl = new TeaType<Skill>();
		flag = true;
	}
	
	public void setReputation(int code) {
		rep = repArr[code];
	}

	public String getReputation() {
		return rep;
	}
	
	public TeaType<Focus> getFocus() {
		return fcs;
	}
	
	public TeaType<Skill> getSkills() {
		return skl;
	}
}