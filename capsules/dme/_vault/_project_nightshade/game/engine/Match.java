package game.engine;

import java.util.regex.Pattern;

import game.asset.util.Asset_Init;

/**
 * The class {@code Match}
 * 
 * @since JDK 1.91 ~ <i>2018</i>
 * @author Burak Günaydin <b>{@code (arsonite)}</b>
 * @see
 */
public class Match {
	
	/** String-array for */
	final String[] arr1, arr2;

	public Match() {
		String[] s = Asset_Init.MATCH();
		arr1 = new String[s.length];
		arr2 = new String[s.length];
		for(int i = 0; i < s.length; i++) {
			String[] arr = toRegex(s[i]);
			arr1[i] = arr[0];
			arr2[i] = arr[1];
		}
	}

	/**
	 * 
	 * 
	 * @param p1
	 * @param p2
	 * @return
	 */
	final Pattern compilePattern(String p1, String p2) {
		return Pattern.compile("^[" + p1 + "]+" + p2 + ".*");
	}

	final boolean match(int i, String input) {
		return compilePattern(arr1[i], arr2[i]).matcher(input).find();
	}
	
	final String[] toRegex(String s) {
		StringBuilder sb = new StringBuilder();
		sb.append(Character.toString(s.charAt(0)).toUpperCase());
		sb.append(sb.substring(0, 1).toLowerCase());
		return new String[] {sb.toString(), s.substring(1, s.length())};
	}

	public final boolean north(String input) { return match(0, input); }
	public final boolean south(String input) { return match(1, input); }
	public final boolean west(String input) { return match(2, input); }
	public final boolean east(String input) { return match(3, input); }

	public final boolean male(String input) { return match(4, input); }
	public final boolean female(String input) { return match(5, input); }

	public final boolean meditate(String input) { return match(6, input); }	
	public final boolean remember(String input) { return match(7, input); }	
	public final boolean rebirth(String input) { return match(8, input); }	
	public final boolean suicide(String input) { return match(9, input); }	
	public final boolean think(String input) { return match(10, input); }	
	public final boolean awake(String input) { return match(11, input); }	

	public final boolean check(String input) { return match(12, input); }	
	public final boolean status(String input) { return match(13, input); }	
	public final boolean mind(String input) { return match(14, input); }	
	public final boolean attributes(String input) { return match(15, input); }	
	public final boolean inventory(String input) { return match(16, input); }	
	public final boolean skills(String input) { return match(17, input); }	
	public final boolean traits(String input) { return match(18, input); }	
	public final boolean focus(String input) { return match(19, input); }	
	public final boolean bloodtype(String input) { return match(20, input); }	
	public final boolean appearance(String input) { return match(21, input); }	

	public final boolean open(String input) { return match(22, input); }	
	public final boolean breach(String input) { return match(23, input); }	
	public final boolean unlock(String input) { return match(24, input); }	
	public final boolean shut(String input) { return match(25, input); }

	public final boolean strike(String input) { return match(26, input); }
}