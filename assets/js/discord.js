export function updateOnlineCount() {

    fetch('https://discord.com/api/v10/invites/bSDPbbdkCb?with_counts=true')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const onlineCount = data.approximate_presence_count;
            document.getElementById('online-status').innerText = onlineCount + ' online';
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
