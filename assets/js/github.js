export function getCommStatus() {
    fetch('https://api.github.com/repos/qatoqat/qatoqat.github.io')
        .then(response => response.json())
        .then(data => {
            let descData = JSON.parse(data.description)
            if (descData?.commission) {
                let url = descData.commission.url
                let bgColor = descData.commission.bgColor
                let status = descData.commission.status
                let commDiv = document.getElementsByClassName("commission")?.[0]
                let commStatus = document.getElementById("commission-status")
                if (commDiv && commStatus && url && bgColor && status) {
                    commDiv.href = url
                    commDiv.style.backgroundColor = bgColor
                    commStatus.innerText = status
                } else {
                    console.error('Error parsing commission data')
                }
            }
        })
        .catch(error => console.error('Error:', error))
}