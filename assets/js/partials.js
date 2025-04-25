
function loadPartials() {
    for (let p of document.querySelectorAll('a.partial')) {
        let url = p.href;
        if (url) {

            fetch(url).then(r => r.text().then(t => {
                if (t.startsWith('<!--partial-->')) {
                    let parent = p.parentNode
                    p.outerHTML = t
                    console.log(p)
                    for (let s of parent.querySelectorAll('script.partial')) {
                        s.removeAttribute('class')
                        let src = s.src
                        if (src) {
                            console.log(src)
                            let script = document.createElement('script');
                            script.src = src
                            document.head.appendChild(script)
                            script.remove()
                        }
                    }
                } else {
                    throw 'partial error(' + url + '): missing magic text'
                }
            })).catch(e => console.error(e))
        }
    }

}

loadPartials()
document.getElementById('main').style.opacity = '1'