let owner = 'qatoqat'
let repo = 'qatoqat.github.io'

async function getLastSuccessfulDeployment() {
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
        return new Date()
    }

    let init = {headers: {'Accept': 'application/vnd.github+json'}}
    let res = await fetch(`https://api.github.com/repos/${owner}/${repo}/deployments`, init)
    for (let deployment of await res.json()) {
        let init = {headers: {'Accept': 'application/vnd.github+json'}}
        let statusRes = await fetch(deployment.statuses_url, init)
        if ((await statusRes.json()).some(s => s.state === 'success')) {
            return deployment.created_at
        }
    }

    return null
}

getLastSuccessfulDeployment().then(value => {
    if (value) {
        let last = document.getElementById('last-update')
        last.innerText = `Last update - ${(new Date(value)).toDateString()} | `
    }
})
