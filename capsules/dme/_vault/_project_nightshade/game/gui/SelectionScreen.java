package game.gui;

import java.awt.Color;
import java.awt.Container;
import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

import game.engine.AdventureLoader;

public class SelectionScreen {
	protected int count;
	protected JPanel selectScreen;
	protected JButton one;
	protected JButton two;
	protected JButton three;
	protected JFrame frame = new JFrame();
	protected Container c;
	protected AdventureLoader aL;

	protected JButton test;

	public SelectionScreen(boolean b) {
		c = frame.getContentPane();
		selectScreen = new JPanel();
		aL = new AdventureLoader();

		debug(b);

		selectScreen.setLayout(new GridLayout(count, 0));

		c.add(selectScreen);
		c.setBackground(Color.BLACK);

		frame.setTitle("- Select Era -");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	public void debug(boolean b) {
		// TODO: Implementation of SuperReader
		String[] btnID = {
				"I. The First Tale: Primal Instict",
				"II. The Second Tale: Dawn of Civilization",
				"III. The Great Tale: Age of the Sea",
				"IV. The Iron Tale: Accursed Times",
				"V. The Death Tale: Plagued",
				"VI. The Risen Tale: Rise of the Industry",
				"VII. The Old Tale: A Fragile Peace",
				"VIII. The Forbidden Tale: ???",
				"XI. The New Tale: A Strange World",
				"X. The Last Tale: Two Sisters",
				"Debugger"
		};
		String[] actCom = {"1ST", "2ND", "3RD", "4TH", "5TH", "6TH", "7TH", "8TH", "9TH", "10TH", "FRBD", "TEST", "DEBUG"};
		JButton[] j = new JButton[btnID.length];
		count = btnID.length;

		for(int i = 0; i < btnID.length; i++) {
			j[i] = new JButton(btnID[i]);
			selectScreen.add(j[i]);
		}

		int c = 0;
		for(JButton i : j) {
			if(b) {
				i.setEnabled(b);
			} else if(c == 3 || c == 12 && !b) {
				i.setEnabled(true);
			} else {
				i.setEnabled(false);
			}
			i.addActionListener(aL);
			i.setActionCommand(actCom[c]);
			c++;
		}
	}

	public SelectionScreen(int game, boolean debug) {
		c = frame.getContentPane();
		selectScreen = new JPanel();
		aL = new AdventureLoader();

		debug(game, debug);

		selectScreen.setLayout(new GridLayout(count, 0));

		c.add(selectScreen);
		c.setBackground(Color.BLACK);

		frame.setTitle("- Select Adventure -");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	public void debug(int game, boolean b) {
		switch(game) {
		case 1:

			break;
		case 2:

			break;
		case 3:

			break;
		case 4:
			selectScreen.add(one = new JButton("I. Lost At Sea"));
			selectScreen.add(two = new JButton("II. Exile"));
			selectScreen.add(three = new JButton("III. Bloodtinted Dusk"));
			two.setEnabled(b);
			three.setEnabled(b);
			one.addActionListener(aL);
			two.addActionListener(aL);
			three.addActionListener(aL);
			one.setActionCommand("LOST_AT_SEA");
			two.setActionCommand("EXILE");
			three.setActionCommand("BLOODTINTED_DUSK");
			count = 3;
			break;
		case 5:

			break;
		case 6:

			break;
		case 7:

			break;
		case 8:

			break;
		case 9:

			break;
		case 10:

			break;
		case 11:

			break;
		case 12:
			selectScreen.add(test = new JButton("Debug"));
			test.addActionListener(aL);
			test.setActionCommand("DEBUG");
			count = 1;
			break;
		}
	}

	public void display(boolean show) {
		if(show) {
			frame.setVisible(true);
		} else {
			frame.setVisible(false);
		}
	}

	public void setSize(int width, int height, boolean resize) {
		if(resize) {
			frame.setResizable(true);
		} else {
			frame.setResizable(false);
		}
		frame.setSize(width, height);
	}

	public void close() {
		frame.dispose();
	}
}