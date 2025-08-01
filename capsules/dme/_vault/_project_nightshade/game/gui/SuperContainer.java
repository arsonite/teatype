package game.gui;

import java.awt.Color;
import java.awt.Container;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.border.EmptyBorder;

import game.engine.AdventureController;
import game.engine.AdventureLoader;
import game.engine.Adventure_I;

public class SuperContainer implements PropertyChangeListener {
	private int r, g, b, p;
	private String input;
	private ActionController aC;
	private AdventureController advC;
	private Adventure_I a;
	private Ambience am;
	private Color color;
	private Container con;
	private JFrame frame;
	private AdventureLoader lA;
	private Central c;
	private GUI_Controller gC;

	public SuperContainer(Adventure_I a) {
		frame = new JFrame();
		am = new Ambience(this);
		con = frame.getContentPane();
		c = new Central();
		aC = new ActionController(c);
		gC = new GUI_Controller(aC, c);
		lA = new AdventureLoader();
		advC = new AdventureController(a, c);

		c.addPropertyChangeListener(advC);
		
		con.add(gC);
		con.setBackground(am.getColor());

		((JComponent) con).setBorder(new EmptyBorder(0, 35, 0, 35));

		frame.setTitle("Text Adventure ");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	public void display(boolean b) {
		if (b) {
			frame.setVisible(true);
		} else {
			frame.setVisible(false);
		}
	}

	public void setSize(int width, int height, boolean b) {
		if(b) {
			frame.setResizable(true);
		} else {
			frame.setResizable(false);
		}
		frame.setSize(width, height);
	}

	public void propertyChange(PropertyChangeEvent evt) {
		if(evt.getPropertyName().equals("AMBIENCE_UPDATE")) {
			input = c.getUserInput();
			p = Integer.parseInt(input);
			frame.setTitle(input);
			r = p;
			g = p;
			b = p;
			color = new Color(r, g, b);
			color = Color.getColor(c.getUserInput());
		}
	}

	public void changeAmbience() {
		con.setBackground(color);
		frame.getContentPane().validate();
		frame.getContentPane().repaint();
	}
}