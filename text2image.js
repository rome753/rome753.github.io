


main();

function main() {
    console.log("hello js!")

    var node = document.getElementById('mybody')

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
                // alert(allText);
                handleJsonStr(allText);
            }
        }
    }
    rawFile.send(null);
}

function handleJsonStr(str) {
    var arr = str.split("\n");
    // var json = JSON.parse(str);
    console.log(arr.length);


    // for (i = 0; i < json.length; i++) {
    //     var data = json[i].object.data
    //     saveOneImage(data)
    // }

    // var node = document.getElementById('mybody')

    // domtoimage.toPng(node, {width: 800, height: 1200})
    //     .then(function(dataUrl) {
    //         var link = document.createElement('a')
    //         link.download = "all.png"
    //         link.href = dataUrl
    //         link.click()
    //     })
}


function saveOneImage(data) {
    var id = data.id
    var title = data.title
    var time = data.first_shared_at
    var slug = data.slug

    var node = document.getElementById('mybody')

    var h1 = document.createElement('h4')
    var h2 = document.createElement('h5')
    h1.innerHTML = title
    h2.innerHTML = time
    
    console.log(h1.offsetWidth)

    node.appendChild(h1)
    node.appendChild(h2)
}

function requestMyJianshuBlog() {
    var url = "https://www.jianshu.com/asimov/users/slug/6740854c6174/public_notes?order_by=top&page=7"

}

function requestPage() {
    var url = "https://www.jianshu.com/asimov/users/slug/6740854c6174/public_notes?order_by=top&page=7"
    var xhr = new XMLHttpRequest()
    xhr.open("GET", url, false)
    xhr.send(null)
    console.log(xhr.responseText)
}