package game.asset;

import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Character;
import game.asset.core.Mind;

public class NPC extends Character {
	private String profession;
	private String algn;
	// TODO: Replace with SuperReader-init
	private String[] algnScale = {"Friendly", "Trusting", "Neutral", "Mistrusting", "Hostile"};
	private String[] professions = {"", "", "", "", "", "", "", "", ""};
	private boolean crucial;

	public NPC(String name, String orig, String sex, int age, Appearance appearance, Attributes attributes,
			Mind mind, boolean crucial) throws Exception {
		super(name, orig, sex, age, appearance, attributes, mind);
		this.crucial = crucial;
		flag = false;
	}

	public void setProfession(int code) {
		profession = professions[code];
	}

	public void setAlignment(int code) {
		algn = algnScale[code];
	}

	public boolean isCrucial() {
		return crucial;
	}

	public String getProfession() {
		return profession;
	}

	public String getAlignment() {
		return algn;
	}
}