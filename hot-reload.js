console.log("Hot reload is enabled");

let reloadInterval;
let wasPaused = false;

function startPolling() {
    reloadInterval = setInterval(() => {
        fetch("/__ping__")
            .then(res => res.text())
            .then(ts => {
                if (window.__last_reload_ts && window.__last_reload_ts !== ts) {
                    location.reload();
                }
                window.__last_reload_ts = ts;
            })
            .catch(() => {
            });
    }, 1000);
}

function stopPolling() {
    if (reloadInterval) {
        clearInterval(reloadInterval);
        reloadInterval = null;
    }
}

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        if (!reloadInterval) {
            startPolling();
            if (wasPaused) {
                console.log("Hot reload is resumed");
            }
        }
    } else {
        stopPolling();
        wasPaused = true;
        console.log("Hot reload is paused");
    }
});

if (document.visibilityState === 'visible') {
    startPolling();
}