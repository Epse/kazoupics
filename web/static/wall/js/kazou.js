function reqListener() {
    console.log(this.responseText);
    var data = JSON.parse(this.responseText);
    var poster_div = $('#poster');
    var img = $('.hero-image');

    poster_div.text(data.poster);
    img.attr("src", data.url);
}

$(function() {
    window.setInterval(function() {
        var oReq = new XMLHttpRequest();
        oReq.addEventListener("load", reqListener);
        console.log(window.location.protocol+"//"+window.location.host);
        oReq.open("GET", "/next/" + $('.hero-image').attr('src'));
        oReq.send();
    }, 1000);

});
