var div=document.getElementById("listdir");
div.innerHTML='<a id=\"diva\" href=#toptitle>Top</a>'
div.onmousedown=function(){
    div.style.backgroundColor="white";
}
div.onmouseup=function(){ 
    div.style.backgroundColor="#a0a0a0";
}

var divt=document.getElementById("toptitle");
var topdir=document.createElement('div');
topdir.setAttribute('id','t1');
var len=window.location.pathname.length;
var firstp=window.location.pathname.substring(1,len).indexOf('/');
var project=window.location.pathname.substring(0,firstp+1);
topdir.innerHTML='<a id=\"atop\" href='+project+'/index.html>List Dir</a>';
var current=document.createElement('div');
current.setAttribute('id','t2');
var last=window.location.pathname.lastIndexOf('/');
var path=window.location.pathname.substring(1,last);
current.innerHTML='<a id=\"currenta\" href='+project+'#'+path+'>Current</a>';
divt.appendChild(topdir);
divt.appendChild(current);

topdir.onmouseover=function(){
    topdir.style.backgroundColor="#a3a3a3";

}
topdir.onmouseout=function(){
    topdir.style.backgroundColor="#666666";
}
current.onmouseover=function(){
    current.style.backgroundColor="#a3a3a3";

}
current.onmouseout=function(){
    current.style.backgroundColor="#666666";
}