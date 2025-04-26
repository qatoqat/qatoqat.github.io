const owner = 'qatoqat';
const repo = 'qatoqat.github.io';

async function getLastSuccessfulDeployment() {
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
        return
    }
    const res = await fetch(`https://api.github.com/repos/${owner}/${repo}/deployments`, {
        headers: {
            'Accept': 'application/vnd.github+json'
        }
    });

    const deployments = await res.json();

    for (const deployment of deployments) {
        const statusRes = await fetch(deployment.statuses_url, {
            headers: {
                'Accept': 'application/vnd.github+json'
            }
        });

        const statuses = await statusRes.json();
        const isSuccessful = statuses.some(s => s.state === 'success');

        if (isSuccessful) {
            console.log('Last Successful Deployment Time:', deployment.created_at);
            return deployment.created_at;
        }
    }

    console.log('No successful deployments found.');
}

getLastSuccessfulDeployment().then(value => {
    if (value) {
        let last = document.getElementById('last-update')
        last.innerText = 'Last update - ' + (new Date(value)).toDateString() + ' | '
    }
});
