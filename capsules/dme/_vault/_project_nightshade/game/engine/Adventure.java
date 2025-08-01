package game.engine;

import java.util.TeaType;
import java.util.HashMap;

import game.asset.NPC;

import game.asset.core.Item;
import game.asset.core.Location;

public abstract class Adventure extends HashMap<Object, Object> implements Adventure_I {
	private static final long serialVersionUID = 1187307781663420870L;
	
	protected String title, desc, input, output;
	protected int chrono;
	protected TeaType<NPC> npcList;
	protected TeaType<Item> itemList;
	protected TeaType<Location> locList;

	public Adventure() {
		npcList = new TeaType<NPC>();
		itemList = new TeaType<Item>();
		locList = new TeaType<Location>();
	}

	public Adventure(String title, String description, int chronology) {
		this.title = title;
		this.desc = description;
		this.chrono = chronology;
	}

	public void addNPC(NPC npc) {
		npcList.add(npc);
	}

	public void addItem(Item item) {
		itemList.add(item);
	}

	public void addLocation(Location loc) {
		locList.add(loc);
	}

	public TeaType<NPC> getNPCS() {
		return npcList;
	}

	public TeaType<Item> getItems() {
		return itemList;
	}

	public TeaType<Location> getLocations() {
		return locList;
	}

	public HashMap<Object, Object> getPackage() {
		HashMap<Object, Object> m = new HashMap<Object, Object>();
//		m.put(0, this);
//		m.put(1, title);
//		m.put(2, desc);
//		m.put(3, chrono);
//		m.put(4, npcList);
//		m.put(5, itemList);
//		m.put(6, locList);
		return m;
	}

	public void setInput(String input) {
		this.input = input;
	}

	public String getOutput() {
		return output;
	}

	@Override
	public void validateProcess() {
		// TODO Auto-generated method stub
		
	}
}