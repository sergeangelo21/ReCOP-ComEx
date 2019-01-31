window.onload = function() {

if(window.location.pathname=='/linkages/events/create'){
document.getElementById('thrust').options.item(0).selected="True"
document.getElementById('thrust').options.item(0).hidden="True"
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