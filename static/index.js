fetch('/text', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    console.log(data)
    renderedText = data["texts"].reduce((prev, curr, ind) => {
        return prev + `<p>Index ${ind}:\n${curr["text_section"]}</p>`
    }, "")
    document.getElementById("content-holder").innerHTML += renderedText
    
})
.catch(error => console.error('Error:', error));
