package _debug.old;

import game.engine.Match;

import teaType.data.TeaType;

public class Main {

    public static void main(String args[]) {

        // Build rooms
        final int WIDTH = 2;
        final int HEIGHT = 2;
        Room[][] room = new Room[WIDTH][HEIGHT];
        Rooms.build(room, WIDTH, HEIGHT);
        int x = 0;
        int y = 0;
        Rooms.print(room, x, y);

        // Load inventory
        TeaType<String> inventory = new TeaType<>();
        Match m = new Match();

        // Start game
        boolean playing = true;
        while (playing) {
        	
            String input = Input.getInput();
            // Movement commands
            if (m.north(input)) {
                if (y > 0) {
                    Rooms.print(room, x, y);
                } else {
                    System.out.println("You can't go that way.");
                }
            } else if (m.south(input)) {
                if (y < HEIGHT - 1) {
                    y++;
                    Rooms.print(room, x, y);
                } else {
                    System.out.println("You can't go that way.");
                }
            } else if (m.east(input)) {
                if (x > 0) {
                    x--;
                    Rooms.print(room, x, y);
                } else {
                    System.out.println("You can't go that way.");
                }
            } else if (m.west(input)) {
                if (x < WIDTH - 1) {
                    x++;
                    Rooms.print(room, x, y);
                } else {
                    System.out.println("You can't go that way.");
                }
            }

            // Look commands
            else if (input.equals("look")) {
                Rooms.print(room, x, y);
            }

            // Get commands
            else if (input.length() > 4  && input.substring(0, 4).equals("get ")) {
            	if (input.substring(0, input.indexOf(' ')).equals("get")) {
            		if (input.substring(input.indexOf(' ')).length() > 1) {
            			String item = input.substring(input.indexOf(' ') + 1);
                    	Inventory.checkItem(x, y, item, inventory, room);
            		}	
            	}
            }

            // Inventory commands
            else if (input.equals("i") || input.equals("inv")
                    || input.equals("inventory")) {
                Inventory.print(inventory);
            }
            
            // Quit commands
            else if (input.equals("quit")) {
                System.out.println("Goodbye!");
                playing = false;

            // Catch-all for invalid input
            } else {
                System.out.println("You can't do that.");
            }
        }
        System.exit(0);
    }
}
