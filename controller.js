
function updateStatus() {
    let text = document.getElementById("status-input").value;
    const xmlhttp = new XMLHttpRequest();
    let url = "updatestatus="+text;
    xmlhttp.open("PUT", url, true);
    xmlhttp.send();
    document.getElementById("status-input").value = "";
}

function getJson(url, callback) {
    const xmlhttp = new XMLHttpRequest();
    
    xmlhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
        try {
            const data = JSON.parse(this.responseText);
            callback(null, data);
        }
        catch(err) {
            callback(err);
        }
        }
        else {
        callback(new Error("Sorry something went wrong with your request, try again later."))
        }
    };
    
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    }

function friendsUpdate() {
    getJson("friends.html?update_feed=true", (err, data) => {
        if (err) {
        console.warn(err);
        return
        }
        let load = "";
        for(let i in data.friends_updates) {
            console.log(data.friends_updates[i]);
            let friend = data.friends_updates[i];
            console.log(friend.picture)
            load += `<div class="status-container">
                   
                    <article class="card">
                        <img src="${friend.picture}" alt=""></img>
                    </article>
    
                    <article class="card">
                        <div class="right-card">
                            <div class="top-row">
                                <h4>${friend.name}</h4>
                                <h4>${friend.timestamp}</h4>
                            </div>
                        </div>
    
                        <div class="right-card">
                            <div class="middle-row">
                                <p>${friend.status}</p>
                            </div>
                        </div>
    
                        <div class="right-card">
                            <div class="likes-row">
                                <p id="${friend.feed_id}">${friend.likes} Likes</p>
                                <button
                                type="submit"
                                id="like_button"
                                class="btn"
                                onclick="updateLike('${friend.feed_id}', '${friend.name}')">
                                Like</button>
                            </div>
                        </div>
                    </article>
            </div>`
        };
        console.log(load)
        document.getElementById("content").innerHTML = load;

        });
    }

    function updateLike(id, name) {
        console.log(id)
        const xmlhttp = new XMLHttpRequest();
        let url = "updatelikes=func&feed_id="+id+"&friend_name="+name;
        xmlhttp.open("PUT", url, true);
        xmlhttp.send();
        location.reload()

    }
