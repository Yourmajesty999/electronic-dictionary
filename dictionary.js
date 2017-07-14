
function getWords() {
	var xmlhttp;
	if (window.XMLHttpRequest)
	  {// code for IE7+, Firefox, Chrome, Opera, Safari
	  xmlhttp=new XMLHttpRequest();
	  }
	else
	  {// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }

	
	//var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange=function()
  	{
  	if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    var myObj = JSON.parse(this.responseText);
    var content = ""
    if(myObj.result && myObj.result.pronounces && myObj.result.translate && myObj.result.web_translate){
	content += myObj.result.pronounces.join("<br>") + "<br>" + myObj.result.translate.join("<br>") + "<br>" + "网络释义：" + myObj.result.web_translate
    }
    document.getElementById("myDiv").innerHTML=content;
    }
  };
  var words = document.getElementById('myWords').value;
	xmlhttp.open("GET","/dictionary/eng/" + words);
	//xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xmlhttp.send();

}

function do_getword(e){
	if(e.code === 'Enter'){
		getWords()
	}
}
/*
function getWords(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	        var myObj = JSON.parse(this.responseText);
	        var content = ""
	        if(myObj.result && myObj.result.translate){
	        	content += myObj.result.translate.join("<br>")
	        }
	        document.getElementById("myDiv").innerHTML = content;
	    }
	};
	var words = document.getElementById('myWords').value;
	xmlhttp.open("GET", "/dictionary/eng/" + words);
	xmlhttp.send();
}
*/

function myCanvas() {
	var c = document.getElementById("myCanvas");
	var img = document.createElement("img");
	img.src="wilde.jpg";
	c.appendChild(img);
}














