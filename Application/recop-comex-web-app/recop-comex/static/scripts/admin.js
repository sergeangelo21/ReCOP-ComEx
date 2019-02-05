

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

function filter(value){

	alert(value)
	f.push(value)
	for(ctr=0;ctr<=f.size;ctr++)
		{
			alert(value)
		}

}