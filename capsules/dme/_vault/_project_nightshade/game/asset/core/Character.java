package game.asset.core;

import java.util.TeaType;

import game.asset.util.Asset;

import game.engine.Match;

import game.engine.exceptions.ArmorLimitException;
import game.engine.exceptions.InvalidSexException;

import teaType.data.BiPrimitive;

import teaType.util.rigid.Random;

import util.Functions;

public class Character extends Asset {
	protected String sex, orig, titl;
	protected final String[] pn, PN;
	protected int lvl, exp, age, hlt, stm, grn, gold, maxStm, maxHlt, maxGrn;
	protected final int EXP_MAX = 128256512, ARM_MAX = 512;
	protected double arm, dmgIn;
	protected double[] baseDmg, dmg;
	protected boolean flag, gift;
	protected Item fist;
	protected TeaType<Item> eq;
	protected Appearance app;
	protected Attributes att;
	protected Blood bld;
	protected TeaType<Conjuration> con;
	protected Inventory inv;
	protected Mind mnd;
	protected TeaType<Status> sts;
	protected TeaType<Trait> trt;
	protected Match m;

	public void setName(String name) { this.name = name; }

	public void setOrigin(String orig) { this.orig = orig; }

	public void setAge(int age) { this.age = age; }

	public void setAppearance() { }

	public Character(String name, String orig, String sex, int age, Appearance app,  Attributes att, Mind mnd) throws Exception {
		super(name, String.format("%s %s %s", name, orig, sex));
		pn = PN = new String[3];
		arm = 0.0;
		lvl = 1;
		baseDmg = dmg = new double[3];
		m = new Match();
		gold = 0;

		// temporary //

		this.app = app;
		this.att = att;
		this.mnd = mnd;

		///////////////

		this.name = name;
		this.orig = orig;
		setSex(sex);
		this.age = age;
		if(att.getTranscendence() >= 25) {
			gift = true;
			calculateGrant();
		} else {
			gift = false;
		}
		this.bld = new Blood(getSex(), app.getHeight(), app.getWeight());
		sts = new TeaType<Status>();
		trt = new TeaType<Trait>();
		con = new TeaType<Conjuration>();
		inv = new Inventory();
		fist = new Item("Fist", "Your very own fist. Big deal.");
		fist.setUsability(true, true, false, false, true, true, false, false, true, true);
		fist.setValues(0, 0, 0, 0, 0);
		fist.setDamageStats(0, 0, 0);
		fist.setEquipCode(8);
		eq = new TeaType<Item>(21);
		for(int i = 0; i < 21; i++) {
			eq.add(i, null);
		}
		equipFist(2, true);
		calculateAge();
		calculateHealth();
		calculateStamina();
		calculateDamage();
	}



	private final void equipFist(int side, boolean right) {
		switch(side) {
		case 0:
			break;
		case 1:
			if(right) {
				eq.set(11, fist);
			} else {
				eq.set(8, fist);
			}
			break;
		case 2:
			eq.set(8, fist);
			eq.set(11, fist);
			break;
		}
	}

	protected final void calculateLevel() {
		//Functions.calculateLevel(exp, EXP_MAX);
	}

	public void levelUp(int exp, int atr) {
		att.levelUp(exp, atr);
	}

	public void setLevel(int lvl) {

	}

	public void setExperience(int exp) {

	}

	// TODO: StringReader for pronoun-set
	public void setSex(String sex) throws InvalidSexException {
		// Statement for preventing empty sex-strings
		if(!m.male(sex) && !m.female(sex)) {
			if(new Random().nextInt(2) == 0) {
				sex = "Male";
			} else {
				sex = "Female";
			}
		}
		if(m.male(sex)) {
			this.sex = "Male";
			// TODO: Probably better solution possible/superReader read-in
			pn[0] = "he";
			pn[1] = "him";
			pn[2] = "his";
			PN[0] = "He";
			PN[1] = "Him";
			PN[2] = "His";
		} else if(m.female(sex)) {
			this.sex = "Female";
			pn[0] = "she";
			pn[1] = "her";
			pn[2] = "hers";
			PN[0] = "She";
			PN[1] = "Her";
			PN[2] = "Hers";
		}
		/*} else {
			throw new InvalidSexException(null);
		}*/
	}

