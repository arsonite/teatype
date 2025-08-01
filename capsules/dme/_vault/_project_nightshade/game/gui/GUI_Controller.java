package game.gui;

import java.awt.Color;
import java.awt.GridLayout;

import javax.swing.JPanel;

public class GUI_Controller extends JPanel {
	private static final long serialVersionUID = -7886083481478369150L;

	protected ActionController aC;
	protected Central m;

	public GUI_Controller(ActionController aC, Central c) {
		this.aC = aC;
		this.m = c;
		
		setLayout(new GridLayout(2, 0));
		
		GC_EngineOutput o = new GC_EngineOutput(c);
		GC_InputField i = new GC_InputField(aC, new Color(65, 65, 65));
		
		c.addPropertyChangeListener(o);
		c.addPropertyChangeListener(i);
		
		add(o);
		add(i);
		
		setVisible(true);
	}
}
