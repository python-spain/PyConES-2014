String.prototype.count = function(search) {
        var m = this.match(new RegExp(search.toString().replace(/(?=[.\\+*?[^\]$(){}\|])/g, "\\"), "g"));
            return m ? m.length:0;
}

function select_lang() {
    lang = $.trim($('#langselect option:selected').val());
    if (window.location.href.count("/") > 3){
        window.location.href = window.location.protocol + "//" + window.location.hostname + "/"+lang+"/" + window.location.href.split("/")[4]
    } else {
        window.location.href = window.location.protocol + "//" + window.location.hostname + "/"+lang+"/";
    }
}
