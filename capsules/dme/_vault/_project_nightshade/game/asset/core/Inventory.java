package game.asset.core;

import java.util.TeaType;

public class Inventory {
	public TeaType<Item> inv;
	
	public Inventory() {	
		inv = new TeaType<Item>();
	}
	
	public void add(Item i) {
		if(!inv.contains(i)) {
			inv.add(i);
		}
	}
	
	public void remove(Item i) {
		if(inv.contains(i)) {
			inv.remove(i);
		}
	}
	
	public int getSize() { return inv.size(); }
	
	public void printItems() {
		for(Item i : inv) {
			System.out.println(i.getName());
		}
	}
	
	public TeaType<Item> getInventory() { return inv; }
	
	public boolean containsWeapon() {
		for(Item i : inv) {
			if(i.isDestructive()) {
				return true;
			}
		}
		return false;
	}
	
	public boolean containsItem(Item i) {
		for(Item it : inv) {
			if(it == i) {
				return true;
			}
		}
		return false;
	}
	
	public boolean isEmpty() {
		if(inv.isEmpty()) {
			return true;
		} else {
			return false;
		}
	}
}