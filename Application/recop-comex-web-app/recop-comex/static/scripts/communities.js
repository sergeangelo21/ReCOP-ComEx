function check_pass()
{

    pass = document.getElementById('password')
    confirm = document.getElementById('password_confirm')

    if (pass.value!=confirm.value)
    {
        alert('Passwords did not match.')
        return false
    }
    else
    {
        return true
    }
}

function employed(value)
{

    occupation = document.getElementById('occupation_field')
    income = document.getElementById('income_field')

    if (value=='N')
    {
        document.getElementById('occupation_field').style.display="none"
        document.getElementById('income_field').style.display="none"
        occupation.value = null
        income.value = 0

    }

    else
    {
        document.getElementById('occupation_field').style.display="block"
        document.getElementById('income_field').style.display="block"
        occupation.value = ''
        income.value = ''
    }
}

function filtershrink()
{
    var div = document.getElementById("filterDIV");
    if (div.style.display === "none")
    {
        div.style.display = "block";
    } 
    else 
    {
        div.style.display = "none";
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