	protected final void calculateHealth() { maxHlt = hlt = Functions.calculateHealth(att.getFitness(), att.getVigor(), getAge(), bld); }

	protected final void calculateStamina() { maxStm = stm = Functions.calculateStamina(att.getFitness(), att.getAlacrity(), getAge(), bld); }

	protected final void calculateDamage() {
		double[] itemDmg = new double[3];
		for(int i = 0; i < itemDmg.length; i++) {
			itemDmg[i] = eq.get(8).getDamageStats()[i] + eq.get(11).getDamageStats()[i];
		}
		baseDmg = Functions.calculateDamage(att.getVigor(), att.getAlacrity(), mnd, trt);
		for(int i = 0; i < dmg.length; i++) {
			dmg[i] = baseDmg[i] + itemDmg[i];
		}
	}

	protected final void calculateGrant() { maxGrn = grn = Functions.calculateGrant(att.getTranscendence(), mnd, trt); }

	public void useConjuration(int spl_ID) {
		for(int i = 0; i < con.size(); i++) {
			if(con.get(i).getID() == spl_ID) {
				grn-= con.get(i).getCost();
			}
		}
		// TODO: Exception
	}

	// TODO: Convert to id confirmation not entire object comparison like above method
	public void addConjuration(Conjuration c) {
		if(!(con.contains(c))) {
			con.add(c);
		}
	}

	public void removeConjuration(Conjuration c) {
		if(!(con.contains(c))) {
			con.remove(c);
		}
	}

	public void addStatus(Status s) {
		if(!sts.contains(s)) {
			sts.add(s);
		}
	}

	public void removeStatus(Status s) {
		if(sts.contains(s)) {
			sts.remove(s);
		}
	}

	public void removeAllStatus() {
		if(!sts.isEmpty()) {
			sts.clear();
		}
	}

	public Status getStatus(int id) {
		for(Status s : sts) {
			if(s.getID() == id) {
				return s;
			}
		}
		return null;
	}

	public TeaType<Status> getAllStatus() {
		return sts;
	}

	public void addTrait(Trait t) {
		if(!trt.contains(t)) {
			trt.add(t);
		}
	}

	public void removeTrait(Trait t) {
		if(trt.contains(t)) {
			trt.remove(t);
		}
	}

	public void removeAllTraits() {
		if(!trt.isEmpty()) {
			trt.clear();
		}
	}

	public Trait getTrait(int id) {
		for(Trait t : trt) {
			if(t.getID() == id) {
				return t;
			}
		}
		return null;
	}

	public TeaType<Trait> getAllTraits() {
		return trt;
	}

	public BiPrimitive inflictDamage() {
		return Functions.inflictDamage(dmg);
	}

	public void addArmor(int arm) throws ArmorLimitException {
		if((this.arm + (double) arm/ARM_MAX) <= 1.0) {
			this.arm+= (double) arm/ARM_MAX;
		} else {
			//Finish ArmorLimitException and its dependencies
			throw new ArmorLimitException(Double.toString(arm));
		}
	}

	public void randomArmor() {
		arm = Math.random();
	}

	public void randomArmorWithMax(int max) throws ArmorLimitException {
		if((double) max/ARM_MAX <= 1.0) {
			// TODO: Write more efficient algorithm
			do {
				arm = Math.random();
			} while(arm > (double) max/ARM_MAX);
		} else {
			throw new ArmorLimitException(Double.toString(arm));
		}
	}

	public void addItem(Item i) {
		if(!(inv.containsItem(i))) {
			inv.add(i);
		}
	}

	public void removeItem(Item i) {
		if(inv.containsItem(i)) {
			inv.remove(i);
		}
	}

	public void equipItem(Item i) {
		// TODO: Condition to check for already full slot
		int code = i.getEquipCode();
		if(inv.containsItem(i)) {
			eq.set(code, i);
			inv.remove(i);
			calculateDamage();
		}
	}

	public void unequipItem(int code) {
		if(eq.get(code) != fist) {
			inv.add(eq.get(code));;
			eq.remove(code);
			if(code == 8) {
				equipFist(1, false);
			} else if(code == 11) {
				equipFist(1, true);
			}
		}
		calculateDamage();
	}

