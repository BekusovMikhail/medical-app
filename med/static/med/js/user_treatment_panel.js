window.onload = () => {
    select_proc.onchange = selectChanged
    createProcButt.onclick = createTreatClicked
    closeTreatmentButt.onclick = closeTreatment

    resultImage.onchange = evt => {
        const [file] = resultImage.files
        if (file) {
            imgPreview.src = URL.createObjectURL(file)
        }
    }
    
}

async function addResultButton(but) {
    let id = but.getAttribute('data-id');
    let response = await fetch('/api/get_current_procedure_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'proc_id': id})
    });

    if (response.ok) {
        data = await response.json()
        if (data['text'] != null) {
            resultTextField.innerText = data['text'];
        } else {
            resultTextField.innerText = null;
        }
        if (data['img'] != null) {
            imgPreview.src = data['img'];
        } else {
            imgPreview.src = "";
        }
    } 

    procId.value = id;
}

function selectChanged(event){
    let s = event.target.selectedOptions[0]
    if (s.value == '-1'){
        proc_name.value = ""
        proc_description.value = ""
        proc_steps.value = ""
        proc_name.disabled = false
        proc_description.disabled = false
        proc_steps.disabled = false
    } else {
        proc_name.value = s.dataset.name
        proc_description.value = s.dataset.description
        proc_steps.value = s.dataset.steps
        proc_name.disabled = true
        proc_description.disabled = true
        proc_steps.disabled = true
    }
}

async function createTreatClicked(event) {
     if (!add_proc.reportValidity()){
            return
        }
        let response = await fetch('/api/addCurrProcedure', {
            method: 'POST',
            body: new FormData(add_proc)
        });
        if (response.ok) {
            document.location.reload();
        } else {
            alert('Unknown error. Try again')
        }
}

async function closeTreatment(event) {
    let response = await fetch('/api/closeTreatment', {
		    method: 'POST',
		    headers: {
		        'Content-Type': 'application/json'
		    },
		    body: JSON.stringify({'treat_id': treat_id.value })})
		if (response.ok) {
		    window.location.replace('/account')
        } else{
		    alert('Unknown error. Try again')
        }
}

async function getValue(radio) {
    let response = await fetch('/api/setDoctorRating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'treat_id': treat_id.value, 'rate': radio.value})})
        if (response.ok) {
            radio.checked = true;
            document.location.reload();
        } else {
            alert('Unknown error. Try again')
        }

}
