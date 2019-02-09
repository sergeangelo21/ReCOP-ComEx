window.onload = function() {

	if(window.location.pathname=='/registered/donate'){
		document.getElementById('event').options.item(0).hidden=true
		document.getElementById('event').options.item(0).selected=true
	}

}

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

function choose(value){

	comm = document.getElementById('comm')
	event = document.getElementById('events')
	sel_comm = document.getElementById('sponsee')
	sel_event = document.getElementById('event')

	if (value==1){
		comm.className="field is-horizontal"
		events.className="hidden"
		sel_event.value=''
	}
	else{
		comm.className="hidden"
		events.className="field is-horizontal"
		sel_comm.value=''
	}

}

function donate_type(value){

	amount = document.getElementById('amount_div')
	trans = document.getElementById('trans_div')
	money = document.getElementById('amount')

	if (value==1){
		amount.className="field is-horizontal"
		trans.className="field is-horizontal"
		money.value=''
	}
	else{
		amount.className="hidden"
		trans.className="field is-horizontal"
		money.value	= 0
	}

}