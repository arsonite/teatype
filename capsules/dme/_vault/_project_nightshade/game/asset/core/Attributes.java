package game.asset.core;

import java.util.Arrays;
import java.util.Random;

import teaType.data.BiPrimitive;

import util.Functions;

import game.engine.exceptions.LevelOutOfBoundsException;

/**
 * The class {@code Attributes} contains the methods necessary to determine
 * the amount of experience-points, the level and the character-attributes
 * of all the non-playable and playable characters in the game.
 * This ranges from humans to creatures to bosses.
 * 
 * <p>{@code Attributes} is part of every {@code Character} and its subclasses.
 * 
 * @author Burak Günaydin
 */

public class Attributes {
	private int let, sum;
	final int LVL_CAP = 700;
	private int[] att;
	private BiPrimitive letUtil;
	private BiPrimitive[] attUtil;

	public Attributes() {
		att = new int[7];
		for(int i = 0; i < att.length; i++) {
			att[i] = 1;
		}
		attUtil = new BiPrimitive[att.length];
		attributesToUtil();
	}

	public void levelUp(int exp, int atr) {
		att[atr]+= exp;
		attributesToUtil();
	}

	final void calculateLethargy() { let = Functions.calculateLethargy(att); }

	public boolean isGodlike() {
		int sum = 0;
		for(int i : att) {
			sum+=i;
		}
		if(sum == LVL_CAP) {
			return true;
		} else {
			return false;
		}
	}

	public void setAttributes(int fit, int vig, int alc, int bri, int awe, int emp, int trc) throws LevelOutOfBoundsException {
		if((fit + vig + alc + bri + awe + emp + trc) <= LVL_CAP) {
			att[0] = fit;
			att[1] = vig;
			att[2] = alc;
			att[3] = bri;
			att[4] = awe;
			att[5] = emp;
			att[6] = trc;
			attributesToUtil();
		} else {
			throw new LevelOutOfBoundsException(0);
		}
	}

	/**
	 * An efficient random-generation algorithm, which distributes a certain number of given experience-points
	 * randomly between a fixed amount of attributes.
	 * 
	 * @param lvl A parameter containing the amount of character-levels,
	 * 		  which depict the amount of available experience-points
	 * @throws Exception
	 */
	public void random(int lvl) throws Exception {
		Random rnd = new Random();
		int bonusEXP;
		if(lvl > 1 && lvl <= 83) {
			bonusEXP = 7 * lvl;
		} else if (lvl > 83) {
			bonusEXP = (7 * lvl) + (int) (lvl / 90.0 * 100 - 90 + 1);
		} else if (lvl > 85) {
			throw new LevelOutOfBoundsException(lvl);
		} else {
			bonusEXP = 0;
		}
		int m = 101 + bonusEXP;
		int min = 1;
		int max = m - min * 7;
		for(int i = 1; i < att.length; i++) {
			att[i]+= rnd.nextInt(max);
		}
		Arrays.sort(att, 1, att.length);
		for(int i = 1; i < att.length; i++) {
			att[i-1] = att[i] - att[i-1] + min;
		}
		att[att.length-1] = max - att[att.length-1] + min;
		attributesToUtil();
	}

	/**
	 * A method to convert the integer-array of attributes to a StringInteger-array containing
	 * the descriptive attribute-names with their corresponding value
	 */
	final void attributesToUtil() {
		// TODO: Replace with StringReader
		sum = 0;
		String[] temp = {"Fitness", "Vigor", "Alacrity", "Brilliance", "Awareness", "Empathy", "Transcendence"};
		for(int i = 0; i < temp.length; i++) {
			attUtil[i] = new BiPrimitive(temp[i], att[i]);
			sum+= att[i];
		}
		calculateLethargy();
		letUtil = new BiPrimitive("Lethargy", let);
	}

	// TODO: Player-Title dependent on amount of different attributes
	public String setTitle() {
		String t = "";
		return t;
	}

	public int getFitness() { return att[0]; }
	public int getVigor() { return att[1]; }
	public int getAlacrity() { return att[2]; }
	public int getBrilliance() { return att[3]; }
	public int getAwareness() { return att[4]; }
	public int getEmpathy() { return att[5]; }
	public int getTranscendence() { return att[6]; }
	public int getLethargy() { return let; }

	public int[] getNumbers(boolean let) {
		if(let) {
			int[] temp = new int[att.length+1];
			for(int i = 0; i < att.length; i++) {
				temp[i] = att[i];
			}
			temp[temp.length-1] = this.let;
			return temp;
		} else {
			return att;
		}
	}

	public BiPrimitive getAttribute(int code) {
		switch(code) {
		case 0: return attUtil[0];
		case 1: return attUtil[1];
		case 2: return attUtil[2];
		case 3: return attUtil[3];
		case 4: return attUtil[4];
		case 5: return attUtil[5];
		case 6: return attUtil[6];
		case 7: return letUtil;
		}
		// TODO: Argument
		throw new IllegalArgumentException("" + code);
	}

	public BiPrimitive[] getAttributes(boolean let) {
		if(let) {
			BiPrimitive[] temp = new BiPrimitive[attUtil.length+1];
			for(int i = 0; i < attUtil.length; i++) {
				temp[i] = attUtil[i];
			}
			temp[temp.length-1] = letUtil;
			return temp;
		} else {
			return attUtil;
		}
	}

	public void DEBUG_SetAllZero() {
		for(int i = 0; i < att.length; i++) {
			att[i] = 0;
		}
		attributesToUtil();
	} 

	public void DEBUG_SetAll100() {
		for(int i = 0; i < att.length; i++) {
			att[i] = 100;
		}
		attributesToUtil();
	}

	public void DEBUG_setAttributes(int[] attArr) {
		int count = 0;
		for(int i : attArr) {
			att[count] = i;
			count++;
		}
		attributesToUtil();
	}
}