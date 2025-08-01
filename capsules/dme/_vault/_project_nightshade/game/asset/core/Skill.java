package game.asset.core;

import game.asset.util.Asset;

public class Skill extends Asset {
	private Attributes att;
	private Trait[] trts;
	private boolean avail;
	private boolean debugAvail;
	
	public Skill(String name, String desc) {
		super(name, desc);
	}
	
	public void setConditions(Attributes att, Trait[] trts) {
		this.att = att;
		this.trts = trts;
	}
	
	public void setAttributeConditions(Attributes att) { this.att = att; }
	
	public void setTraitConditions(Trait[] trts) { this.trts = trts; }

	public boolean isAvailable() { return avail; }
	
	public boolean DEBUG_Availability() { return debugAvail; }
	
	public Attributes getAttributeConditions() { return att; }
	
	public Trait[] getTraitConditions() { return trts; }
}