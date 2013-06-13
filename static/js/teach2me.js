var delaytime=10		//time before disabled button is re-enbled
var delayAjax=50
$(document).ready(function(){
var enableSubmit = function(ele) {
    $(ele).removeAttr("disabled");
}
function unpack(data){
	console.log()
	console.log(''+data['too_slow'])
	$('#lost-badge').text(data['lost'])
	$('#slow_down-badge').text(data['too_fast'])
	$('#speed_up-badge').text(data['too_slow'])
}
function nj (){
	$.get('/mystats',{sample:true},function(data){
		console.log(data)
		unpack(data)
		setTimeout(nj,delayAjax)
	});
}
nj();

$('#questionbox').bind('input propertychange', function() {

//    $("#qn-submit").hide();

    if(this.value.length>3){
      $("#qn-submit").show();
    }
    else{
    	$("#qn-submit").hide();
    }
});

$('#qn-submit').click(function(){
	console.log('submitting data')
	$.get('/post_qn',{question:$('#questionbox').val()},
			function(data){
		console.log("TODO")
	})
	$('#questionbox').val('')
	$("#qn-submit").hide();
})

jQuery('.btn').attr('disabled', false);
    $('.btn').click(function(){
    	console.log(''+this.value +this.id);
    	$(this).attr('disabled',true)
    	x=this
    	$.get("/post_data", { button: x.id},
				function(data) {
				console.log("Data Loaded: " + data);
//	    		$('#'+x.id+'-badge').text(data)
				});
    	$('#'+this.id+'-badge').effect('pulsate')
    	setTimeout(function(){
    		console.log('sending value to server'+x.value)
    		$(x).attr('disabled',false)
    	}, delaytime)
    }); 
});
