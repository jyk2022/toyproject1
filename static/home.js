const homeBtn = document.querySelector("#side-bar__link__homebtn")

function goHome(){
    window.location.href="/home"
}
homeBtn.addEventListener("click",goHome)