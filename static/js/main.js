function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var rating_question = $(".rating-question")

rating_question.find('.like-question').on('click', function (ev) {
    console.log('click like');
    const request = new Request(
        'http://127.0.0.1:8000/rating_set_question',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: JSON.stringify({question_id: $(this).data('id'), type: true})
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json => rating_question.find('#question-'+$(this).data('id')).text(response_json.new_rating)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});

rating_question.find('.dislike-question').on('click', function (ev) {
    console.log('click dislike');
    const request = new Request(
        'http://127.0.0.1:8000/rating_set_question',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: JSON.stringify({question_id: $(this).data('id'), type: false})
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json => rating_question.find('#question-'+$(this).data('id')).text(response_json.new_rating)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});

var rating_answer = $(".rating-answer")

rating_answer.find('.like-answer').on('click', function (ev) {
    console.log('click like');
    const request = new Request(
        'http://127.0.0.1:8000/rating_set_answer',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: JSON.stringify({answer_id: $(this).data('id'), type: true})
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json => rating_answer.find('#answer-'+$(this).data('id')).text(response_json.new_rating)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});

rating_answer.find('.dislike-answer').on('click', function (ev) {
    console.log('click dislike');
    const request = new Request(
        'http://127.0.0.1:8000/rating_set_answer',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: JSON.stringify({answer_id: $(this).data('id'), type: false})
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json => rating_answer.find('#answer-'+$(this).data('id')).text(response_json.new_rating)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});

$(".answer-is-right").on('click', function (ev) {
    console.log('click checkbox');
    const request = new Request(
        'http://127.0.0.1:8000/correct_set_answer',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: JSON.stringify({answer_id: $(this).data('id')})
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json =>  $(this).prop('checked', response_json.answer_is_right)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});