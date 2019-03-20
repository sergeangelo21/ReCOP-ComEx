var page=1	

var carousels = bulmaCarousel.attach(); // carousels now contains an array of all Carousel instances
setInterval(3000);

if(window.location.pathname=='/events/calendar'){
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

if(window.location.pathname!='/signup' && window.location.pathname.startsWith('/signup')){

    if (document.getElementById('thrust')){
        document.getElementById('thrust').options.item(0).hidden=true
        document.getElementById('thrust').options.item(0).selected=true   
    }

    if (document.getElementById('classification')){
        document.getElementById('classification').options.item(0).hidden=true
        document.getElementById('classification').options.item(0).selected=true   
    }
    
    new bulmaSteps(document.getElementById('signup'), {	
    })
    
}

if(window.location.pathname=='/donate'){
    document.getElementById('event').options.item(0).hidden=true
    document.getElementById('event').options.item(0).selected=true
}


function check_pass(){

    pass = document.getElementById('password')
    confirm = document.getElementById('password_confirm')

    if (pass.value!=confirm.value){
        Swal.fire('Passwords did not match.', ' ', 'error')
        return false
    }
    else{
        return true
    }
}

function choose(sender){
    
    field = document.getElementById('address_field')
    thrust = document.getElementById('thrust_field')
    hide = document.getElementById('address')

    if (sender=='Y'){

        hide.value = 'San Sebastian College Recoletos de Cavite'
        field.className = "hidden"
        thrust.className="hidden"


    }
    else{
        hide.value = ''
        field.className='field is-horizontal'
       thrust.className="field is-horizontal"
    }

}


function btn(sender){

	if (sender=='prev'){
	
		page--
    
    }

    else{

    	page++

    }

    if (page>1){
        prev = document.getElementById('prev')
        prev.style.display = ""
        prev.style.z_index = 0
        prev.style.display = "flex"
        next = document.getElementById('next')
        next.style.display = ""
        next.style.display = "flex"
        next.style.z_index = 0
        document.getElementById('illusion').style.display = "none"
        document.getElementById('illusion').style.z_index = -1
        document.getElementById('submit').style.display = "none"
        document.getElementById('submit').style.z_index= -1

        if (page==3){
            next = document.getElementById('next')
            next.style.display = "none"
            next.style.position = "absolute"
            next.style.z_index = -1
            document.getElementById('submit').style.display = ""
            document.getElementById('submit').style.display = "flex"
        }
    }

    else{

        prev = document.getElementById('prev')
        prev.style.display = "none"
        prev.style.position = "absolute"
        prev.style.z_index = -1
        document.getElementById('illusion').style.display = ""                        
    }

}

function donate_choose(value){

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
        money.value = 0.00
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
