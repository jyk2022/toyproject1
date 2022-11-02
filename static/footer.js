$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/guhaejo/review',
        data: {},
        success: function (response) {
            let reviews = response['reviews'];
            let imgList = response['imgList'];
            // console.log(reviews, imgList);
            for (let i = 0; i < reviews.length; i++) {
                const title = reviews[i]['title'];
                const img = imgList[i];
                const company = reviews[i]['company'];
                const comment = reviews[i]['comment'];
                const recomment = comment.substr(1, comment.length - 2);
                const temp_html = `<li class='swiper-slide'>
                                    <h1>${title}</h1>
                                    <img
                                        src=${img}
                                    />
                                    <h2>${company}</h2>
                                    <span>${recomment}</span>
                                </li>`
                $('#footer__reviewBox').append(temp_html);
            }
            new Swiper("#footer__inner.swiper", {
                autoplay: {
                    delay: 5000
                },
                loop: true,
                loopAdditionalSlides: 1,
                spaceBetween: 50, // 슬라이드 사이 여백
                slidesPerView: 3, // 한 슬라이드에 보여줄 갯수
            })
        }
    });
}, );