let lvl = 25;

let player = new Player(
    'Burak Günaydin',
    'The main character.',
    24,
    'Male',
    'Western',
    'The God',
    new Attributes(50, 50, 50, 50, 50, 50, 150)
);

player.lvl = lvl;

player.addCopper(124);
player.addSilver(63);
player.addGold(10);
player.setMoralityScores(-100, -250, 200, -75, 100, -25, 50, 250, -15);

console.log(player.hlt + ' ' + player.grn);
player.grn -= 161;
console.log(player.hlt + ' ' + player.grn);
player.gainGrant(2);
console.log(player.hlt + ' ' + player.grn);

console.log(player);