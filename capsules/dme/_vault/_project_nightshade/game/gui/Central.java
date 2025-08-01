package game.gui;

import java.awt.Color;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

import java.util.Scanner;

public class Central {
	static final Object EVENT = null;
	private int code;
	private String engineOutput, userInput;
	private Enum<?> command;
	private Color c;
	private PropertyChangeSupport pCS;
	private Scanner in;
	
	public Central () {
		userInput = "";
		in = new Scanner(userInput);
		pCS = new PropertyChangeSupport(this);
	}

	private void updateInput(Object para) {
		pCS.firePropertyChange("INPUT_UPDATE", EVENT, para);
	}
	
	private void updateOutput(Object para) {
		pCS.firePropertyChange("OUTPUT_UPDATE", EVENT, para);
	}
	
	private void updateAmbience(Object para) {
		pCS.firePropertyChange("AMBIENCE_UPDATE", EVENT, para);
	}

	public void addPropertyChangeListener(PropertyChangeListener l) {
		this.pCS.addPropertyChangeListener(l);
	}

	public void removePropertyChangeListener(PropertyChangeListener l) {
		this.pCS.removePropertyChangeListener(l);
	}
	
	public void sendEngineOutput(String engineOutput) {
		this.engineOutput = engineOutput;
		updateOutput(engineOutput);
	}

	public void parseUserInput(String userInput) {
		this.userInput = userInput;
		if(in.hasNextInt()) {
			code = Integer.parseInt(this.userInput);
		}
		updateInput(userInput);
	}
	
	public void changeColor(Color c) {
		this.c = c;
		updateAmbience(c);
	}
	
	public String getEngineOutput() {
		return engineOutput;
	}

	public String getUserInput() {
		return userInput;
	}

	public int getSelectionCode() {
		return code;
	}
}