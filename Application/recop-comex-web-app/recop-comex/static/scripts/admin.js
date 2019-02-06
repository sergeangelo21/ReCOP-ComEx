

var f = []

function check_pass(){

    pass = document.getElementById('password')
    confirm = document.getElementById('password_confirm')

    if (pass.value!=confirm.value){
        alert('Passwords did not match.')
        return false
    }
    else{
        return true
    }
}

function event_pages(value) {

	info = document.getElementById('info_div')
	tracker = document.getElementById('tracker_div')
	participant = document.getElementById('participant_div')

	if (value=='info'){

		info.className='container'
		tracker.className='container hidden'
		participant.className='container hidden'

	}
	else if (value=='tracker'){

		tracker.className='container'
		info.className='container hidden'
		participant.className='container hidden'

	}
	else{

		participant.className='container'
		info.className='container hidden'
		tracker.className='container hidden'

	}

}

function filter(value){

	alert(value)
	f.push(value)
	for(ctr=0;ctr<=f.size;ctr++)
		{
			alert(value)
		}

}