let date;
let name;
let content;
let template = ``;

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
        console.log(data)
        document.getElementById("feed").innerHTML = "<h1>" + data.friends_updates[0].name + "</h1><br>";
        
        });
    }
