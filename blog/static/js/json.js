function printPre(elementId, url, data) {
    document.getElementById(elementId).innerHTML = '';

    var obj = document.createElement('pre');
    obj.style.cssText = 'border:0px';

    var element = document.getElementById(elementId).appendChild(obj);
    element.innerHTML = '호출주소 : ' + decodeURIComponent(url);

    var obj = document.createElement('pre');
    obj.style.cssText = 'border:0px';

    var element = document.getElementById(elementId).appendChild(obj);
    element.innerHTML = data;
}

function prettyJson(data) {
    return syntaxHighlight(JSON.stringify(JSON.parse(data), undefined, 4));
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}