// function avatarAppears() {
//     let file = document.getElementById('formFile').files[0]
//     let img = document.getElementById('newavatar')
//     if (typeof file === 'undefined') {
//         img.setAttribute("src", img.getAttribute("data-original"))
//     } else {
//         img.src = window.URL.createObjectURL(file)
//     }
// }
//
// function clearFileUploader() {
//     let file = document.getElementById('formFile')
//     file.value = ''
//     avatarAppears.call()
// }

window.onload = () => {
    avatar.onchange = evt => {
        const [file] = avatar.files
        if (file) {
            imgPreview.hidden = false;
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