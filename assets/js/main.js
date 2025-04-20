let d = document
let e = (id) => d.getElementById(id)
let listen = (o, t, f) => o.addEventListener(t, f)

function initColorScheme() {
    let schemeButton = e('scheme-button')
    let schemeIcon = e('scheme-icon')
    let key = 'colorScheme'

    let preferredScheme = localStorage.getItem(key)
    if (preferredScheme === null) {
        preferredScheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
        localStorage.setItem(key, preferredScheme)
    }
    document.body.style.colorScheme = preferredScheme
    document.documentElement.setAttribute("data-color-scheme", preferredScheme)

    if (preferredScheme === 'dark') {
        schemeIcon.className = 'fa-solid fa-cloud-moon'
    } else {
        schemeIcon.className = 'fa-solid fa-cloud-sun'
    }

    function toggleScheme() {
        if (localStorage.getItem(key) === 'dark') {
            d.documentElement.setAttribute("data-color-scheme", "light")
            schemeIcon.classList.replace('fa-cloud-moon', 'fa-cloud-sun')
            localStorage.setItem(key, 'light')
        } else {
            d.documentElement.setAttribute("data-color-scheme", "dark")
            schemeIcon.classList.replace('fa-cloud-sun', 'fa-cloud-moon')
            localStorage.setItem(key, 'dark')
        }
    }

    listen(schemeButton, 'click', toggleScheme)
}

listen(d, 'DOMContentLoaded', async _ => {
    initColorScheme()
    let discord = await import('./discord.js');
    discord.updateOnlineCount()
})