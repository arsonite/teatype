package util;

import game.asset.core.Blood;
import game.asset.core.Mind;
import game.asset.core.Trait;

import teaType.data.BiPrimitive;
import teaType.data.TeaType;

/**
 * The utility-class {@code Functions} is a collection of mathematical functions and algorithms
 * which finds its uses all over the classes in the engine and its assets.
 *
 * @since JDK 1.91 ~ <i>2017</i>
 * @author Burak Günaydin <b>{@code (arsonite)}</b>
 */
public class Functions {

	/**
	 *
	 * @param chance
	 * @return
	 */
	public final static boolean roll(double chance) {
		return Math.random() <= chance;
	}

	/**
	 *
	 * @param dmgPack
	 * @return
	 */
	// TODO: Revamp for internal double system and external int system
	public final static BiPrimitive inflictDamage(double[] dmgPack) {
		double dmgCap = dmgPack[0];
		double baseFluct = dmgCap * 1.0875;
		double min = dmgCap * 0.875;
		double max = baseFluct - min;
		if(roll(dmgPack[1])) {
			return new BiPrimitive(true, (dmgPack[2]*= (Math.random()*max+min)));
		} else {
			return new BiPrimitive(false, new Double(Math.random()*max+min));
		}
	}

	/**
	 * Calculates and returns a double-array containing the overall damage.
	 *
	 * @param vig Represents the stat for the character-attribute 'Vigor'
	 * @param alc Represents the stat for the character-attribute 'Alacrity'
	 * @param m
	 * @param trt
	 * @return
	 */
	public final static double[] calculateDamage(int vig, int alc, Mind m, TeaType<Trait> trt) {
		double dmgCap = 1.0;
		double critChance = 0.05;
		double critDmg = 1.0;
		dmgCap+= ((double) (dmgCap + vig + alc)/2);
		critChance+= ((double) (alc)/768);
		critDmg+= ((double) (vig)/256);
		if(m.getMentalState() == 2) {
			for(Trait t : trt) {
				// TODO: Wrong Trait-ID, read from file
				//Checks
				if(t.getID() == 3) {
					//
					if(m.getProgress() >= 6 && m.getProgress() < 8) {
						//Distributes the bonus
						dmgCap*= 1.15;
						critChance*= 1.1;
						critDmg*= 1.35;
					} else if (m.getProgress() == 8) {
						dmgCap*= 1.35;
						critChance*= 1.2;
						critDmg*= 1.65;
					}
				}
			}
		}
		return new double[] {dmgCap, critChance, critDmg};
	}

	public final static int calculateItemDamage() {
		return 0;
	}

	/**
	 *
	 * @param fit
	 * @param vig
	 * @param age
	 * @param bld
	 * @return
	 */
	public final static int calculateHealth(int fit, int vig, int age, Blood bld) {
		return new Integer((int) alphaFormula(age, fit, vig, 10, 1.5, bld));
	}

	/**
	 *
	 * @param fit
	 * @param alc
	 * @param age
	 * @param bld
	 * @return
	 */
	public final static int calculateStamina(int fit, int alc, int age, Blood bld) {
		return new Integer((int) alphaFormula(age, fit, alc, 1.5, 2, bld));
	}

	/**
	 *
	 * @param trc
	 * @param m
	 * @param t
	 * @return
	 */
	// TODO: Balancing
	public final static int calculateGrant(int trc, Mind m, TeaType<Trait> t) {
		return new Integer((int) betaFormula(trc));
	}

	/**
	 *
	 * @param att
	 * @return
	 */
	public final static int calculateLethargy(int[] att) {
		double[] temp = new double[att.length];
		for(int i = 0; i < att.length; i++) {
			temp[i] = Math.log(att[i]);
		}
		double incr = (temp[1] + temp[3] + temp[6] + temp[5])*2.56;
		double decr = (temp[0] + temp[2] + temp[4])*1.28;
		double sum = (incr - decr)*0.512;
		if(sum < 1) {
			sum+= Math.abs(sum) + 1;
		}
		return new Integer((int) sum);
	}

	/**
	 *
	 * @param exp
	 * @return
	 */
	public final static int calculateLevel(int exp) {
		SuperReader r = new SuperReader();
		int[] arr = r.DEBUG_fileRegexToIntegerArray("./src/_res/raw_vault/#!exp.txt");
		int tempMin = 0;
		int tempMax = 0;
		for(int i = 0; i < arr.length; i++) {
			tempMin+= arr[i];
			tempMax+= arr[i+1];
			if(exp >= tempMin && exp < tempMax) {
				return i;
			} else {
				continue;
			}
		}
		return 0;
	}

	/**
	 *
	 * @param exp
	 * @param lvl
	 * @return
	 */
	public final static boolean levelUp(int exp, int lvl) {
		gammaFormula(exp, lvl);
		return false;
	}

	/**
	 *
	 * @param hlt
	 * @param trc
	 * @return
	 */
	// TODO: Balancing
	public final static int sacrificeHealth(int hlt, int trc) {
		return ((int) ((hlt/16.0) - (betaFormula(trc)/8.0)));
	}

	/**
	 *
	 * @param sex
	 * @param hght
	 * @param wght
	 * @return
	 */
	public final static double calculateBloodAmount(String sex, double hght, double wght) {
		if(sex.equals("Male")) {
			return new Double((0.3669 * (Math.pow(hght, 3)) + (0.03219 * wght + 0.6041)));
		} else {
			return new Double((0.3561 * (Math.pow(hght, 3)) + (0.03308 * wght + 0.1833)));
		}
	}

	/**
	 *
	 * @param hght
	 * @param wght
	 * @return
	 */
	public final static double calculateBMI(double hght, double wght) {
		return new Double(wght/(Math.pow(hght, 2)));
	}

	/**
	 *
	 * @param s1
	 * @param s2
	 * @return
	 */
	public final static int hashID(String s1, String s2) {
		return Integer.parseInt(Integer.toString(Math.abs((s1 + s2).hashCode())).substring(0, 5));
	}

	/**
	 *
	 * @param age
	 * @param frstAtt
	 * @param secAtt
	 * @param frstFac
	 * @param secFac
	 * @param bld
	 * @return
	 */
	private final static double alphaFormula(int age, int frstAtt, int secAtt, double frstFac, double secFac, Blood bld) {
		double ageFac = 50.0 * (Math.sin(Math.toRadians(age + 15 + 45)));
		return new Double((ageFac + (frstAtt * frstFac) + (secAtt * secFac) * bld.getBloodfactor()) * bld.getRemainingFactor());
	}

	/**
	 *
	 * @param trc
	 * @return
	 */
	private final static double betaFormula(int trc) {
		return new Double(((6.4 + trc) * trc) - ((3.2 + trc) * trc) + (trc / (trc + 16)));
	}

	/**
	 *
	 * @param exp
	 * @param lvl
	 * @return
	 */
	private final static double gammaFormula(int exp, int lvl) {
		//exp += 157.37 * Math.pow(2, lvl/16);
		return new Double(exp + 157.37 * Math.pow(2, lvl/16));
	}
}
