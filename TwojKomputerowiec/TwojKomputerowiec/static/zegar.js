function currentTimeAndDate()
{
    var today = new Date();
    var hours = today.getHours();
    if(hours < 10) hours = "0" + hours;
    var minutes = today.getMinutes();
    if(minutes < 10) minutes = "0" + minutes;
    var seconds = today.getSeconds();
    if(seconds < 10) seconds = "0" + seconds;
    $("#zegar").html(hours + ":" + minutes + ":" + seconds);

    setTimeout("currentTimeAndDate()", 500);
}