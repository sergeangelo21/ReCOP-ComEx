window.onload = function() {

	var burger = document.querySelector('.burger');
	var nav = document.querySelector('#'+burger.dataset.target);

	burger.addEventListener('click', function(){
  		burger.classList.toggle('is-active');
 		nav.classList.toggle('is-active');
 	})

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