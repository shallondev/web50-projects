
function saveHandler(postId) {
    // Get textarea
    const textareaContent = document.getElementById('textarea_' + postId).value;
    
    // Get token
    const formData = new FormData(document.getElementById('postForm'));
    const csrfToken = formData.get('csrfmiddlewaretoken');

    // Send to backend
    fetch('/update_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            post_id: postId,
            new_content: textareaContent
        })
        })
        // Send content to model
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update post content');
            }
            return response.json();
        })
        // Update DOM with content
        .then(result => {
            const postId = result.post_id; // Assuming the backend returns the updated post ID
            const newContent = result.new_content; // Assuming the backend returns the updated content
            const postContentElement = document.getElementById('postcontent' + postId);
            if (postContentElement) {
                postContentElement.textContent = newContent;
            }
        })
}

function likeHandler(postId) {

    // Get token
    const formData = new FormData(document.getElementById('likeForm'));
    const csrfToken = formData.get('csrfmiddlewaretoken');

        // Send to backend for updating likes
        fetch('/update_like/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                post_id: postId,
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update likes');
            }
            return response.json();
        })
        .then(result => {
            console.log('JSON response:', result);
            const postId = result.post_id; 
            const post_likes = result.post_likes; 
            const likesElement = document.getElementById('likes_' + postId);
            if (likesElement) { 
                likesElement.textContent = post_likes;
            }

            const likeBtn = document.getElementById('likeBtn_' + postId);

            if (likeBtn.innerHTML === 'Like') {
                likeBtn.innerHTML = 'Unlike';
            } else {
                likeBtn.innerHTML = 'Like';
            }

            if (likeBtn.classList.contains('btn-danger')) {
                likeBtn.classList.remove('btn-danger');
                likeBtn.classList.add("btn-success");
            } else {
                likeBtn.classList.remove("btn-success");
                likeBtn.classList.add('btn-danger');
            }

        })
}