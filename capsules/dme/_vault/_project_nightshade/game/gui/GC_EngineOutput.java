package game.gui;

import java.awt.BorderLayout;
import java.awt.Color;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.border.EmptyBorder;

public class GC_EngineOutput extends JPanel implements PropertyChangeListener {
	private static final long serialVersionUID = -4967614298523654734L;

	private int selectionCode;
	private String output;
	private JTextArea engineOutput;
	private JScrollPane sp;
	private Central c;

	public GC_EngineOutput(Central c) {
		this.c = c;

		setLayout(new BorderLayout());

		engineOutput = new JTextArea();
		engineOutput.setEditable(false);
		engineOutput.setBackground(Color.BLACK);
		engineOutput.setForeground(Color.GREEN);
		
		// TODO: temporary solution for missing refresh
		engineOutput.setText("Please proceed by pressing \"Enter\"");

		sp = new JScrollPane(engineOutput);
		sp.setBackground(Color.BLACK);
		sp.setForeground(Color.BLACK);
		
		add(sp, BorderLayout.CENTER);

		setBackground(Color.BLACK);
		setForeground(Color.GREEN);

		setBorder(new EmptyBorder(5, 5, 5, 5));
	}

	public void select() {
	}

	public void propertyChange(PropertyChangeEvent evt) {
		if(evt.getPropertyName().equals("OUTPUT_UPDATE")) {
			selectionCode = c.getSelectionCode();
			output = c.getEngineOutput();
			engineOutput.setText(output);
		}
	}
	
	public int getSelectionCode() {
		return selectionCode;
	}
}