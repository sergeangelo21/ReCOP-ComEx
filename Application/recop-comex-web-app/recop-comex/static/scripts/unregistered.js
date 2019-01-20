var page=0  

new bulmaSteps(document.getElementById('signup'), {	
})

function show_form(sender){

    document.getElementById('signup').style.visibility = "visible"
    document.getElementById('illusion').style.visibility = "visible"
    types = document.getElementById('select_type')
    types.style.visibility = "hidden"
    types.style.position = "absolute"
    types.style.z_index = -1
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

   document.getElementById('signup').style.visibility = "hidden"
   document.getElementById('illusion').style.visibility = "hidden"
   types = document.getElementById('select_type')
   types.style.visibility = "visible"
   types.style.position = ""
   types.style.z_index = 0
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
        prev.style.visibility = "visible"
        prev.style.position = ""
        prev.style.z_index = 0
        next = document.getElementById('next')
        next.style.visibility = "visible"
        next.style.position = ""
        next.style.z_index = 0
        document.getElementById('illusion').style.visibility = "hidden"
        document.getElementById('submit').style.visibility = "hidden"

        if (page==3){
            next = document.getElementById('next')
            next.style.visibility = "hidden"
            next.style.position = "absolute"
            next.style.z_index = -1
            document.getElementById('submit').style.visibility = "visible"
        }
    }
    else{

        prev = document.getElementById('prev')
        prev.style.visibility = "hidden"
        prev.style.position = "absolute"
        prev.style.z_index = -1
        document.getElementById('illusion').style.visibility = "visible"                        
    }

}