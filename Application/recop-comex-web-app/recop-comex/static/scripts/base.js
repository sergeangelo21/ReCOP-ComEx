window.onload = function() {

	var burger = document.querySelector('.burger');
	var nav = document.querySelector('#'+burger.dataset.target);

	burger.addEventListener('click', function(){
  		burger.classList.toggle('is-active');
 		nav.classList.toggle('is-active');
 	})

<<<<<<< HEAD
}
=======
}

function show_notif(){

	toogle = document.getElementById('navtoggle').checked

	if (toogle==true){
		document.getElementById('notifications').className='notifications'
		document.getElementById('navtoggle').checked=false
	}
	else{
		document.getElementById('notifications').className='hidden'
		document.getElementById('navtoggle').checked=true		
	}

}

function show_profile(){

	a = document.getElementById('modal')
	a.className = "modal is-active"
	 document.getElementById('photo').value=''
	document.getElementById('show').src = document.getElementById('dp').src
}

function close_profile(){

	a = document.getElementById('modal')
	a.className = "modal"
}

function profile() {
    var file = document.getElementById('photo').files[0];
    var reader  = new FileReader();
    // it's onload event and you forgot (parameters)
    reader.onload = function(e)  {
        var image = document.getElementById('show');
        // the result image data
        image.src = e.target.result;
    }
     // you have to declare the file loading
     reader.readAsDataURL(file);
 }
>>>>>>> ed41dd78e3d90906e0a1d1b66d3b95b6b7f9ad82
