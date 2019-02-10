if(window.location.pathname=='/linkages/events/create'){
	document.getElementById('thrust').options.item(0).selected="True"
	document.getElementById('thrust').options.item(0).hidden="True"
	document.getElementById('select_link').options.item(0).selected="True"
	document.getElementById('select_link').options.item(0).hidden="True"
	document.getElementById('target_link').value = ""
}

function add_comm(){
	div = document.getElementById('link_div')
	input = document.getElementById('select_link');
	comm = document.getElementById('target_link')
	id = input.selectedIndex
	selected = input.options.item(id).value
	text = input.options[id].text
	input.options.item(id).hidden=true
	
	if (document.getElementById(selected)){
		document.getElementById(selected).style.display=""
	}
	else{
		div.innerHTML = div.innerHTML + "<span id="+ selected + " class='button' style='margin-top:1%; padding:1%'>"+ text + "&nbsp; <a class='button is-white is-small' name='"+selected+"'onclick='remove_comm(this.name)'><i class='fas fa-times'></i></a></span>"
	}

	comm.value = comm.value + selected + '|'
	input.selectedIndex=0
}

function remove_comm(value){

	document.getElementById(value).style.display = "none"
	control =  document.getElementById('select_link')

	for (id=0; id<=control.options.length-1; id++){
		if (control.options.item(id).value==value){
			control.options.item(id).hidden=false
		}
		if (control.options.item(id).value=="Please Select Here"){
			control.selectedIndex=id
		}
	}

	selected = document.getElementById('target_link').value
	str = '|' + value.toString() + '|'
	removed = selected.replace(str, '')
	document.getElementById('target_link').value = removed	
	control.selectedIndex=0

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

function show_event(value){

	a = document.getElementById(value+'_modal')
	a.style.display='block'

}

function close_event(value){
	a = document.getElementById(value+'_modal')
	a.style.display='none'

}