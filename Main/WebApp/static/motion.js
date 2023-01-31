function refreshTime() {
    var today = new Date(),
        day = today.getDay(),
        daylist = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
        date = (today.getMonth() + 1) + '月' + today.getDate() + '日',
        time = (("0" + today.getHours()).slice(-2)) + ":" + (("0" + today.getMinutes()).slice(-2));

    $("#time").get(0).innerHTML = date + '<br>' + daylist[day] + '<br>' + time;
}

function display(time, timeout, target){
    $(target).get(0).style.display = "block";
    let cycles = setInterval(() => {
        var objects = $(target),
            now = objects.filter(":visible"),
            next = now.next().length ? now.next() : objects.first();

        now.fadeOut();
        next.fadeIn();
        }, time);

    if(timeout){
        setTimeout(() => {
        clearInterval(cycles);
        }, timeout-1);
    }
}

function cycleVT(time, timeout, target, videoNo) {
    var video = $("video").eq(videoNo);
    display(time, timeout, target);

    setTimeout(() => {
        $(target).filter(":visible").fadeOut();
        video.fadeIn();
        video.get(0).play();
        video.get(0).onended = function(){
        video.fadeOut();
        if(videoNo == $("video").length - 1){
            window.location = window.location.href;
        }
        cycleVT(time, timeout, target, videoNo + 1);
        };
    }, timeout);
}

var systemCycle = 5000,
footerCycle = 5000,
tableCycle = 5000,
tablesTime = tableCycle * $("#tables > div").length;

Promise.all($("video").map(function() {
    return new Promise(resolve => {
        $(this).one("loadedmetadata", resolve);
    });
})).then(() => {
    display(systemCycle, 0, "#system > *");
    display(footerCycle, 0, "footer > div");

    refreshTime();
    setInterval(refreshTime, 1000);

    cycleVT(tableCycle, tablesTime, "#tables > div", 0)
});