 $(document).ready(function () {
            show_todo();
        });
function show_todo(){
    $('#main-screen__widget__todos__list').empty();
    $.ajax({
        type: "GET",
        url: "/guhaejo/todos",
        data: {},
        success: function (response) {
            rows = response['todos']
            for(i=0;i<rows.length;i++){
                let todo =rows[i]['todo'];
                let num = rows[i]['num'];
                let done = rows[i]['done'];
                let id = rows[i]['id'];
                let tempHtml ='';
                if(done == 0){
                    tempHtml =  `<li><button onclick="done_todo('${num}',${done})"><i class="fa-regular fa-square"></i></button><h2>${todo}</h2><button  onclick="delete_todo('${num}')" class="fa-solid fa-trash"></button></li>`
                }else{
                     tempHtml = `<li><button onclick="done_todo('${num}',${done})"><i class="fa-solid fa-square-check"></i></button><h2 class="done"> ${todo}</h2> <button  onclick="delete_todo('${num}')" class="fa-solid fa-trash"></button></li>`
                }
                $('#main-screen__widget__todos__list').append(tempHtml);
            }
        }
    });
}
const todoInput = $('main-screen__widget__todos__submit')




function save_todo(){
    let todos = $('#main-screen__widget__todos__submit input').val();
    let myId= "";
    $.ajax({
        type: "POST",
        url: "/guhaejo/todos",
        data: {todo_give:todos,id_give:myId},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}
function done_todo(num,done){
    $.ajax({
        type: "POST",
        url: "/guhaejo/todos/done",
        data: {'num_give':num,'done_give':done},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

function delete_todo(num){
    $.ajax({
        type: "POST",
        url: "/guhaejo/todos/delete",
        data: {'num_give':num},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}
