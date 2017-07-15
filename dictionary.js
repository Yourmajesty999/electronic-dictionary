
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
	xmlhttp.onreadystatechange=function()
  	{
  	if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
    //change the message of json to js
    var myObj = JSON.parse(this.responseText);
    var content = ""
    //get message from dictionary
    if(myObj.result && myObj.result.pronounces && myObj.result.translate && myObj.result.web_translate){
	content += myObj.result.pronounces.join("<br>") + "<br>" + myObj.result.translate.join("<br>") + "<br>" + "网络释义：" + myObj.result.web_translate
    }
    //put the translate message to the place
    document.getElementById("myDiv").innerHTML=content;
    }
  };
  //get words from input 
  var words = document.getElementById('myWords').value;
	xmlhttp.open("GET","/dictionary/eng/" + words);
	xmlhttp.send();

}
//key event
function do_getword(e){
	if(e.code === 'Enter'){
		getWords()
	}
}