	public void takeDamage(double dmgIn) {
		dmgIn-= (dmgIn * arm);
		this.dmgIn = dmgIn;
		hlt-= dmgIn;
		if(hlt <= 0) {
			hlt = 0;
		}
	}

	public void gainGrant(int itrs) {
		if(gift) {
			int sacr = Functions.sacrificeHealth(hlt, att.getTranscendence());
			int gain = (int) (Functions.calculateGrant(att.getTranscendence(), mnd, trt) * Math.sin(Math.toRadians((att.getTranscendence() / 10.0) + 20)));
			int temp = gain;
			boolean grnCon = (grn + gain) <= maxGrn;
			boolean hltCon = (hlt - sacr) >= 0;
			boolean tempCon = (grn + temp) <= maxGrn;
			if(grnCon && hltCon) {
				for(int i = 0; i < itrs; i++) {
					if(hltCon && tempCon) {
						hlt-= sacr;
						grn+= gain;
						temp = gain;
						tempCon = (grn + (temp*= (i + 1))) <= maxGrn;
					} else {
						if(hltCon) {
							hlt-= sacr;
							grn+= temp - ((temp + grn) - maxGrn);
						}
						break;
					}
				}
			}
		}
	}

	public void calculateAge() {
		age*= 256;
	}

	public void age(int days) {
		age+= days;
		bld.regain(days);
	}

	// TODO: Add conditions
	public void setBloodState(int state) {
		bld.setBloodState(state);
	}

	public void increaseIllness(boolean b, int incr) {
		bld.increaseIllness(b, incr);
	}

	public void randomBloodState() {

	}

	public void bleed(int amount) {
		bld.bleed(amount);
		calculateHealth();
	}

	public String getBloodtype() {
		return new String(bld.getBloodtype());
	}

	public int getBloodState() {
		return new Integer(bld.getBloodState());
	}

	public double getBloodAmount() {
		return new Double(bld.getAmount());
	}

	public double getBloodfactor() {
		return new Double(bld.getBloodfactor());
	}

	public boolean isDead() {
		if(hlt <= 0 || bld.isBledOut()) {
			return true;
		} else {
			return false;
		}
	}

	public boolean isExhausted() {
		if(stm == 0) {
			return true;
		} else {
			return false;
		}
	}

	public String getName() {
		return name;
	}

	public String getOrigin() {
		return orig;
	}

	public String getSex() {
		return sex;
	}

	public String getTitle() {
		return new String(att.setTitle());
	}

	public int getLevel() {
		return lvl;
	}

	public int getExperience() {
		return exp;
	}

	public int getAge() {
		return (age / 256);
	}

	public int getHealth() {
		return hlt;
	}

	public int getStamina() {
		return stm;
	}

	public int getGrant() {
		return grn;
	}

	public int getArmor() {
		return new Integer((int) (arm * 512));
	}

	public double getArmorFactor() {
		return arm;
	}

	public double getBaseDamage() {
		return baseDmg[0];
	}

	public double getBaseCriticalChance() {
		return baseDmg[1];
	}

	public double getBaseCriticalDamage() {
		return baseDmg[2];
	}

	public double getDamage() {
		return dmg[0];
	}

	public double getCriticalChance() {
		return dmg[1];
	}

	public double getCriticalDamage() {
		return dmg[2];
	}

	public double getDamageTaken() {
		return dmgIn;
	}

	public double[] getBaseDamageStats() {
		return baseDmg;
	}

	public double[] getDamageStats() {
		return dmg;
	}

	public String getSmallPronoun(int i) {
		return new String(pn[i-1]);
	}

	public String getCapitalPronoun(int i) {
		return new String(PN[i-1]);
	}

	public BiPrimitive[] getAllAttributes(boolean let) {
		return att.getAttributes(let);
	}

	public Item getCurrentItem(int code) {
		return eq.get(code);
	}

	public Appearance getAppearanceObject() {
		return app;
	}

	public Attributes getAttributesObject() {
		return att;
	}

	public Mind getMindObject() {
		return mnd;
	}

