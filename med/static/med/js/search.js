
window.onload = () => {
    search.oninput = formChanged
    selAll.onclick = (event) => {
        let elems = document.querySelectorAll("#search input[type=\"checkbox\"]")
        for (let elem of elems){
           elem.checked = true
        }
        formChanged()
    }
    canAll.onclick = (event) => {
        let elems = document.querySelectorAll("#search input[type=\"checkbox\"]")
        for (let elem of elems){
           elem.checked = false
        }
        formChanged()
    }
}

function formChanged(event=null){
    if (radioClinics.checked === true){
        specDropdown.hidden = true
    } else if (radioDoctors.checked === true){
        specDropdown.hidden = false
    }
    if (radioClinics.checked === true){
        let doctors = document.querySelectorAll(".doctor")
        for (let doctor of doctors){
            doctor.hidden = false
        }
        let clinics = document.querySelectorAll(".clinic")
        for (let clinic of clinics){
            clinic.hidden = !clinic.dataset.name.toLowerCase().trim().includes(searchText.value.toLowerCase().trim());
        }
    } else if (radioDoctors.checked === true){
        let clinics = document.querySelectorAll(".clinic")
        for (let clinic of clinics){
            clinic.hidden = false
        }
        let doctors = document.querySelectorAll(".doctor")
        let specs = document.querySelectorAll("#search input[type=\"checkbox\"]:checked")
        let specs_names = []
        for (let spec of specs){
            specs_names.push(spec.value)
        }
        for (let doctor of doctors){
            if (doctor.dataset.name.toLowerCase().trim().includes(searchText.value.toLowerCase().trim()) && specs_names.includes(doctor.dataset.spec)) {
                doctor.hidden = false
            } else {
                doctor.hidden = true
            }
        }
        clinics = document.querySelectorAll(".clinic")
        for (let clinic of clinics){
            doctors = clinic.querySelectorAll(".doctor")
            let f = true
            for (let doctor of doctors){
                if (doctor.hidden === false){
                    f = false
                    break
                }
            }
            if (f){
                clinic.hidden = true
            }
        }
    }
}