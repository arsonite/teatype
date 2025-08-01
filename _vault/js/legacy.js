/* Getting user-prompt and splitting it into key-value pairs for localStorage */
kvp = window.prompt("Please enter a Key-Value-Pair. The key (single word) has to be separated from the value (can be multiple words) by a space.", "");
out(kvp);
var key = kvp.replace(/\s.*/, "");
var value = kvp.replace(/^\S+\s/, "");
out("Key: " + key + "\nValue: " + value);
localStorage.setItem(key, value);

document.getElementById("drop").onmouseover = function() {
    myFunction();
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

document.getElementById("ls_submit").onclick = function () {
    var key = document.getElementById("key_in").value;
    var val = document.getElementById("value_in").value;
    if (key !== "" &&  val !== "") {
        localStorage.setItem(key, val);
    } else {
        alert("No empty Strings allowed. Key-Value-Pair wasn't submitted into localStorage.");
    }
}

////////// Modal //////////

var modal = document.getElementById('ls_modal');
var span = document.getElementsByClassName("ls-modal-close")[0];

/* When the user clicks on <span> (x), close the modal */
span.onclick = function () {
    modal.style.display = "none";
}

/* When the user clicks anywhere outside of the modal, close it */
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

////////// CommonJS Module Test //////////

let test = require('./js/html_test.js');
console.log(test.header);

var html = {
    header: "header",
    body: "body",
    footer: "footer"
};

module.exports = html;