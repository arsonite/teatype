package game.engine.npc;

import java.util.TeaType;

import game.asset.NPC;
import game.asset.Player;

import teaType.data.BiPrimitive;

import teaType.util.StreamBuffer;

class Fight {
	private int count, round, elapse;
	private BiPrimitive dmg;
	private TeaType<NPC> list;

	public Fight(Player p, NPC... nArr) throws Exception {
		StreamBuffer.fixConsole();
		count = round = elapse = 0;

		/*
		int[] let = new int[nArr.length+1];
		let[0] = p.getAttributesObject().getLethargy();
		for(int i = 1; i < let.length; i++) {
			let[i] = nArr[i].getAttributesObject().getLethargy();
		}
		*/
		
		list = new TeaType<NPC>();
		for(NPC n : nArr) {
			list.add(n);
		}

		// TODO: Good condition to exit the fight
		while(!p.isDead() && !list.isEmpty()) {
			fight(p, nArr);
			round++;
		}
		
		nArr = new NPC[list.size()];
		for(int i = 0; i < nArr.length; i++) {
			nArr[i] = list.get(i);
		}
		
		if(!p.isDead()) {
			System.err.println("\n" + p.getName() + " won!");
		} else {
			System.err.println("\n" + p.getName() + " lost...");
		}
		return;
	}

	private void fight(Player p, NPC... nArr) {
		StreamBuffer.fixConsole();
		for(NPC n : nArr) {
			if(count % p.getAttributesObject().getLethargy() == 0 && count % n.getAttributesObject().getLethargy() == 0) {
				System.err.print("Both hit their lethargy! Let's roll: ");
				double random = Math.random();
				System.out.print(random);
				System.out.flush();
				if(random < 0.5) {
					dmg = p.inflictDamage();
					n.takeDamage((double) dmg.getSecond());
					System.out.printf("!%n%d It's %s's turn! %s did %.0f damage! %s has %d health left.%n",
							count, p.getName(), p.getName(), dmg.getSecond(), n.getName(), n.getHealth());
				} else {
					dmg = n.inflictDamage();
					p.takeDamage((double) dmg.getSecond());
					System.out.printf("!%n%d It's %s's turn! %s did %.0f damage! %s has %d health left.%n",
							count, n.getName(), n.getName(), dmg.getSecond(), p.getName(), p.getHealth());
				}
			} else if(count % p.getAttributesObject().getLethargy() == 0) {
				dmg = p.inflictDamage();
				n.takeDamage((double) dmg.getSecond());
				System.out.printf("%d It's %s's turn! %s did %.0f damage! %s has %d health left.%n",
						count, p.getName(), p.getName(), dmg.getSecond(), n.getName(), n.getHealth());
			} else if(count % n.getAttributesObject().getLethargy() == 0) {
				dmg = n.inflictDamage();
				p.takeDamage((double) dmg.getSecond());
				System.out.printf("%d It's %s's turn! %s did %.0f damage! %s has %d health left.%n",
						count, n.getName(), n.getName(), dmg.getSecond(), p.getName(), p.getHealth());
			}
			if((boolean) dmg.getFirst()) {
				System.err.println("Critical Hit! Ouch!");
			}
			dmg.setFirst(false);
			dmg.setSecond(0);
			if(n.isDead() && list.contains(n)) {
				list.remove(n);
				System.err.println(n.getName() + " is dead.");
				continue;
			} else if(p.isDead()){
				System.err.println(p.getName() + " is dead.");
				return;
			} else {
				count++;
			}
		}
	}

	/*
	public Fight(Character_I... c) {
	}
	 */

	private void measureFightTime() {
	}

	private void displayFightTime() {
	}
}
