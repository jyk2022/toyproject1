$(document).ready(function(){
    $('#main-screen__widget__news__list').empty()
    show_news()
    });

    function show_news(){
    $.ajax({
    type: "GET",
    url: "/guhaejo/news",
    data: {},
    success: function (response) {
        let rows = response["news_list"];
        for (i = 0; i < rows.length; i++) {
             let company = rows[i]["company"];
              let url = rows[i]["url"];
              let title = rows[i]["title"];
               let tempHtml=`<li>
                <a href="${url}" target="_blank"
                  >${title} <span>-${company}</span></a
                >
              </li>`
            $("#main-screen__widget__news__list").append(tempHtml);

        }

    }
})
    }
