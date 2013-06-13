var last_id=0
var delayAjax=5000
function unpackmsg(data){
	if(last_id==0){
		for (var i=0;i<data.length;i++)
		{
			console.log('unpacking '+i)
			console.log(data[i]['question'])
			$('#messages').prepend('<tr><td>'+data[i]['question']+'</td><tr>')
		}
		last_id=data[0]['id']
	}
	else{
		console.log('data update unpacking...')
		console.log(data)
		if(data['id']!=last_id){
			$('#messages').prepend('<tr><td>'+data['question']+'</td><tr>')
			last_id=data['id']
		}
	}
}
function s(){
	$.get('/stream_qn',{initial:true},function(data){
		console.log('starting')
		console.log(data)
		unpackmsg(data)
	});
}
s()
function check_for_update(){
	$.get('/stream_qn',{last_message:last_id},function(data){
		console.log(data)
		unpackmsg(data)
		setTimeout(check_for_update,delayAjax)
	});
}
check_for_update();