/*
package util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import teaType.data.BiPrimitive;
import teaType.data.TeaType;

import teaType.util.io.Reader;

public class SuperReader extends Reader {
	// TODO: Complete and efficient Generalization and overhaul

	final Pattern CAT = Pattern.compile("#.*#");
	final Pattern TYPE = Pattern.compile("!.*!");
	final Pattern CON = Pattern.compile("-.*-");
	final Pattern END = Pattern.compile(";;");
	final Pattern STR = Pattern.compile(".*String.*");
	final Pattern APPCOL = Pattern.compile(".*app_color.*");

	private Matcher cat, type, con, end, str, appCol;


	private String[] arr;
	private StringBuilder sb;
	@SuppressWarnings("rawtypes")
	private TeaType l;
	private TeaType<TeaType<?>> allList;
	private TeaType<TeaType<String>> strList;

	public SuperReader() {
	}

	private final void compile(String s) {
		cat = CAT.matcher(s);
		type = TYPE.matcher(s);
		con = CON.matcher(s);
		end = END.matcher(s);
		str = STR.matcher(s);
		appCol = APPCOL.matcher(s);
	}
	
	private final void searchPattern(String s) {
	}
	
	private final void cutListEnd(boolean type) {
		if(type) {
			if(end.find()) {
				l.remove(l.size()-1);
				allList.add(l);
			}	
		} else {
			if(end.find()) {
				l.remove(l.size()-1);
				strList.add(l);
			}	
		}
		
	}

	public TeaType<TeaType<?>> DEBUG_fileRegexToTeaType() {
		arr = stringArray("./res/raw/#!app.txt");

		allList = new TeaType<TeaType<?>>();

		for(String s : arr) {
			compile(s);
			sb = new StringBuilder(s);
			if(str.find()) {
				s = str.group();
				l = new TeaType<String>();
				continue;
			} else if (appCol.find()) {
				s = appCol.group();
				l = new TeaType<BiPrimitive>();
				continue;
			} else {
				if(cat.find()) {
					s = cat.group();
				} else if (type.find()) {
					s = type.group();
				} else if(con.find()) {
					s = con.group();
				}
				s = sb.substring(1, s.length()-1);
				l.add(s);
			}
			cutListEnd(true);
		}
		return allList;
	}

	public TeaType<TeaType<String>> DEBUG_fileRegexToStringTeaType(String path, boolean skipCat) {
		arr = stringArray(path);
		strList = new TeaType<TeaType<String>>();
		l = new TeaType<String>();

		for(String s : arr) {
			compile(s);
			sb = new StringBuilder(s);
			if(str.find()) {
				s = str.group();
				l = new TeaType<String>();
				continue;
			} else {
				if(cat.find()) {
					s = cat.group();
					if(skipCat) {
						continue;
					}
				} else if (type.find()) {
					s = type.group();
				} else if(con.find()) {
					s = con.group();
				}
				s = sb.substring(1, s.length()-1);
				l.add(s);
			}
			cutListEnd(false);
		}
		return strList;
	}

	public int[] DEBUG_fileRegexToIntegerArray(String path) {
		arr = stringArray(path);
		TeaType<String> list = new TeaType<String>();
		for(String s : arr) {
			compile(s);
			sb = new StringBuilder(s);
			if(cat.find()) {
				s = cat.group();
			} else if (type.find()) {
				s = type.group();
			} else if(con.find()) {
				s = con.group();
			}
			s = sb.substring(1, s.length()-1);
			list.add(s);
		}
		if(end.find()) {
			list.remove(list.size()-1);
			list.remove(0);
			list.remove(0);
		}
		
		arr = new String[list.size()];
		int[] intArr = new int[arr.length];
		for(int i = 0; i < arr.length; i++) {
			arr[i] = list.get(i);
			intArr[i] = Integer.parseInt(arr[i]);
		}
		return intArr;
	}
}
*/