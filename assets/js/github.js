export function getCommStatus() {
    fetch('https://api.github.com/repos/qatoqat/qatoqat.github.io')
        .then(response => response.json())
        .then(data => {
            let descData = JSON.parse(data.description)
            if (descData?.commission) {
                let bgColor = descData.commission.bgColor
                let status = descData.commission.status
                let commDiv = document.getElementsByClassName("commission")?.[0]
                if (commDiv && bgColor) {
                    commDiv.style.backgroundColor = bgColor
                }

                let commStatus = document.getElementById("commission-status")
                if (commStatus && status) {
                    commStatus.innerText = status
                }
            }
        })
        .catch(error => {
            console.error('Error:', error)
        })
}