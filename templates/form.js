
$('.join').click(function(){
	goalname='华理创客空间'
	$('#myModalLabel').text('想加入'+goalname+'?')

	if ($('#recipient-name').val()==null|| $('#phone-number').val()){
		$('#recipient-name').removeAttr('disabled')
		$('#phone-number').removeAttr('disabled')	
	}
})
$('.apply').click(function(e){
	goalname=$(e.target).parent().find('h2').text()
	$('#myModalLabel').text(goalname+'?')
	if (!($('#recipient-name').val()) || !($('#phone-number').val())){
		$('#recipient-name').removeAttr('disabled')
		$('#phone-number').removeAttr('disabled')	
	}
})


