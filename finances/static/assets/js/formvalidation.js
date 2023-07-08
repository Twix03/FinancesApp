const username = document.querySelector("#username");
const feedback = document.querySelector("#username-invalid");

const showpass = document.querySelector("#show-password");
const passwordField = document.querySelector("#password");
const submitbtn = document.querySelector("#submit-btn");

username.addEventListener('keyup', (e)=>{
    const usernameVal = e.target.value;
    username.classList.remove('is-invalid')
    
    if(usernameVal.length > 0){
        fetch("usernamevalidate", {
            body: JSON.stringify({"username": usernameVal}), 
            method: "POST", 
        }).then((res) => res.json()).then((data)=>{
            if(data.usernameError){
                username.classList.add('is-invalid');
                feedback.innerHTML = data.usernameError;  
                submitbtn.disabled = true;
            }
            else{
                submitbtn.removeAttribute("disabled");
            }
        });     
    } 
});

const email = document.querySelector("#email");
const feedback2 = document.querySelector("#email-invalid");


email.addEventListener('keyup', (e) => {
    emailval = e.target.value;
    email.classList.remove('is-invalid');

    if(emailval.length > 0){
        fetch('emailvalidate', {
            body: JSON.stringify({"email": emailval}),
            method: "POST",
        }).then(res => res.json()).then(data => {
            if(data.emailError){
                email.classList.add('is-invalid');
                feedback2.innerHTML = data.emailError;
                submitbtn.disabled = true;
            }
            else{
                submitbtn.removeAttribute("disabled");
            }
        });
    }
});

passwordField.addEventListener('keyup', (e)=>{
    console.log(1);
    const feedback = document.querySelector("#invalid-password");
    passwordField.classList.remove('is-invalid')
    if(e.target.value.length < 8){
        passwordField.classList.add('is-invalid');
        feedback.innerHTML = "password should contain atleast 8 characters";
        submitbtn.disabled = true;
    }
    else{
        submitbtn.removeAttribute("disabled");
    }
})

showpass.addEventListener('click', (e)=>{
    if(showpass.textContent == "show"){
        showpass.textContent = "hide";
        passwordField.setAttribute("type", "text");
    }
    else{
        showpass.textContent = "show";
        passwordField.setAttribute("type", "password");
    }
})
