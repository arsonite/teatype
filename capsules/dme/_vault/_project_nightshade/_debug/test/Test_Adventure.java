package _debug.test;

import java.util.Scanner;

import game.asset.Player;
import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Blood;
import game.asset.core.Conjuration;
import game.asset.core.Focus;
import game.asset.core.Inventory;
import game.asset.core.Mind;
import game.asset.core.Skill;
import game.asset.core.Trait;
import game.engine.Adventure;
import teaType.data.TeaType;

//TODO: Für Code und Codelock Thread erstellen
public class Test_Adventure extends Adventure {
	static final long serialVersionUID = 7454987830282711827L;

	private final String MARK_I = "> ";
	public String name, sex, race, input;
	public int inputInt, age, chronoCount, attPnts, code;
	public int[] temp;
	public boolean codeLock, charCreated;
	public StringBuilder sb;
	public Scanner in;
	public Appearance app;
	public Attributes att;
	public Blood bld;
	public Conjuration[] con;
	public Focus foc;
	public Inventory inv;
	public Mind mnd;
	public TeaType<Skill> skls;
	public TeaType<Trait> trt;
	public Player p;

	public Test_Adventure() {
		super();
		temp = new int[7];
		attPnts = 100;
		code = 0;
		charCreated = false;
		codeLock = false;
		sb = new StringBuilder();
		displayMenu();
	}

	public void setInput(String input) { this.input = input; }

	private final void updateOutput(String output) {
		this.output = output;
		clearCache();
	}

	private final void clearCache() { sb.delete(0, sb.length()); }

	private final void displayMenu() {
		sb.append(String.format("1.%s %n2.%s %n3.%s",
				" Character-Utility", " Debug-Stats", " Spawn-Menu"));
		updateOutput(sb.toString());
	}

	public void validateProcess() {

		// TODO: Debug
		/*#############################################*/
		System.out.println("Adventure_Debug: " + input);
		/*#############################################*/

		if(input.equals("re")) {
			input = "0";
		}
		in = new Scanner(input);
		if(in.hasNextInt() && !codeLock) {
			code = Integer.parseInt(input.replaceAll("\\S+s+", ""));
			try {
				switch(code) {
				case 0:
					displayMenu();
					break;
				case 1:
					chronoCount = 0;
					codeLock = true;
					if(!charCreated) {
						characterCreation();
					}
					break;
				case 2:
					if(charCreated) {
						displayStats();
					}
					break;
				case 3:
					codeLock = true;
					spawnMenu();
					break;
				}
			} catch(Exception e) {
				e.printStackTrace();
			}
		} else {
			try {
				switch(code) {
				case 0:
					displayMenu();
					break;
				case 1:
					characterCreation();
					break;
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		in.close();
	}
	
	public void spawnMenu() {
		
	}

	public void characterCreation() throws Exception {
		String enter = MARK_I + "Please enter: ";
		switch(chronoCount) {
		case 0:
			updateOutput(enter + "Name");
			break;
		case 1:
			name = input;
			updateOutput(enter + "Race");
			break;
		case 2:
			race = input;
			updateOutput(enter + "Sex");
			break;
		case 3:
			sex = input;	
			updateOutput(enter + "Age");
			break;
		case 4:
			age = parseInteger();
			att = new Attributes();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(0).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 5:
			parseInteger();
			attPnts-= parseInteger();
			temp[0] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(1).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 6:
			parseInteger();
			attPnts-= parseInteger();
			temp[1] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(2).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 7:
			parseInteger();
			attPnts-= parseInteger();
			temp[2] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(3).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 8:
			parseInteger();
			attPnts-= parseInteger();
			temp[3] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(4).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 9:
			parseInteger();
			attPnts-= parseInteger();
			temp[4] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(5).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 10:
			parseInteger();
			attPnts-= parseInteger();
			temp[5] = parseInteger();
			updateOutput(enter + "Amount XP you want to invest into: \"" + att.getAttribute(6).getFirst() + "\" (" + attPnts + " XP left)");
			break;
		case 11:
			parseInteger();
			attPnts-= parseInteger();
			temp[6] = parseInteger();
			break;
		case 12:
			att.DEBUG_setAttributes(temp);
			app = new Appearance();
			mnd = new Mind();
			mnd.randomStats();
			mnd.randomCivic();
			p = new Player(name, race, sex, age, app, att, mnd);
			app.setRandom(p.getSex());
			updateOutput(p.retrieveStats());
			charCreated = true;
			codeLock = false;
			break;
		}
		chronoCount++;
	}

	private void displayStats() { updateOutput(p.retrieveStats()); }

	private final int parseInteger() { return new Integer(Integer.parseInt(input.replaceAll("\\S+s+", ""))); }
}