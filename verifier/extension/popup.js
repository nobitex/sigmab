var context = { proof: null };

chrome.runtime.onMessage.addListener(async function (request, sender) {
    context.proof = request.data;
});

document.addEventListener('DOMContentLoaded', function () {
    var verifyButton = document.getElementById('verifyButton');

    verifyButton.addEventListener('click', function () {
        if(context.proof !== null) {
            alert(context.proof);
            window.sigmab.verifySigmaB();
        }
    });
});