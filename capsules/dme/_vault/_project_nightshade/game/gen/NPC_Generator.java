package game.gen;

import java.util.Random;

import game.asset.NPC;
import game.asset.core.Appearance;
import game.asset.core.Attributes;
import game.asset.core.Mind;
import teaType.util.io.Reader;

public class NPC_Generator {
	private static String m = "./src/_res/dump/#!m_names.txt";
	private static String f = "./src/_res/dump/#!f_names.txt";
	private static String l = "./src/_res/dump/#!lastnames.txt";
	private static Reader r = new Reader();
	private static String[] mArr = r.stringArray(m);
	private static String[] fArr = r.stringArray(f);
	private static String[] lArr = r.stringArray(l);

	public static NPC generateNPC() throws Exception {
		Random rnd = new Random();

		NPC npc;

		Appearance app = new Appearance();

		Attributes att = new Attributes();
		att.random(rnd.nextInt(85));

		Mind mnd = new Mind();
		mnd.random();

		if(rnd.nextInt(2) == 0) {
			npc = new NPC((mArr[rnd.nextInt(mArr.length)] + " " + lArr[rnd.nextInt(lArr.length)]),
					"Human", "Male", ((int) (Math.random()*34+16)), app, att, mnd, false);
		} else {
			npc = new NPC((fArr[rnd.nextInt(fArr.length)] + " " + lArr[rnd.nextInt(lArr.length)]),
					"Human", "Female", ((int) (Math.random()*34+16)), app, att, mnd, false);
		}
		app.setRandom(npc.getSex());
		return npc;
	}

	public static NPC[] generateNPCS(int amount) throws Exception {
		NPC[] npcArr = new NPC[amount+1];
		for(int i = 0; i <= amount; i++) {
			npcArr[i] = generateNPC();
		}
		return npcArr;
	}
}