addEventListener('DOMContentLoaded', listeners);

    function listeners(){

        // processing likes and unlikes
        let like_buttons = document.querySelectorAll('.like-btn')
        like_buttons.forEach(button => {
            button.addEventListener('click', processLike)
        });

         // script for processing editing of posts
        let edit_links = document.querySelectorAll('.edit');
        edit_links.forEach(link => {
            link.addEventListener('click', processEdit);
        });       
    }

    function processLike(){
        let button = this;
        let button_text = this.innerHTML;
        let post_id = this.id
        console.log(post_id, button_text);

        // update database
        let csrftoken = getCookie('csrftoken');
        fetch(`/update/${post_id}/likes`, {
            method:'PUT',
            headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
            },
            credentials: 'same-origin',
            body: JSON.stringify({action:button_text})
        })
        .then(response => {
            // console.log(response.status);
            return response.json();
        })
        .then(data => {
            console.log(data);
            if ('likes_count' in data){
                    // update number of likes
                    let count = data['likes_count'];
                    let counter_elem =  button.nextElementSibling;
                    counter_elem.innerHTML = count;
                    // update button text
                    button.innerHTML = data['next_action'];
                }
        })
        .catch(error => {
            console.log(error);
        });
    }

    function processEdit(event){
        event.preventDefault();
        // 'this' is the anchor 'edit' element
        let edit = this;
        let post_id = this.dataset.post;
        // post is the 'div' next to it
        let post = document.querySelector(`.post-text-${post_id}`);
        let post_text = post.innerHTML.replace(/(\r\n|\n|\r)/g, "").trim();
        post.innerHTML = `<textarea rows="2" cols="100">${post_text}</textarea>`;
        let textarea = document.querySelector('textarea');
        textarea.addEventListener('change', () => {
            let value = textarea.value.replace(/(\r\n|\n|\r)/g, "").trim();
            post.innerHTML = '';
            processTextArea(value, post, edit);
        });
        textarea.addEventListener('keydown', (event) => {
            if (event.key == 'Enter' || event.key == 'Escape'){
                let value = textarea.value.replace(/(\r\n|\n|\r)/g, "").trim();
                post.innerHTML = '';
                processTextArea(value, post, edit);
            }
        });
    }

function processTextArea(value, post, edit){
    let post_id = edit.dataset.post;
    post.innerHTML = value;
    // update database
    let csrftoken = getCookie('csrftoken');
    fetch(`/update/${post_id}/edit`, {
        method:'PUT',
        headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        "Content-Type": "application/json"
        },
        credentials: 'same-origin',
        body: JSON.stringify({newText:post.innerHTML})
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