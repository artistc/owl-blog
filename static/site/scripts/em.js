setTimeout(function() { 
    var l = String.fromCharCode(108);
    var em = ['o' + l + 'ooney',  'gmai' + l + '.com'].join(String.fromCharCode(64));
    var mt = 'mai' + l + 'to';
    // document.write('<a href="' + mt + ':' + em + '">' + em + '</a>');
	var el = document.getElementById("owl-em");
	if ( el ) el.innerHTML = '<a href="' + mt + ':' + em + '">' + em + '</a>';
}, 100);

