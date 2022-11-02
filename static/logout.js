
const logoutBtn = document.querySelector("#logoutbtn")



function logout() {
    $.ajax({
        type: "POST",
        url: "/logout",
        data: {},
        success: function (response) {
            // response
            console.log(response);
            userState = response.logged_in_as;
            window.location.href = '/';
        },
    });
}

logoutBtn.addEventListener("click",logout)