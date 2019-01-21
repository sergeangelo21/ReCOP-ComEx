var page=0	

new bulmaSteps(document.getElementById('signup'), {	
})

function show_form(sender){

    document.getElementById('signup').style.display = "block"
    document.getElementById('illusion').style.display = ""
    document.getElementById('next').style.display = ""
    types = document.getElementById('select_type')
    types.style.display = "none"
    page=1

    if (sender=="3"){
    	document.getElementById('variant').innerHTML = "Company"
    }
    else {
        document.getElementById('variant').innerHTML = "Personal"
    }

    document.getElementById('type').value = sender

}

function hide_form(){

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