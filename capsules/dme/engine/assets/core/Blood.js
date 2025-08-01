class Blood {
    constructor() {
    }
}

module.exports = Blood;

/*
private String bldType;
// TODO: Super-Reader Implementation
final String[] bldHlt = {
		"Pure", "Healthy", "Polluted", "Infected", "Ill", "Incurable", "Fatal", "Occult", "Mutated"
};
private int state;
private double amount, bldFac;
private final double MAX_AMOUNT;
private boolean bledOut, bleed;

public Blood(String sex, double height, double weight) {
	setBloodState(1);
	MAX_AMOUNT = amount = Functions.calculateBloodAmount(sex, height, weight);
	bledOut = bleed = false;
}

protected void setBloodState(int state) {
	if(state <= bldHlt.length) {
		this.state = state;
	} else {
		this.state = state = 6;
	}
	bldType = bldHlt[state];
	setBloodFactor();
}

private void setBloodFactor() {
	switch(state) {
	case 0: bldFac = 1.175; break;
	case 1: bldFac = 1.0; break;
	case 2: bldFac = 0.9; break;
	case 3: bldFac = 0.85; break;
	case 4: bldFac = 0.675; break;
	case 5: bldFac = 0.5; break;
	case 6: bldFac = 0.35; break;
	case 7: bldFac = 1.25; break;
	case 8: bldFac = 1.5; break;
	}
}

protected void increaseIllness(boolean b, int incr) {
	if(b) {
		setBloodState((state+incr));
	} else {
		setBloodState((state-incr));
	}
}

// TODO: Integration into status object + chance to bleed on hit, based on armor and damage
public void bleed(int amountInMilli) {
	if(amount != 0) {
		amount-= (double) amountInMilli/1000;
		bleed = true;
	} else {
		bleed = false;
		bledOut = true;
	}
}

// TODO: Notification, that you regained x blood or that you still bleed
protected void regain(int days) {
	if(!bleed) {
		amount+= (int) ((Math.random()*40+30) * days);
	}
}

public String getBloodtype() { return bldType; }

public int getBloodState() { return state; }

public double getAmount() { return amount; }
public double getBloodfactor() { return bldFac; }
public double getRemainingFactor() { return (amount / MAX_AMOUNT); }

public boolean isBledOut() {
	if(bledOut) {
		return true;
	} else {
		return false;
	}
}
*/