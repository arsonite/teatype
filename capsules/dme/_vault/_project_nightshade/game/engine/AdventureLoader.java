package game.engine;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import _debug.Main;

public class AdventureLoader implements ActionListener {
	protected AdventureController aC;

	public void actionPerformed(ActionEvent e) {
		switch(e.getActionCommand()) {
		case "1ST":
			Main.launchAdventure(1);
			break;
		case "2ND":
			Main.launchAdventure(2);
			break;
		case "3RD":
			Main.launchAdventure(3);
			break;
		case "4TH":
			Main.launchAdventure(4);
			break;
		case "5TH":
			Main.launchAdventure(5);
			break;
		case "6TH":
			Main.launchAdventure(6);
			break;
		case "7TH":
			Main.launchAdventure(7);
			break;
		case "8TH":
			Main.launchAdventure(8);
			break;
		case "9TH":
			Main.launchAdventure(9);
			break;
		case "10TH":
			Main.launchAdventure(10);
			break;
		case "FRBD":
			Main.launchAdventure(11);
			break;
		case "LOST_AT_SEA":
			Main.launchGame(null);
			break;
		case "EXILE":
			Main.launchGame(null);
			break;
		case "BLOODTINTED_DUSK":
			Main.launchGame(null);
			break;
			
	    	///////////////////////////////////////////////////////////////////////
		//Debug

		case "TEST":
			Main.launchAdventure(12);
			break;
		}
	}
}