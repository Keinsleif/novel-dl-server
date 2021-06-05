var tf=1;
var iid;
var pid;
window.onload = function() {
    document.getElementById('submit').onclick = function() {
        post();
    };
  
    xhr = new XMLHttpRequest();
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                if (xhr.responseText!="False"){
                    pid=xhr.responseText;
                    dl_wait(pid);
                }
                else{
                    document.getElementById("submit").disabled=false;
                }
            }
        }
    };
    xhr2 = new XMLHttpRequest();
    xhr2.onload = function (e) {
        if (xhr2.readyState === 4) {
            if (xhr2.status === 200) {
                if (xhr2.responseText.match("/False/")){
                    dl_wait(pid);
                }
                else{
                    location.reload();
                }
            }
        }
    };
};

function dl_wait(pid){
    xhr2.open('GET','/dl/'+pid,true);
    xhr2.send("");
}

function post() {
    form={};
    args=["url","theme","media","renew","axel","episode","short"];
    request="url="+document.getElementById("url").value;
    for (var i=1;i<args.length;++i){
        request=request+"&"+args[i]+"="+document.getElementById(args[i]).value;
    }
    xhr.open('POST', '/', true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send(request);
    document.getElementById("submit").disabled=true;
    document.getElementById("spinner").style="display:inline-block"
}