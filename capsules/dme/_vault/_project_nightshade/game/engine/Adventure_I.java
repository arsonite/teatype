package game.engine;

import java.util.TeaType;
import java.util.HashMap;

import game.asset.NPC;
import game.asset.core.Item;
import game.asset.core.Location;

public interface Adventure_I {
	public void addNPC(NPC npc);
	public void addItem(Item item);
	public void addLocation(Location loc);
	public TeaType<NPC> getNPCS();
	public TeaType<Item> getItems();
	public TeaType<Location> getLocations();
	public HashMap<Object, Object> getPackage();
	public void setInput(String input);
	public String getOutput();
	public void validateProcess();
}