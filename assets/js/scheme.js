// init color scheme so page wont flash
(function() {
    const key = 'colorScheme';
    let scheme = localStorage.getItem(key);
    if (!scheme) {
        scheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-color-scheme', scheme);
    if (scheme === 'light') document.body?.classList.add('light');
})();