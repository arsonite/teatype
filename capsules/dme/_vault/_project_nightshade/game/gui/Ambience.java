package game.gui;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Ambience implements ActionListener {
	protected SuperContainer sC;
	
	protected Color c = Color.WHITE;
	
	static final String DEFAULT = "DEFAULT";
	static final String INDOOR_BRIGHT = "INDOOR_BRIGHT";
	static final String INDOOR_DARK = "INDOOR_DARK";
	static final String DUSK = "DUSK";
	static final String DAY = "DAY";
	static final String DAWN = "DAWN";
	static final String NIGHT = "NIGHT";
	
	static final String b = "BLACK";
	
	public Ambience(SuperContainer sC) {
		this.sC = sC;
	}

	public void actionPerformed(ActionEvent e) {
		switch(e.getActionCommand()) {
		case DEFAULT:
			break;
		case INDOOR_BRIGHT:
			break;
		case INDOOR_DARK:
			break;
		case DUSK:
			break;
		case DAY:
			break;
		case DAWN:
			break;
		case NIGHT:
			break;
		case b:
			c = Color.getColor(b);
			sC.changeAmbience();
			break;
		}
	}
	
	public Color getColor() {
		return c;
	}
}