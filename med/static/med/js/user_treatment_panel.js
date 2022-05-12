window.onload = () => {
    select_proc.onchange = selectChanged
}

function selectChanged(event){
    let s = event.target.selectedOptions[0]
    if (s.value == '-1'){
        proc_name.value = ""
        proc_description.innerText = ""
        proc_steps.innerText = ""
        proc_name.disabled = false
        proc_description.disabled = false
        proc_steps.disabled = false
    } else {
        proc_name.value = s.dataset.name
        proc_description.innerText = s.dataset.description
        proc_steps.innerText = s.dataset.steps
        proc_name.disabled = true
        proc_description.disabled = true
        proc_steps.disabled = true
    }
}