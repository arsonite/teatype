package game.engine;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

import game.gui.Central;

public class AdventureController implements PropertyChangeListener {
	protected Adventure_I a;
	protected Central c;
	protected PropertyChangeSupport pcs;
	
	public AdventureController(Adventure_I a, Central c) {
		this.a = a;
		this.c = c;
	}

	public void propertyChange(PropertyChangeEvent evt) {
		if(evt.getPropertyName().equals("INPUT_UPDATE")) {
			a.setInput(c.getUserInput());
			
			// TODO: Debug
			/*#############################################*/
			System.out.println("AdventureController: " + c.getUserInput());
			/*#############################################*/
			
			a.validateProcess();
			c.sendEngineOutput(a.getOutput());
		}
	}
}