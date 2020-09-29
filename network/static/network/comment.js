addEventListener('DOMContentLoaded', commentListeners);

function commentListeners() {
    let comment_btn = document.querySelectorAll('.comments-action');
    comment_btn.forEach(btn => {
        if (btn)
            btn.addEventListener('click', displayComments);
    });

    let post_btn = document.querySelectorAll('.post-action');
    post_btn.forEach(btn => {
        if (btn)
            btn.addEventListener('click', addComment);
    });
    let del_btn = document.querySelectorAll('.del-action');
    del_btn.forEach(btn => {
        if (btn)
            btn.addEventListener('click', delComment);
    });
}

function delComment(event) {
    event.preventDefault();
    // console.log(this);
    let post_id = this.dataset.post;
    let comment_id = this.dataset.comment;
    console.log('post_id', post_id);
    console.log('comment_id', comment_id);
    let counter = Number(this.dataset.counter) - 1;
    console.log('counter', counter);
    let comment = document.querySelector(`.comment-item-${post_id}-${comment_id}`);
    // console.log(comment);
    let csrftoken = getCookie('csrftoken');
    fetch(`/comments/del/${post_id}/${comment_id}`, {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        credentials: 'same-origin'
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            const ul_elem = document.querySelector(`.comment-list-${post_id}`);
            // console.log(ul_elem)
            ul_elem.removeChild(comment);
            document.querySelector(`.comment-counter-${post_id}`).innerHTML = counter;
        })
        .catch(error => {
            console.log(error);
        });
}

function addComment(event) {
    event.preventDefault();
    let btn = this;
    console.log(btn);
    let post_id = btn.dataset.post;
    let counter = Number(this.dataset.counter) + 1;
    let input = document.querySelector(`.form-comment-${post_id} input`);
    console.log(input);
    let value = input.value;
    input.value = '';
    if (value.length > 0) {
        let csrftoken = getCookie('csrftoken');
        fetch(`/comments/add/${post_id}`, {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            credentials: 'same-origin',
            body: JSON.stringify({ comment: value })
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                let months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.',
                    'Jul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
                console.log(data);
                let current_user = data['current_user'];
                let post_user = data['post_user'];
                let comment_id = data['comment_id'];
                let commented_by = data['commented_by'];
                // console.log('current user', current_user);
                // console.log('post_user', post_user);
                // console.log('comment_id', comment_id);
                let date = new Date();
                let hours = date.getHours();
                let min = date.getMinutes()
                let hours_short = hours;
                let total_min = (hours * 60) + min;
                const twelve_hours = 12 * 60;
                let pre_min = '';
                if (min < 10) {
                    pre_min = '0'
                }
                let ampm = 'a.m.';
                if (hours > 12) {
                    hours_short = hours - 12;
                }
                if (total_min > twelve_hours) {
                    ampm = 'p.m.';
                }
                let str_date = `${months[date.getMonth()]} ${date.getDate()}, 
                            ${date.getFullYear()},
                            ${hours_short}:${pre_min}${date.getMinutes()} ${ampm}`;
                let li_item = document.createElement('li');
                li_item.innerHTML = `(${str_date} by ${current_user}) ${value}`;
                let ul_elem = document.querySelector(`.comment-list-${post_id}`);
                let div_elem = document.createElement('div');
                div_elem.className = `comment-item comment-item-${post_id}-${comment_id}`
                div_elem.append(li_item);
                if (current_user == post_user || commented_by == current_user) {
                    let a_elem = document.createElement('a');
                    a_elem.className = "del-btn del-action";
                    a_elem.href = '#';
                    a_elem.dataset.post = post_id;
                    a_elem.dataset.comment = comment_id;
                    a_elem.innerHTML = 'delete';
                    a_elem.addEventListener('click', delComment);
                    let div2_elem = document.createElement('div');
                    div2_elem.append(a_elem);
                    div_elem.append(div2_elem);
                } else {
                    // <div><a class="del-btn text-white bg-white">delete</a></div>
                    let a_elem = document.createElement('a');
                    a_elem.className = "del-btn text-white bg-white";
                    a_elem.innerHTML = 'delete';
                    let div2_elem = document.createElement('div');
                    div2_elem.append(a_elem);
                    div_elem.append(div2_elem);
                }
                ul_elem.append(div_elem);
                document.querySelector(`.comment-counter-${post_id}`).innerHTML = counter;
            })
            .catch(error => {
                console.log(error);
            });
    }
}

function displayComments(event) {
    event.preventDefault();
    let post_id = this.dataset.post;
    // console.log('postid', post_id);

    let ul_elem = document.querySelector(`.comment-list-${post_id}`);
    // console.log('ul elem', ul_elem);
    if (ul_elem.classList.contains('hide-comments')) {
        ul_elem.classList.remove('hide-comments');
        ul_elem.classList.add('show-comments');
    } else {
        ul_elem.classList.remove('show-comments');
        ul_elem.classList.add('hide-comments');
    }
}