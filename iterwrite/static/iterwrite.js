document.addEventListener('DOMContentLoaded', () => {

     document.querySelector('#comment-toggle').onclick = toggleComments;
})

function addComment() {

    return ('todo');

}

function edit(id) {
    
    const editor = document.querySelector('#editor')
    const my_paper = document.querySelector('#paper');

    const edit = document.querySelector('#edit');
    edit.style.display = 'none';
    
    my_paper.style.display = 'none';
    var quill = new Quill(editor, {
        placeholder: 'Compose an epic...',
        theme: 'snow'
    });

    const done = document.querySelector('#done');
    done.style.display = 'block';
    done.onclick = function () {
        my_paper.innerHTML = document.querySelector('.ql-editor').innerHTML;
        edit.style.display = 'block';
        done.style.display = 'none';
        my_paper.style.display = 'block';
        editor.style.display = 'none';
        document.querySelector('.ql-toolbar').remove()
    }

    editor.style.display = 'block';
    editor.onkeyup = function() {
        var content = document.querySelector('.ql-editor').innerHTML;
        fetch(`edit`, {
            method: 'PUT',
            body: JSON.stringify({
                id: id,
                content: content
            }),
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
    }    
}

function toggleComments() {
    const comments = document.querySelector('#comments');
    if (comments.style.display != 'block') {
        document.querySelector('#edit').style.display = 'none';
        comments.style.display = 'block';
        this.value = 'Close';
        this.className = 'btn btn-danger';
    } else {
        comments.style.display = 'none';
        document.querySelector('#edit').style.display = 'block';
        this.value = 'Comments';
        this.className = 'btn btn-primary';
    }
        text = window.getSelection();
        if (text != '') {
            const selection = document.querySelector('#selection');
            selection.value = text;
            selection.style.visibility = 'visible';
        }

}

function findText(text) {
    const paper = document.querySelector('#paper');
    var content = paper.innerHTML;
    const selection = `<span style="background-color: red; color: white;">${text}</span>`;
    content = content.replace(text, selection);
    paper.innerHTML = content;
    toggleComments();

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}