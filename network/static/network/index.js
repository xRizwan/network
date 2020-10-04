document.addEventListener('DOMContentLoaded', () => {
    let editbtns = document.getElementsByClassName('edit-btn');
    let likebtns = document.getElementsByClassName('like-btn');
    let followbtns = document.getElementsByClassName('followbtn');

    if (editbtns.length > 0) {
        // converting node list to a javascript array
        editbtns = [...editbtns]
        editbtns.forEach(btn => {
            btn.addEventListener('click', () => allowEdit(btn.id))        
        });
    }

    if (likebtns.length > 0) {
        // converting node list to a javascript array
        likebtns = [...likebtns]

        likebtns.forEach(btn => {
            btn.addEventListener('click', (event) => likePost(btn.dataset.post, event))
        });
    }

    if (followbtns.length > 0) {
        // converting element list to javascript array

        followbtns = [...followbtns]

        followbtns.forEach(btn => {
            btn.addEventListener('click', (event) => follow(btn.id, event))
        })
    }
})

function follow(user_name, event) {
    let target = event.target
    let targetParent = target.parentElement
    let total = parseInt(target.dataset.followers)
    console.log(total)

    fetch(`/managefollowing/${user_name}`, {
        method: 'POST',
        body: JSON.stringify({
            'follow' : true,
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response)
        if (response.message === "followed") {
            event.target.dataset.followers = total + 1;
            event.target.innerText = 'Unfollow';
            targetParent.querySelector('.followers').innerText = `${total + 1} Followers`

        } else if(response.message === "unfollowed") {
            event.target.dataset.followers = total - 1;
            event.target.innerText = 'Follow';
            targetParent.querySelector('.followers').innerText = `${total - 1} Followers`
        }
    })
}

function likePost(post_id, event){
    let target = event.target
    let counter = target.parentElement.querySelector('.like-counter')
    console.log(counter)
    fetch(`/postinformation/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            'like': true,
        })
    }).then(response => response.json())
    .then(response => {
        if (response.message === 'liked'){
            counter.innerText = parseInt(counter.innerText) + 1
        }
        else if(response.message === 'unliked'){
            counter.innerText = parseInt(counter.innerText) - 1
        }
    })
}

function allowEdit(id) {
    let field = document.querySelector(`#message${id}`)
    message = field.dataset.message
    field.innerHTML = `
    
    <textarea class='form-control' id="addition" required>${message}</textarea>
    <button class="btn btn-primary savebtn">Save</button> 
    <button class="btn btn-primary cancelbtn">Cancel</button>
    `
    field.querySelector('.savebtn').addEventListener('click', () => {
        field.querySelector('#addition').disabled = true;
        val = field.querySelector('#addition').value
        console.log(val)

        fetch(`/postinformation/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                message: val,
            })
        })
        .then(response => response.json())
        .then(response => {
            if (response.error){
                alert(response.error)
            } else {
                field.dataset.message = val
                field.innerHTML = `${val}`
            }
        })
    })

    field.querySelector('.cancelbtn').addEventListener('click', () => {
        field.innerHTML = `${message}`
    })   
}
