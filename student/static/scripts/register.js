function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (username === "" || password === "" || confirmPassword === "") {
        alert("Please fill in all fields.");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }

    if (password == confirmPassword) {
        alert("Registration Successful!");
        localStorage.setItem("Id",'gokul')
        return true;
    }
    
}

function submitted(){
    alert("Details Submitted");
}
const id = localStorage.getItem('Id')
console.log(id)


function logout(){
    window.history.forward();
}