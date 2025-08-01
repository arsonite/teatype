package game.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridLayout;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

import game.engine.Command;

public class GC_InputField extends JPanel implements PropertyChangeListener {
	private static final long serialVersionUID = 7556237804640207437L;

	protected JTextField inputField;
	protected JPanel panel;
	protected JPanel permanentPanel;
	protected JPanel temporaryPanel;
	protected JLabel j;

	public GC_InputField(ActionController aC, Color c) {
		setLayout(new BorderLayout());

		inputField = new JTextField();
		inputField.setBackground(new Color(100, 100, 100));
		inputField.setForeground(Color.WHITE);
		
		panel = new JPanel();
		
		permanentPanel = new JPanel();
		permanentPanel.setBackground(new Color(41, 49, 51));
		permanentPanel.setLayout(new GridLayout(4, 4));
		permanentPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
		
		temporaryPanel = new JPanel();
		temporaryPanel.setBackground(Color.GREEN);
		temporaryPanel.setLayout(new GridLayout(4, 4));
		temporaryPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
		
		add(inputField, BorderLayout.NORTH);
		add(panel, BorderLayout.CENTER);
		
		panel.setLayout(new GridLayout(0, 2));
		panel.add(temporaryPanel);
		panel.add(permanentPanel);
		
		inputField.addKeyListener(aC);

		setBackground(c);
		setForeground(Color.WHITE);
		
		fillActions();
	}

	public void propertyChange(PropertyChangeEvent evt) {
		if(evt.getPropertyName().equals("INPUT_UPDATE")) {
			inputField.setText("");
		}
	}
	
	public void fillActions() {
		Enum<?>[] permCom = {
				Command.CHECK,
				Command.THINK,
				Command.WALK,
				Command.JUMP,
				Command.CROUCH,
				Command.LOOKAROUND,
				Command.USE,
				Command.STRIKE,
				Command.MEDITATE,
				Command.REMEMBER,
				Command.AWAKE,
				Command.UNLINK
				};
		for(Enum<?> e : permCom) {
			j = new JLabel(e.toString());
			if(	e == Command.CHECK 		||
				e == Command.MEDITATE 	||
				e == Command.REMEMBER 	||
				e == Command.AWAKE 		||
				e == Command.UNLINK) {
				j.setForeground(Color.RED);
			} else {
				j.setForeground(Color.WHITE);
			}
			j.setFont(new Font("", Font.BOLD, 14));
			permanentPanel.add(j);
		}
	}
	
	public void updateActions() {	
	}
}