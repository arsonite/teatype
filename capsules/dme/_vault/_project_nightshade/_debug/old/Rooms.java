package _debug.old;

import teaType.data.TeaType;

class Rooms {

    public static void build(Room[][] room, final int WIDTH, final int HEIGHT) {

    	// Initialize rooms (a 2D array)
        for (int i = 0; i < WIDTH; i++) {
            for (int j = 0; j < HEIGHT; j++) {
                room[i][j] = new Room(i, "", "", null);
            }
        }

        room[0][0].setNumber(1);
        room[0][0].setName("Living Room");
        room[0][0].setDescription("You are in your living room.");
        room[0][0].setItems("wallet");
        room[0][0].setItems("remote");

        room[0][1].setNumber(2);
        room[0][1].setName("Bedroom");
        room[0][1].setDescription("You are in your bedroom. Your closet is slightly ajar.");
        room[0][1].setItems("keys");
        room[0][1].setItems("flashlight");

        room[1][0].setNumber(3);
        room[1][0].setName("Kitchen");
        room[1][0].setDescription("You are in your kitchen.");
        room[1][0].setItems("pop tarts");
        room[1][0].setItems("soda");

        room[1][1].setNumber(4);
        room[1][1].setName("Bathroom");
        room[1][1].setDescription("You are in your bathroom.");
        room[1][1].setItems("toilet paper");
        room[1][1].setItems("magazine");
    }

    public static void print(Room[][] room, int x, int y) {

        System.out.println(room[x][y].getDescription());
        System.out.println("You see: " + room[x][y].getItems());
        System.out.println();
    }

    // Remove item from room when added to inventory
    public static void removeItem(Room[][] room, int x, int y, String item) {
    	
    	room[x][y].deleteItem(item);
    }
}

class Room {

    private int number;
    private String name;
    private String description;
    public TeaType<String> items = new TeaType<>();

    public Room(int number, String name, String description,
            TeaType<String> items) {
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public int getNumber() {
        return this.number;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return this.description;
    }

    public void setItems(String item) {
        this.items.add(item);
    }

    public void deleteItem(String item) {
        this.items.remove(item);
    }

    public TeaType<String> getItems() {
        return this.items;
    }
}
