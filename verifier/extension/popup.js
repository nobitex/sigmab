var context = {
    proofs: null,
    amount: null,
    uid: null,
    verification_state: null,
};

chrome.runtime.onMessage.addListener(async function (request, sender) {
    context.proofs = request.data["proofs"];
    context.amount = request.data["amount"];
    context.uid = request.data["uid"];

    var amonut = document.getElementById('amount');
    amonut.innerHTML = context.amount;

    var date = document.getElementById('date');
    let d = new Date();
    date.innerHTML = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`;

    var uid = document.getElementById('uid');
    uid.innerHTML = context.uid;
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

validationStages = [
    ["mpt chains validation", async function () {
        await sleep(500);
        for (var l = 0; l < context.proofs["MPT_PATH"].length; l++) {
            for (var i = context.proofs["MPT_PATH"][l].length - 1; i >= 1; i--) {
                if (context.proofs["MPT_PATH"][l][i]["pub"][1] !== context.proofs["MPT_PATH"][l][i - 1]["pub"][0]) {
                    return false;
                }
            }

            if (context.proofs["MPT_PATH"][l][0]["pub"][1] !== context.proofs["MPT_LAST"][l]["pub"][0]) {
                return false;
            }
        }

        return true;
    }],
]

verifyStages = [
    ["ecdsa verification", async function () {
        await sleep(200);
        for (var i = 0; i < context.proofs["ECDSA"].length; i++) {
            try {
                if (await window.sigmab.verifyECDSA(context.proofs["ECDSA"][i]["pub"], context.proofs["ECDSA"][i]["proof"])) {
                    return true;
                }
            } catch (error) {
                console.error(error);
            }
        }
    }],
    ["mpt last verification", async function () {
        await sleep(200);
        for (var i = 0; i < context.proofs["MPT_LAST"].length; i++) {
            try {
                if (await window.sigmab.verifyMPTLast(context.proofs["MPT_LAST"][i]["pub"], context.proofs["MPT_LAST"][i]["proof"])) {
                    return true;
                }
            } catch (error) {
                console.error(error);
            }
        }
    }],
    ["mpt path verifications", async function () {
        await sleep(200);
        for (var i = 0; i < context.proofs["MPT_PATH"].length; i++) {
            for (var j = 0; j < context.proofs["MPT_PATH"][i].length; j++) {
                try {
                    if (await window.sigmab.verifyMPTPath(context.proofs["MPT_PATH"][i][j]["pub"], context.proofs["MPT_PATH"][i][j]["proof"])) {
                        return true;
                    }
                } catch (error) {
                    console.error(error);
                }
            }
        }
    }],
    ["sba verification", async function () {
        await sleep(200);
        for (var i = 0; i < context.proofs["SBA"].length; i++) {
            try {
                if (await window.sigmab.verifySBA(context.proofs["SBA"][i]["pub"], context.proofs["SBA"][i]["proof"])) {
                    return true;
                }
            } catch (error) {
                console.error(error);
            }
        }
    }],
    ["pol verification", async function () {
        await sleep(200);
        try {
            if (await window.sigmab.verifyPOL(context.proofs["POL"]["pub"], context.proofs["POL"]["proof"])) {
                return true;
            }
        } catch (error) {
            console.error(error);
        }
    }],
];

document.addEventListener('DOMContentLoaded', function () {
    var verifyButton = document.getElementById('verifyButton');

    var content = document.getElementById('content');
    var spinner = document.getElementById('progress');


    verifyButton.addEventListener('click', async function () {
        content.style.display = 'none';
        spinner.style.display = 'block';

        context.verification_state = "init";

        if (context.proof !== null) {
            for (var i = 0; i < validationStages.length; i++) {
                var spinnerStage = document.getElementById('spinner-stage');
                spinnerStage.innerHTML = validationStages[i][0];

                var result = await validationStages[i][1]();
                if (result) {
                    console.log(`${validationStages[i][0]} passed`);
                } else {
                    console.log(`${validationStages[i][0]} failed`);

                    content.style.display = 'block';
                    spinner.style.display = 'none';
                    return;
                }
            }

            for (var i = 0; i < verifyStages.length; i++) {
                var spinnerStage = document.getElementById('spinner-stage');
                spinnerStage.innerHTML = verifyStages[i][0];

                var result = await verifyStages[i][1]();
                if (result) {
                    context.verification_state = `passed ${verifyStages[i][0]}`;
                    console.log(`${verifyStages[i][0]} passed`);
                } else {
                    context.verification_state = `failed ${verifyStages[i][0]}`;
                    console.log(`${verifyStages[i][0]} failed`);

                    content.style.display = 'block';
                    spinner.style.display = 'none';
                    return;
                }
            }

            content.style.display = 'block';
            spinner.style.display = 'none';
            context.verification_state = "done";
        } else {
            content.style.display = 'block';
            spinner.style.display = 'none';
            context.verification_state = "no proof";
            alert("No proof to verify!");
        }
    });

    setInterval(function () {
        if (context.verification_state === null) {
            return;
        }

        var verificationResult = document.getElementById('result');
        var verificationResultText = document.getElementById('result-text');
        if (context.verification_state == "done") {
            verificationResult.style.display = 'block';
            verificationResult.style.opacity = 1;
            verificationResult.style.backgroundColor = 'green';
            verificationResultText.innerHTML = "Proof verified successfully";

            setInterval(function () {
                if (verificationResult.style.display == 'none')
                    return;
                verificationResult.style.opacity = verificationResult.style.opacity - 0.005;
            }, 10);
            setTimeout(function () {
                verificationResult.style.display = 'none';
                verificationResult.style.opacity = 1;
            }, 2000);
        } else if (context.verification_state.startsWith("failed")) {
            verificationResult.style.display = 'block';
            verificationResult.style.opacity = 1;
            verificationResult.style.backgroundColor = 'red';
            verificationResultText.innerHTML = "Proof verification failed";

            setInterval(function () {
                if (verificationResult.style.display == 'none')
                    return;
                verificationResult.style.opacity = verificationResult.style.opacity - 0.005;
            }, 10);
            setTimeout(function () {
                verificationResult.style.display = 'none';
                verificationResult.style.opacity = 1;
            }, 2000);
        }
        console.log(context.verification_state)
        context.verification_state = null;
    }, 100);
});