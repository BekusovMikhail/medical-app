function avatarAppears() {
    let file = document.getElementById('formFile').files[0]
    let img = document.getElementById('newavatar')
    if (typeof file === 'undefined') {
        img.setAttribute("src", img.getAttribute("data-original"))         
    } else {
        img.src = window.URL.createObjectURL(file)
    }
}

function clearFileUploader() {
    let file = document.getElementById('formFile')
    file.value = ''
    avatarAppears.call()
}