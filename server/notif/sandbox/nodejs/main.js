function formatParams( params ){
	return "?" + Object
		.keys(params)
		.map(function(key){
			return key+"="+encodeURIComponent(params[key])
		})
		.join("&")
}
function urlencodeFormData(fd){
	var params = new URLSearchParams();
	for(var pair of fd.entries()){
		typeof pair[1]=='string' && params.append(pair[0], pair[1]);
	}
	return params.toString();
	return s;
}


onSubmit = function(e){
	addr = document.getElementById("address").value
	addr = 'http://'+addr
	console.log(addr)
	json = document.getElementById("json")
	sending = {}
	items = json.children
	var data = new FormData();
	for (i in items){
		c = items[i].children
		//console.log(c[0].value,c[1].value)
		if (c){
			sending[c[0].value]=c[1].value
			data.append(c[0].value,c[1].value)
		}
	}
	console.log(sending)
	res = document.getElementById("result")
	res.innerHTML = "<div>MAKING...</div>"

	var xhr = new XMLHttpRequest();
	type = document.getElementById('type').value
	if (type!='POST'){
		url = addr+formatParams(sending)
		xhr.open( type , url, true);
	}else{
		url = addr
		xhr.open( type , url, true);
		xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	}
	xhr.onload = function () {
		res = document.getElementById("result")
		res.innerHTML = "<div>DONE</div>" +xhr.responseText
	}
	xhr.send(JSON.stringify(sending))
}


Add = function(){
	json = document.getElementById("json")
	item= document.getElementById("item")
	json.innerHTML = json.innerHTML + itemhtml
	//json.appendChild(item.cloneNode())

}

var itemhtml = "<div id=\"item\">\
				<input id=\"key\" type=\"text\">\
				<input id=\"value\" type=\"text\">\
			</div>\
"
