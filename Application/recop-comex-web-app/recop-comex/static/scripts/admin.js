if(window.location.pathname=='/admin/events/calendar'){
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

if(window.location.pathname=='/admin/events/create'){
	document.getElementById('thrust').options.item(0).selected="True"
	document.getElementById('thrust').options.item(0).hidden="True"
	document.getElementById('select_link').options.item(0).selected="True"
	document.getElementById('select_link').options.item(0).hidden="True"
	document.getElementById('target_link').value = ""
}

var f = []

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

function event_pages(value)
{

	info = document.getElementById('info_div')
	tracker = document.getElementById('tracker_div')
	participant = document.getElementById('participant_div')

	if (value=='info')
	{

		info.className='container'
		tracker.className='container hidden'
		participant.className='container hidden'

	}
	else if (value=='tracker')
	{

		tracker.className='container'
		info.className='container hidden'
		participant.className='container hidden'

	}
	else
	{

		participant.className='container'
		info.className='container hidden'
		tracker.className='container hidden'

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

	document.getElementById('month_year').innerHTML=months[month-1] + ' ' + year

	var calendar = Calendar(first_day, last_day, month, year)

	document.getElementById('calendar').appendChild(calendar)

}

function filter(value)
{

	sender = document.getElementById(value)

	if (sender.checked==true)
	{
		f.push(value)

		// when 'all' is selected, remove value from array
		if (f == 0 || f == 7)
		{
			f.splice(f.indexOf(value), 1);
		}
	}
	else
	{
		f.splice(f.indexOf(value), 1);
	}

	var tbody = document.getElementsByTagName('tbody')

	if (f.length!=0)
	{
		for (ctr=0; ctr<=f.length-1; ctr++)
		{
			for (ctr2=0; ctr2<=tbody.length-1; ctr2++)
			{
					// get tbodies then compare to f.length
					if (tbody[ctr2].id.indexOf(f[ctr].toString()+'_'))
					{
						tbody[ctr2].style.display="none"
					}
					else
					{ 
						tbody[ctr2].style.display=""
					}
			}
		}
	}
	else
	{
		for (ctr2=0; ctr2<=tbody.length-1; ctr2++)
		{
			tbody[ctr2].style.display=""
		}
	}
}

function add_comm(){
	div = document.getElementById('link_div')
	input = document.getElementById('select_link');
	comm = document.getElementById('target_link')
	id = input.selectedIndex
	selected = input.options.item(id).value
	text = input.options[id].text
	input.options.item(id).hidden=true
	
	if (document.getElementById(selected)){
		document.getElementById(selected).style.display=""
	}
	else{
		div.innerHTML = div.innerHTML + "<span class='tag is-dark is-small' id="+ selected + ">"+ text + "&nbsp; <a name='"+selected+"'onclick='remove_comm(this.name)'><i class='fas fa-times'></i></a></span>"
	}

	comm.value = comm.value + selected + '|'
	input.selectedIndex=0
}

function remove_comm(value){

	document.getElementById(value).style.display = "none"
	control =  document.getElementById('select_link')

	for (id=0; id<=control.options.length-1; id++){
		if (control.options.item(id).value==value){
			control.options.item(id).hidden=false
		}
		if (control.options.item(id).value=="Please Select Here"){
			control.selectedIndex=id
		}
	}

	selected = document.getElementById('target_link').value
	str = '|' + value.toString() + '|'
	removed = selected.replace(str, '')
	document.getElementById('target_link').value = removed	
	control.selectedIndex=0

}

function settingsVPACAD() {
    var div = document.getElementById("settingsACAD");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}

function settingsVPFMI() {
    var div = document.getElementById("settingsFMI");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}

function settingsPRES() {
    var div = document.getElementById("settingsSPRES");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}

function filtershrink() {
    var div = document.getElementById("filterDIV");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}