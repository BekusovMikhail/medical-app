window.onload = function() {
    let reg = document.getElementById('reg');
    reg.onsubmit = async (e) => {
        e.preventDefault();
        if (!reg.reportValidity()){
          return
        }
        card1.hidden = 'hidden'
        card2.removeAttribute('hidden')
        let response = await fetch('/api/sendcode', {
          method: 'POST', 
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'email': email.value})
        });
    
        if (response.status == 200) {
          result = await response.json()
          code = result['code']
        } else {
          window.location.replace("dashboard");
        }
      };
    
    let codeForm = document.getElementById('codeForm');
    codeForm.onsubmit = async (e) => {
        e.preventDefault();
        if (codeField.value == code){
          let response = await fetch('/api/registeruser', {
            method: 'POST',
            body: new FormData(reg)
          });

          if (response.status == 201) {
            window.location.replace("dashboard");
          } else {
            window.location.replace("dashboard");
          }
        } else {
          document.getElementById('notif').hidden = false;
        }
        
      };

    let repeatCode = document.getElementById('repeatCode');
    repeatCode.onclick = async (e) => {
        let response = await fetch('/api/sendcode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'email': email.value})
        });

        if (response.status == 200) {
          result = await response.json()
          code = result['code']
        } else {
          window.location.replace("dashboard");
        }
        
      };
}



function checkRoleAddSpec(radioRole) {
    const radioValue = radioRole.value;
    document.getElementById("surnameField").hidden = false;
    document.getElementById("surname").required = true;
    document.getElementById("patronymicField").hidden = false;
    document.getElementById("patronymic").required = true;
    document.getElementById("extraCheck").hidden = false;

    if (radioValue == "doctor"){
      document.getElementById('for_patient').hidden = true;
      document.getElementById('for_doctor').hidden = false;
      
      let d = document.querySelector('#specializ');
      document.querySelector('#specialization_id').required = true
      d.hidden = false
      d = document.querySelector('#address');
      document.querySelector('#address_id').required = false
      d.hidden = true
    }
    else if (radioValue == "patient"){
      console.log(1)
      let d = document.querySelector('#specializ');
      document.querySelector('#specialization_id').required = false
      d.hidden = true
      d = document.querySelector('#address');
      document.querySelector('#address_id').required = false
      d.hidden = true

      document.getElementById('for_patient').hidden = false;
      document.getElementById('for_doctor').hidden = true;
    } else {
      let d = document.querySelector('#specializ');
      document.querySelector('#specialization_id').required = true
      d.hidden = false
      d = document.querySelector('#address');
      document.querySelector('#address_id').required = true
      d.hidden = false
      document.getElementById("patronymicField").hidden = true;
      document.getElementById("surnameField").hidden = true;
      document.getElementById("surname").required = false;
      document.getElementById("patronymic").required = false;
      document.getElementById("extraCheck").hidden = true;
    }
}

function showExtra() {
    let el = document.getElementById("extra");

    if (!el.hidden) {
        el.hidden = true;
    } else {
        el.hidden = false;
    }
}