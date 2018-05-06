function getRequest(getURL, async, f) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', getURL, async);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (this.readyState == 4 && this.status == 200) {
            let res = JSON.parse(this.responseText);
            f(res);
        }
    };
    xhr.send();
}

function postRequest(postURL, json, async, f) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', postURL, async);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (this.readyState == 4 && this.status == 200) {
            let res = JSON.parse(this.responseText);
            f(res);
        }
    };
    xhr.send(JSON.stringify(json));
}