	public String retrieveStats() {
		StringBuilder sb = new StringBuilder();
		sb.append("Status profile (");
		if(flag) {
			sb.append("Player");
		} else {
			sb.append("NPC");
		}
		sb.append("):\n------------------------\n");
		sb.append(String.format("Name: %s %nOrigin: %s %nSex: %s %nAge: %d %nLevel: %d %nArmor: %d %nHealth: %d %nStamina: %d %nGrant: %d%n",
				getName(), getOrigin(), getSex(), getAge(), getLevel(), getArmor(), getHealth(), getStamina(), getGrant()));

		sb.append("\n▪ Appearance:\n");
		sb.append(String.format("   » %.2fm %n   » %.1fkg%n   » BMI-Score: %.1f %n", app.getHeight(), app.getWeight(), app.getBMI()));
		for(int i = 0; i < app.getAppearance().size(); i++) {
			if(getSex().equals("Female") && (i == 8 || i == 9)) {
				continue;
			}
			sb.append(String.format("   » %s: %s %n", app.getList().get(i).get(0), app.getAppearance().get(i)));
		}

		sb.append("\n▪ Attributes:");
		for(BiPrimitive a : att.getAttributes(true)) {
			sb.append("\n   » " + a.getFirst() + " - " + a.getSecond());
		}
		sb.append("\n");

		sb.append("\n▪ Bloodtype:\n");
		sb.append(String.format("   » Blood-Status: %s%n   » Blood-State: %d%n   » Bloodfactor: %.2f %n   » Blood-Amount: %.1f%n",
				getBloodtype(), getBloodState(), getBloodfactor(), getBloodAmount()));

		if(!(con.isEmpty())) {
			sb.append("\n");
			sb.append("\n▪ Conjurations:\n");
			for(int i = 0; i < con.size(); i++) {
				sb.append(String.format("      → %s - \"%s\" (Spell-ID: %s)%n", con.get(i).getName(), con.get(i).getDescription(), con.get(i).getID()));
			}
			sb.append("\n");
		}

		if(flag) {
			sb.append("\n▪ Focus:");
			sb.append("\n");
		}

		sb.append("\n▪ Inventory:\n");
		sb.append(String.format("   » Currently equipped: %s%n   » Item-Stache: %n", eq.get(11).getName()));
		for(Item i : eq) {
			if(i != null) {
				//sb.append(String.format("On ", ));
			}
		}
		for(Item i : inv.getInventory()) {
			sb.append(String.format("      → %s - \"%s\" (Item-ID: %s)%n", i.getName(), i.getDescription(), i.getID()));
		}

		sb.append("\n▪ Mind:\n");
		String.format("   » Mind-State: %s, %d%n   » Mind-Progression: %s, %d%n",
				mnd.getMentalStateToString(), mnd.getMentalState(), mnd.getProgressToString(), mnd.getProgress());

		sb.append("   » Civic beliefs:\n");
		for(int i = 0; i < mnd.getCivicBeliefs().length; i++) {
			sb.append(String.format("      → %s: %s%n", mnd.DEBUG_displayAllCivicOptions().get(i).get(0), mnd.getCivicBeliefs()[i]));
		}

		if(flag) {
			sb.append("\n▪ Reputation:\n");
			sb.append("\n");
			sb.append("\n▪ Skills:\n");
			sb.append("\n");
		}

		sb.append("\n▪ Status:\n");
		sb.append("\n");

		sb.append("\n▪ Traits:\n");
		sb.append("\n");

		sb.append(String.format("%n▪ Damage-Stats: %n   » Base Damage:     %.0f = %.0f + %.0f Item-Damage %n   "
				+ "» Critical Damage: %.0f = Base + %.2f%% + %.2f%% Item-Critical-Damage %n"
				+ "   » Critical Chance: %.2f%% = %.2f%% + %.2f%% Item-Critical-Chance %n",
				getDamage(), getBaseDamage(), (eq.get(8).getDamage() + eq.get(11).getDamage()), (getBaseDamage() * getCriticalDamage()),
				(100 * getBaseCriticalDamage() - 100), (100 * (eq.get(8).getCriticalDamage() + eq.get(11).getCriticalDamage())), (getCriticalChance() * 100),
				(getBaseCriticalChance() * 80), ((eq.get(8).getCriticalChance() + eq.get(11).getCriticalChance()) * 100)));
		return sb.toString();
	}
}
