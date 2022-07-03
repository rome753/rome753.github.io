
main();

function main() {
    readTextFile('blogJsonFile.txt');
}

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                handleJsonStr(allText);
            }
        }
    }
    rawFile.send(null);
}

function handleJsonStr(str) {
    var arr = str.split("\n");
    for (i = 0; i < arr.length; i++) {
        if (arr[i].length <= 2) {
            continue
        }
        var json = JSON.parse(arr[i]);
        for (j = 0; j < json.length; j++) {
            var data = json[j].object.data
            appendOne(data)
        }
    }
}

function appendOne(data) {
    var id = data.id
    var title = data.title
    var time = data.first_shared_at
    var slug = data.slug

    var node = document.getElementById('mybody')

    var h1 = document.createElement('h4')
    var h2 = document.createElement('h5')
    h2.innerHTML = time

    node.appendChild(h1)
    node.appendChild(h2)

    var a = document.createElement('a')
    a.innerHTML = title
    a.href = 'https://www.jianshu.com/p/' + slug
    h1.appendChild(a)
}