const registerForm = document.getElementById("register-form"); //get register form element
const registerButton = document.getElementById("register-form-submit"); // get register button element
const registerErrorMsg = document.getElementById("register-error-msg"); // get error message element

// adds clcik event listener to the register button
registerButton.addEventListener("click", (e) => {
    e.preventDefault(); //prevent defualt submisison 
    const username = registerForm.username.value; // get inputted username
    const password = registerForm.password.value; // get inputted password
    const confirmPassword = registerForm["confirm-password"].value; // get inputted confirm password

    // check if passwords match and are not empty (basic validation for register)
    if (username && password && password === confirmPassword) {
        alert("You have successfully registered."); // show success message
        location.reload(); //reloads the page
    } else {
        registerErrorMsg.style.opacity = 1;//shows erorr messgae
    }
})



