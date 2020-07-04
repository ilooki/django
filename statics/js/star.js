window.onload = function(){
    let clientW = document.documentElement.clientWidth;
    let clientH = document.documentElement.clientHeight;
    // var container = document.getElementsByClassName("container")[0];

    for(let i=0; i<159; i++){
        let span = document.createElement("span");
        span.className = "star";
        document.body.appendChild(span);
        let x = Math.random() * clientW;
        let y = Math.random() * clientH;
        span.style.left = x + "px";
        span.style.top = y + "px";
        // 闪烁的频率
        let rate = Math.random() * 1.5;
        span.style.animationDelay = rate + "s";

        // 大小
        let scale = Math.random() * 1.5;
        span.style.transform = 'scale('+ scale + "," + scale + ')';



    }



}
