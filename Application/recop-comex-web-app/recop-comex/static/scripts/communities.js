if(window.location.pathname=='/communities/events/calendar'){
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
        income.value = 0.00

    }

    else
    {
        document.getElementById('occupation_field').style.display="block"
        document.getElementById('income_field').style.display="block"
        occupation.value = null
        income.value = 0.00
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
    a.className="modal is-active"

}

function close_event(value){
    a = document.getElementById(value+'_modal')
    a.className="modal"

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