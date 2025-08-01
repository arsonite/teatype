package game.gen;

import game.asset.core.Item;

import teaType.data.TeaType;

import teaType.util.io.Writer;

public class Item_Creation {
	static final String PATH = "./src/_res/pre/common_items.txt";;
	static boolean create, append, linebreak, extraspace;
	static TeaType<Item> items;	
	static TeaType<String> list;
	static Writer w;

	public static void main(String[] args) {
		create = true;
		append = true;
		linebreak = true;
		extraspace = false;

		w = new Writer(PATH);
		items = new TeaType<Item>();
		list = new TeaType<String>();

		Item i = new Item("Sword of the Sun", "A peculiar sword, allegedly forged in the warmth of a distant star.");
		i.setUsability(true, true, true, true, true, true, true, true, false, false);
		i.setEquipCode(11);
		i.setValues(10, 75, 5, 3, 10000);
		i.setDamageStats(3500, 35, 350);
		i.setRarity(5);
		i.setType(5);
		i.setWeaponType(10);

		Item i2 = new Item("Helmet of the Sun", "A peculiar Helm, allegedly forged in the warmth of a distant star.");
		i2.setUsability(false, true, true, true, false, true, true, true, false, false);
		i2.setEquipCode(0);
		i2.setValues(50, 125, 10, 5, 5000);
		i2.setRarity(5);
		i2.setType(4);

		printItems();
		addItems(i);
		writeItems();

	}

	private final static void printItems(Item... i) {
		for(Item item : i) {
			System.out.println(item.retrieveStats() + "\n");	
		}
	}

	private final static void addItems(Item... i) {
		for(Item item : i) {
			items.add(item);
		}
	}

	public static void writeItems() {
		for(Item i : items) {
			list.add(convertToString(i));
		}
		w.teaType(list, create, append, linebreak, extraspace);
	}

	public static String convertToString(Item item) {
		String s = "";
		String[] sym = {"!", "#", "-", ";"};
		StringBuilder sb = new StringBuilder();

		sb.append(sym[0] + item.getID() + sym[0]);
		sb.append("\n");

		sb.append(sym[1] + item.getName() + sym[1]);
		sb.append("\n");

		sb.append(sym[2]);
		int[] arr = item.getUsabilityCodes();
		for(int i = 0; i < arr.length; i++) {
			if(i == arr.length-1) {
				sb.append(arr[i] + sym[2]);
			} else {
				sb.append(arr[i] + " ");
			}
		}
		sb.append("\n");

		sb.append(sym[2] + item.getEquipCode() + sym[2]);
		sb.append("\n");

		sb.append(sym[2]);
		arr = item.getValues();
		for(int i = 0; i < arr.length; i++) {
			if(i == arr.length-1) {
				sb.append(arr[i] + sym[2]);
			} else {
				sb.append(arr[i] + " ");
			}
		}
		sb.append("\n");

		sb.append(sym[2]);
		double[] d = item.getDamageStats();
		for(int i = 0; i < d.length; i++) {
			if(i == d.length-1) {
				sb.append(d[i]*100 + sym[2]);
			} else {
				sb.append(d[i]*10000 + " ");
			}
		}
		sb.append("\n");

		/*
		i.setDamageStats(3500, 35, 350);
		i.setRarity(5);
		i.setType(5);
		i.setWeaponType(10);
		 */

		sb.append(sym[3] + sym[3]);
		s = sb.toString();
		return s;
	}
}