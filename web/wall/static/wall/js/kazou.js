function reqListener() {
    console.log(this.responseText);
    var data = JSON.parse(this.responseText);
    var poster_div = $('#poster');
    var img = $('#img img');

    poster_div.text(data.poster);
    img.attr("src", data.url);
}

$(function() {
    window.setInterval(function() {
        var oReq = new XMLHttpRequest();
        oReq.addEventListener("load", reqListener);
        console.log(window.location.protocol+"//"+window.location.host);
        oReq.open("GET", "/next");
        oReq.send();
    }, 500);

});
