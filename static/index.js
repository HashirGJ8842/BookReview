document.addEventListener("DOMContentLoaded", () => {
    var title = document.querySelector('#title_')
    var author = document.querySelector('#author_')
    var isbn = document.querySelector('#ISBN_')
    title.addEventListener("click", () => {
        console.log('Test')
        document.querySelector('#title').setAttribute('style', 'display:block')
        document.querySelector('#author').setAttribute('style', 'display:none')
        document.querySelector('#isbn').setAttribute('style', 'display:none')
    })
    author.addEventListener("click", () => {
        console.log('Test')
        document.querySelector('#author').setAttribute('style', 'display:block')
        document.querySelector('#title').setAttribute('style', 'display:none')
        document.querySelector('#isbn').setAttribute('style', 'display:none')
    })
    isbn.addEventListener("click", () => {
        console.log('Test')
        document.querySelector('#isbn').setAttribute('style', 'display:block')
        document.querySelector('#title').setAttribute('style', 'display:none')
        document.querySelector('#author').setAttribute('style', 'display:none')
    })

})
