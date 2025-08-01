package game.gen;

import game.asset.core.Item;

public class Item_Generator {
	public static Item generateItem() {
		Item i = new Item(null, null);
		return i;
	}

	public static Item[] generateItems(int amount) {
		Item arr[] = new Item[amount+1];
		for(int i = 0; i <= amount; i++) {
			arr[i] = generateItem();
		}
		return arr;
	}
}