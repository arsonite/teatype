package game.asset.core;

import game.asset.util.Asset;

public class Location extends Asset {
	private int size, d;
	private Asset[][] arr;

	public Location() {
		init(0);
	}

	public Location(int size) {
		init(size);
	}

	public Location(String name, String desc) {
		super(name, desc);
		init(0);
	}

	public Location(String name, String desc, int size) {
		super(name, desc);
		init(size);
	}

	final void init(int size) {
		this.size = size;
		arr = new Asset[size][size];
		d = (int) (Math.log10(size) + 1);
		if(d < 0) {
			d = 0;
		}
	}

	public final void addLocation() {

	}

	public final void removeLocation() {

	}

	public final void addSubLocation(Location l) {

	}

	public final void removeSubLocation(Location l) {

	}

	public final void addAsset() {

	}

	public final void removeAsset() {

	}

	public final void moveAsset(Location l, Asset a) {

	}

	public final void print() {
		String s = String.format("%s-Name: %s | Description: %s | Slot-Size: %d",
				this.getClass().getSimpleName(), name, desc, size);
		System.out.println(s);
		for(int i = 0; i < s.length(); i++) {
			System.out.print("-");
		}
		System.out.println();
		arr[0][0] = null;
		for(int x = 0; x < arr.length; x++) {
			System.out.print("[" + x + "]");
			for(int y = 1; y < arr.length; y++) {
				System.out.print("[" + y + "]");
			}
			System.out.println();
		}
	}

	final String assemble(int i) {
		StringBuilder sb = new StringBuilder();
		String ol, ul, l, w;
		ol = "‾";
		ul = "_";
		l = "|";
		w = " ";
		sb.append("");
		return sb.toString();
	}
}