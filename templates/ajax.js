function post_join_inform(){
	$.getJSON( '/joinus', {
        name: $('#recipient-name').val(),
        phone: $('#phone-number').val(),
		goal:goalname
      }, function(data) {
        $("#inform_show").text(data.result);
		if(data.status=='OK'){
			$('#cancel_join_btn').html('确认！')
			$('#confirm_join_btn').hide()
			$('#recipient-name').attr('disabled','disabled')
			$('#phone-number').attr('disabled','disabled')
		}
		else{
			$('#recipient-name').val('')
			$('#phone-number').val('')
		}
})}