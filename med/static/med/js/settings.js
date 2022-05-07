
window.onload = () => {
    avatar.onchange = evt => {
        const [file] = avatar.files
        if (file) {
            imgPreview.src = URL.createObjectURL(file)
        }
    }

    editButt.onclick = (event) => {
        let elems = document.querySelectorAll('.form-control');
        for (let elem of elems) {
            elem.disabled = false
        }
        saveButt.disabled = false
    }

    saveButt.onclick = saveClicked
}

async function saveClicked(event) {
        if (!settings.reportValidity()){
            return
        }
        let response = await fetch('/api/changesettings', {
            method: 'POST',
            body: new FormData(settings)
        });
        if (response.ok) {
            document.location.reload();
        } else {
            alert('Unknown error. Try again')
        }
    }