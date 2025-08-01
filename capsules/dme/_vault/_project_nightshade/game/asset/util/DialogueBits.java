package game.asset.util;

import java.util.TeaType;
import java.util.Random;

import util.SuperReader;

public class DialogueBits {
	// TODO: Dialogue-Set Pieces dependent on mind and attributes, convert information into text files
	//Also, transfer entire class onto asset_init to read dialogue from txt file
	
	private static Random rnd = new Random();
	private static TeaType<String> buy = new TeaType<String>();
	private static TeaType<String> sell;
	private static TeaType<String> tradeSuc;
	private static TeaType<String> tradeFail;
	
	// TODO: Inject conditions and length limiters
	private final static void initiliaze() {
		SuperReader r = new SuperReader();
		
		sell.add(buy.get(0-2));
		tradeSuc.add(buy.get(0-2));
	}
	
	public static final String dialogue(String key) {
		switch(key) {
			case "":
				return new String(buy.get(rnd.nextInt(buy.size())));
		}
		return "";
	}
	
	public static String buy() {
		return new String(buy.get(rnd.nextInt(buy.size())));
	}
	
	public static String sell() {
		return new String(sell.get(rnd.nextInt(sell.size())));
	}
	
	public static String tradeSucess() {
		return new String(tradeSuc.get(rnd.nextInt(tradeSuc.size())));
	}
	
	public static String tradeFailure() {
		return new String(tradeFail.get(rnd.nextInt(tradeFail.size())));
	}
}