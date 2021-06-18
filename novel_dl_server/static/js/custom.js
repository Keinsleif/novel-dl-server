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
            else {
                add_alert("Network Error");
            }
        }
    };
    xhr2 = new XMLHttpRequest();
    xhr2.onload = function (e) {
        if (xhr2.readyState === 4) {
            if (xhr2.status === 200) {
                if (xhr2.responseText.match("/Never/")){
                    dl_wait(pid);
                }
                else{
                    var response=JSON.parse(xhr2.responseText);
                    if (response["success"]){
                        location.reload();
                    }
                    else {
                        add_alert(response["result"]);
                        document.getElementById("submit").disabled=false;
                        document.getElementById("spinner").style="display:none";
                    }
                }
            }
        }
    };
};

function dl_wait(pid){
    xhr2.open('GET','/dl/'+pid,true);
    xhr2.send("");
}

function add_alert(text) {
    var alert=document.getElementById("alert");
    alert.id="alert";
    alert.className="alert alert-danger alert-fadeout";
    alert.role="alert";
    alert.innerHTML=text;
}

function post() {
    if (!document.getElementById("url").value){
        add_alert("Please enter the URL.");
        return;
    }
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
    document.getElementById("spinner").style="display:inline-block";
}
