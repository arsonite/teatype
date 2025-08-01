package _debug.test;

import game.asset.Player;
import game.asset.core.Location;

public class AssetTest_Location {
	public static void main(String[] args) throws Exception {
		Location l = new Location("World", "*DEBUG*", 10);
		
		Player p = new Player("", "", "", 0, null, null, null);
		
		l.print();
	}
}