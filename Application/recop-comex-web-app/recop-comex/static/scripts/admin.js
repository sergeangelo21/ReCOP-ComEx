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

function filter(value)
{
	all = document.getElementById('0')
	educational = document.getElementById('1')
	environmental = document.getElementById('2')
	health = document.getElementById('3')
	livelihood = document.getElementById('4')
	sociopolitical = document.getElementById('5')
	spiritual = document.getElementById('6')

	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function()
	{
	    if (this.readyState == 4 && this.status == 200) 
	    {
	    document.getElementById("txtHint").innerHTML = this.responseText;
		}
	};

	xhttp.open("GET", "getcustomer.php?q="+str, true);
	xhttp.send();

	alert(partner_thrust)
	f.push(value)


}