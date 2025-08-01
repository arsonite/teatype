class Body {
    constructor() {
        this.app = null;
        this.eq = null;
        this.fist = null;
    }
}

module.exports = Body;

/*
private Hashtable<Object, Object> t;
private double hght, wght, bmi;

public Appearance() {
	t = new Hashtable<Object, Object>();
}

public void setHeight(int hght) {
	this.hght = hght;
	calculateBMI();
}

public void setWeight(double wght) {
	this.wght = wght;
	calculateBMI();
}

public void setBodyMeasurements(int hght, double wght) {
	setHeight(hght);
	setWeight(wght);
	calculateBMI();
}

// TODO: create and fill method in accordance to necessary app_hash_util indices
public void setApperance() {
}

// TODO: Link with BMI and average as conditions and references for realistic proportions
public void setRandom(String sex) {
	// TODO: More efficient algorithm
	TeaType<TeaType<?>> temp = Asset_Init.APP();

	while(bmi <= 23.0 || bmi >= 26.0) {
		hght = Math.random()*60+150;
		wght = Math.random()*100000+35000;
		calculateBMI();
	}
	for(int i = 0; i < temp.size(); i++) {
		if(sex.equals("Female") && (i == 8 || i == 9)) {
			Object o = "";
			t.put(i, o);
			continue;
		}
		int size = (int) (Math.random()*(temp.get(i).size()-1)+1);
		Object o = temp.get(i).get(size);
		t.put(i, o);
	}
}

private final void calculateBMI() { bmi = Functions.calculateBMI(getHeight(), getWeight()); }

public String getHeightInMeter() { return getHeight() + "m"; }
public String getWeightInKG() { return getWeight() + "kg"; }

public double getHeight() { return (hght/100); }
public double getWeight() { return (wght/1000); }
public double getBMI() { return bmi; }

public Hashtable<Object, Object> getAppearance() { return t; }

public TeaType<TeaType<?>> getList() { return Asset_Init.APP(); }

public void DEBUG_printAvailableOptions() {
	PrintWriter out = new PrintWriter(System.out, true);
	Set<Object> keys = t.keySet();
	for(Object o : keys) {
		out.println(t.get(o).toString());
	}
}
*/