var bntSingin = document.querySelector("#singin");
var bntSingup = document.querySelector("#singup");
var body = document.querySelector("body");

bntSingin.addEventListener("click", function() {
    body.className = 'sing-in-js'
});

bntSingup.addEventListener('click', function(){
    body.className = 'sing-up-js'
});

