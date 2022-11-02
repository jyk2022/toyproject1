const writeBtn = document.querySelector("#side-bar__link__writebtn")

function goWrite(){
    window.location.href="/article"
}
writeBtn.addEventListener("click",goWrite)