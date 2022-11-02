const sideBarDate = document.querySelector("#side-bar__clock__date");
const clockMain = document.querySelector("#side-bar__clock__main h2")
const clockAmpm = document.querySelector("#side-bar__clock__main h3")

function getClock(){
    const clockTime = new Date();
    const dateDetail = clockTime.toDateString(); 
    let hours="";

    if(clockTime.getHours() > 12){
        hours =String(clockTime.getHours()-12).padStart(2,"0");
    }else{
         hours = String(clockTime.getHours()).padStart(2,"0");
    }
    const miniutes = String(clockTime.getMinutes()).padStart(2,"0");

    let ampm ="";
        if(clockTime.getHours()< 12){
            ampm="am"        
        }else{
            ampm="pm"
        }
    
    clockMain.innerText = `${hours}:${miniutes}`;
    sideBarDate.innerText = `${dateDetail}`;
    clockAmpm.innerText= `${ampm}`;
}

getClock();
setInterval(getClock,1000);
