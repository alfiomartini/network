addEventListener('DOMContentLoaded', listeners);

function listeners() {

    // processing likes and unlikes
    let like_buttons = document.querySelectorAll('.like-action')
    like_buttons.forEach(btn => {
        if (btn)
            btn.addEventListener('click', processLike)
    });

    // script for processing editing of posts
    let edit_links = document.querySelectorAll('.edit-action');
    edit_links.forEach(btn => {
        if (btn)
            btn.addEventListener('click', processEdit);
    });

    // script for processing deletion of posts
    let delete_posts = document.querySelectorAll('.del-post-action');
    delete_posts.forEach(btn => {
        if (btn)
            btn.addEventListener('click', deletePost);
    });
}

function deletePost(event) {
    event.preventDefault();
    const del_btn = this;
    const post_id = del_btn.dataset.post;
    const post = document.querySelector(`.post-wrapper-${post_id}`);

    
    // update database
    let csrftoken = getCookie('csrftoken');
    fetch(`/post/delete/${post_id}`, {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        credentials: 'same-origin'
    })
    .then(response => {
        // console.log(response.status);
        return response.text();
    })
    .then(data => {
        const container = document.querySelector('.posts-container');
        container.removeChild(post);
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    });
}

function processLike() {
    let button = this;
    let button_text = this.innerHTML;
    let post_id = this.id
    console.log(post_id, button_text);

    // update database
    let csrftoken = getCookie('csrftoken');
    fetch(`/update/${post_id}/likes`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        credentials: 'same-origin',
        body: JSON.stringify({ action: button_text })
    })
    .then(response => {
        // console.log(response.status);
        return response.json();
    })
    .then(data => {
        console.log(data);
        if ('likes_count' in data) {
            // update number of likes
            let count = data['likes_count'];
            let counter_elem = button.nextElementSibling;
            counter_elem.innerHTML = count;
            // update button text
            button.innerHTML = data['next_action'];
        }
    })
    .catch(error => {
        console.log(error);
    });
}

function processEdit(event) {
    event.preventDefault();
    // 'this' is the anchor 'edit' element
    let edit = this;
    let post_id = this.dataset.post;
    let post = document.querySelector(`.post-text-${post_id}`);
    console.log('post before cleaning', post);
    const post_text = post.innerHTML.replace(/(\r\n|\n|\r)/g, "").trim();
    const textarea = document.createElement('textarea');
    textarea.style.width = '100%';
    textarea.rows = '2';
    textarea.innerHTML = post_text;
    post.innerHTML = '';
    post.appendChild(textarea);
    console.log('textarea appended', post);

    textarea.addEventListener('keydown', (event) => {
        if (event.key == 'Enter' || event.key == 'Escape') {
            let value = textarea.value.replace(/(\r\n|\n|\r)/g, "").trim();
            console.log('value', value);
            post.innerHTML = '';
            processTextArea(value, post, edit);
        }
    });
}

function processTextArea(value, post, edit) {
    let post_id = edit.dataset.post;
    post.innerHTML = value;
    // update database
    let csrftoken = getCookie('csrftoken');
    fetch(`/update/${post_id}/edit`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        credentials: 'same-origin',
        body: JSON.stringify({ newText: post.innerHTML })
    })
    .then(response => {
        console.log(response.status);
        return response.text();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    });
}