const loginForm = document.getElementById("login-form"); //get login form element
const loginButton = document.getElementById("login-form-submit"); // get login button element
const loginErrorMsg = document.getElementById("login-error-msg"); // get error message element

// adds clcik event listener to the login button
loginButton.addEventListener("click", (e) => {
    e.preventDefault(); //prevent defualt submisison 
    const username = loginForm.username.value; // get inputted username
    const password = loginForm.password.value; // get inputted password

    if (username === "xxx" && password === "xxx") { // check if usernmae and password matches, going to set up data base first tho
        alert("You have successfully logged in."); // show succes smessage
        location.reload(); //reloads the page
    } else {
        loginErrorMsg.style.opacity = 1;//shows erorr messgae
    }
})