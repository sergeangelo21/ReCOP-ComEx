var page=0	
var user = 0;

var carousels = bulmaCarousel.attach(); // carousels now contains an array of all Carousel instances
setInterval(3000);

if(window.location.pathname=='/signup'){
    
    new bulmaSteps(document.getElementById('signup'), {	
    })
    
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

function choose(sender){
    
    if (user==3){
        field = document.getElementById('address_field')
        hide = document.getElementById('address')
        lbl = document.getElementById('com_label')
        active = document.getElementById('company')
        revert = "Company Name" 
    }
    else if (user==2){
        field = document.getElementById('company_field')
        hide = document.getElementById('company')
        lbl = document.getElementById('add_label')
        active = document.getElementById('address')  
        revert = "Address"     
    }

    if (sender=='Y'){

        hide.value = 'San Sebastian College Recoletos de Cavite'
        field.style.display = "none"
        lbl.innerHTML = "Organization"
        active.placeholder = "Organization"

    }
    else{
        hide.value = ''
        field.style.display = ""
        lbl.innerHTML = revert
        active.placeholder = revert
    }

}

function show_form(sender){

    document.getElementById('signup').style.display = "block"
    document.getElementById('illusion').style.display = ""
    document.getElementById('next').style.display = ""
    types = document.getElementById('select_type')
    types.style.display = "none"
    document.getElementById('type').value=sender

    if (sender==4){
        document.getElementById('sscr_field').style.display = "none"
    }
    else{
        document.getElementById('sscr_field').style.display = ""       
    }

    page=1
    user=sender

}

function hide_form(){

   document.getElementById('signup_form').reset()
   document.getElementById('address_field').style.display = ""
   document.getElementById('company_field').style.display = ""
   document.getElementById('add_label').innerHTML = "Address"
   document.getElementById('address').placeholder = "Address"
   document.getElementById('company').placeholder = "Company Name"
   document.getElementById('com_label').innerHTML = "Company Name"


   document.getElementById('signup').style.display = "none"
   document.getElementById('illusion').style.display = "none"
   document.getElementById('next').style.display = "none"
   types = document.getElementById('select_type')
   types.style.display = ""
   page=0

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