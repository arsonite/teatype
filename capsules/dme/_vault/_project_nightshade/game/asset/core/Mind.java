package game.asset.core;

import java.util.TeaType;

import teaType.util.Array;
import util.SuperReader;

public class Mind {
	// TODO: Remove limit on negative and positive end, or lock both extremes from increase or decrease
	private final String[] mntlStat;
	private final String[] mntlProg;
	private String[] pol;
	private final TeaType<TeaType<String>> polArr;
	private int sta;
	private int prg;
	private int mtl;

	public Mind() {
		SuperReader r = new SuperReader();
		TeaType<TeaType<String>> temp = r.DEBUG_fileRegexToStringTeaType("./res/raw/#!mnd.txt", true);
		
		mntlStat = Array.fromTeaType(temp.get(0));
		mntlProg = Array.fromTeaType(temp.get(1));
		
		mtl = 1000;
		setProgress();
		polArr = r.DEBUG_fileRegexToStringTeaType("./res/raw/#!pol.txt", false);
	}
	
	public void random() {
		randomStats();
		randomCivic();
	}

	public void randomStats() {
		mtl = (int) (Math.random()*2000+0);
		setProgress();
	}

	// TODO: Add civic conditions and group civic beliefs together in groups with picking one of each group
	public void randomCivic() {
		
		pol = new String[polArr.size()];
		for(int i = 0; i < polArr.size(); i++) {
			int size = (int) (Math.random()*(polArr.get(i).size()-1)+1);
			pol[i] = polArr.get(i).get(size);
		}
	}

	public void debug() {
		mtl = 0;
		sta = 0;
		prg = 0;
	}

	public void addMadness(int m) {
		if((mtl + m) < 2000) {
			mtl+= m;
		} else {
			mtl = 2000;
		}
		setProgress();
	}

	public void addGoodwill(int m) {
		if((mtl - m) > 0) {
			mtl-= m;
		} else {
			mtl = 0;
		}
		setProgress();
	}

	public void setMind(int i) {
		if(i >= 0 && i <= 2000) {
			mtl = i;
		}
		setProgress();
	}

	private void setProgress() {
		switch(mtl/250) {
		case 0: prg = 0; break;
		case 1: prg = 1; break;
		case 2: prg = 2; break;
		case 3: prg = 3; break;
		case 4: prg = 4; break;
		case 5: prg = 5; break;
		case 6: prg = 6; break;
		case 7: prg = 7; break;
		case 8: prg = 8; break;
		}
		setMentalState();
	}

	private void setMentalState() {
		if(prg <= 2) {
			sta = 0;
		} else if (prg > 2 && prg <= 5) {
			sta = 1;
		} else {
			sta = 2;
		}
	}

	public int getMentalState() { return sta; }
	public int getProgress() { return prg; }

	public String getMentalStateToString() { return mntlStat[sta]; }
	public String getProgressToString() { return mntlProg[prg]; }
	
	public String[] getCivicBeliefs() { return pol; }
	
	public TeaType<TeaType<String>> DEBUG_displayAllCivicOptions() { return polArr; }

	public boolean isGood() {
		if (sta == 0) {
			return true;
		}
		else {
			return false;
		}
	}

	public boolean isNormal() {
		if (sta == 1) {
			return true;
		} else {
			return false;
		}
	}

	public boolean isEvil() {
		if (sta == 2) {
			return true;
		}else {
			return false;
		}
	}
}