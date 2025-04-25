let d = document
let e = (id) => d.getElementById(id)

function initColorScheme() {
    let schemeButton = e('scheme-button')
    let schemeIcon = e('scheme-icon')
    let attrName = 'data-color-scheme'
    let key = 'colorScheme'
    let light = 'light'
    let dark = 'dark'
    let sunIcon = 'fa-cloud-sun'
    let moonIcon = 'fa-cloud-moon'

    let preferredScheme = localStorage.getItem(key)
    if (preferredScheme === null) {
        preferredScheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? dark : light
        localStorage.setItem(key, preferredScheme)
    }
    d.body.style.colorScheme = preferredScheme
    d.documentElement.setAttribute(attrName, preferredScheme)

    if (preferredScheme === dark) {
    } else {
        schemeIcon.classList.add(sunIcon)
    }

    function toggleScheme() {
        if (localStorage.getItem(key) === dark) {
            d.documentElement.setAttribute(attrName, light)
            schemeIcon.classList.replace(moonIcon, sunIcon)
            localStorage.setItem(key, light)
        } else {
            d.documentElement.setAttribute(attrName, dark)
            schemeIcon.classList.replace(sunIcon, moonIcon)
            localStorage.setItem(key, dark)
        }
    }
    schemeButton.addEventListener('click', toggleScheme)
}

initColorScheme()
