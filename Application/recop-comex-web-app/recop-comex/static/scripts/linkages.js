if(window.location.pathname=='/linkages/events/calendar'){
    var today = new Date()
    var month = today.getMonth() + 1
    var year = today.getFullYear()
    var first_day = new Date(year + '-' + month + '-1')
    var last_day = new Date(year, month , 0)
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    document.getElementById('month_year').innerHTML=months[month-1] + ' ' + year
    var calendar = Calendar(first_day, last_day, month, year)
    document.getElementById('calendar').appendChild(calendar)
}

if(window.location.pathname=='/linkages/donate'){
    if (document.getElementById('event')){
        document.getElementById('event').options.item(0).hidden=true
        document.getElementById('event').options.item(0).selected=true
    }
}

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
		div.innerHTML = div.innerHTML + "<span class='tag is-dark is-small' id="+ selected + ">"+ text + "&nbsp; <a name='"+selected+"'onclick='remove_comm(this.name)'><i class='fas fa-times'></i></a></span>"
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
	str = value.toString() + '|'
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
	a.className="modal is-active"

}

function close_event(value){
	a = document.getElementById(value+'_modal')
	a.className="modal"
} 

function show_eval(value){

    a = document.getElementById('modal')
    a.className="modal is-active"

    document.getElementById(value+'_div').className='fields'
    document.getElementById(value+'_btn').className='delete'
    document.getElementById('participant').value=value

}

function close_eval(value){
    a = document.getElementById('modal')
    a.className="modal"
    document.getElementById(value+'_div').className='hidden'
    document.getElementById(value+'_btn').className='hidden'
    document.getElementById('participant').value=''
}

function show_caption(value){

    a = document.getElementById('modal')
    a.className="modal is-active"

    document.getElementById(value+'_div').className='fields'
    document.getElementById(value+'_btn').className='delete'
    document.getElementById('photo').value=value

}

function close_caption(value){
    a = document.getElementById('modal')
    a.className="modal"
    document.getElementById(value+'_div').className='hidden'
    document.getElementById(value+'_btn').className='hidden'
    document.getElementById('photo').value=''
}

function show_captioned(value){
    a = document.getElementById(value+'_finished')
    a.className="modal is-active"

}

function close_captioned(value){
    a = document.getElementById(value+'_finished')
    a.className="modal"
}

function edit_caption(value){
    close_captioned(value)
    show_caption(value)
}

function show_rating(value){

    a = document.getElementById(value+'_rating')
    a.className="modal is-active"

}

function donate_choose(value){

    comm = document.getElementById('comm')
    event = document.getElementById('events')
    sel_comm = document.getElementById('sponsee')
    sel_event = document.getElementById('event')

    if (value==1){
        comm.className="field is-horizontal"
        events.className="hidden"
        if (sel_event){
            sel_event.value=''
        }
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
        money.value = 0
    }

}   

function filtershrink() {
    var div = document.getElementById("filterDIV");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}


function prev_next(sender){

    document.getElementById('calendar').innerHTML=""

    if (sender=="prev") {
        month = month - 1
        if (month<1){
            month = 12
            year = year - 1
        }
    }

    if (sender=="next"){
        month = month + 1

        if (month>12){
        month = 1
        year = year + 1
        }
    }


    first_day = new Date(year + '-' + month + '-1')
    last_day = new Date(year, month , 0)
    
    document.getElementById('month_year').innerHTML=months[month-1] + ' ' + year

    var calendar = Calendar(first_day, last_day, month, year)

    document.getElementById('calendar').appendChild(calendar)
}
function close_rating(value){
    a = document.getElementById(value+'_rating')
    a.className="modal"
}