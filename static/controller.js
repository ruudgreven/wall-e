function drive(direction) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/drive/" + direction, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function turn(direction) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/turn/" + direction, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function stop() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/stop", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}