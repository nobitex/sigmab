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

  var amonut = document.getElementById("amount");
  amonut.innerHTML = context.amount;

  var date = document.getElementById("date");
  let d = new Date();
  date.innerHTML = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`;

  var uid = document.getElementById("uid");
  uid.innerHTML = context.uid;
});

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

validationStages = [
  [
    "Checking if Merkle-Patricia-Trie nodes are chained with each other...",
    async function () {
      await sleep(500);
      for (var l = 0; l < context.proofs["mpt_path_data"].length; l++) {
        for (
          var i = context.proofs["mpt_path_data"][l].length - 1;
          i >= 1;
          i--
        ) {
          if (
            context.proofs["mpt_path_data"][l]["public_outputs"][i][1] !==
            context.proofs["mpt_path_data"][l]["public_outputs"][i - 1][0]
          ) {
            return false;
          }
        }

        if (
          context.proofs["mpt_path_data"][l]["public_outputs"][0][1] !==
          context.proofs["mpt_last_data"][l]["public_outputs"][0]
        ) {
          return false;
        }
      }

      return true;
    },
  ],
  [
    "Checking if the same salt is being used across account...",
    async function () {
      await sleep(500);
      var saltHashes = new Set();
      for (var l = 0; l < context.proofs["mpt_last_data"].length; l++) {
        saltHashes.add(context.proofs["mpt_last_data"][l]["public_outputs"][4]);
      }

      if (saltHashes.size > 1) {
        return false;
      }

      return true;
    },
  ],
  [
    "Checking if accounts are distinct...",
    async function () {
      await sleep(500);
      var ecdsaHashes = new Set();
      for (var l = 0; l < context.proofs["ecdsa_data"].length; l++) {
        if (
          ecdsaHashes.has(context.proofs["ecdsa_data"][l]["public_outputs"][1])
        ) {
          return false;
        }
        ecdsaHashes.add(context.proofs["ecdsa_data"][l]["public_outputs"][1]);
      }

      return true;
    },
  ],
  [
    "Checking if balances of distinct accounts are being added...",
    async function () {
      await sleep(500);
      var sbaHashes = new Set();
      for (
        var l = 0;
        l < context.proofs["sba_data"]["public_outputs"].length;
        l++
      ) {
        if (
          sbaHashes.has(context.proofs["sba_data"]["public_outputs"][l][0]) ||
          sbaHashes.has(context.proofs["sba_data"]["public_outputs"][l][1])
        ) {
          return false;
        }
        sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][0]);
        sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][1]);
      }
      return true;
    },
  ],
  [
    "Checking if the balances being added belong to the proven accounts...",
    async function () {
      await sleep(500);
      var sbaHashes = new Set();
      for (
        var l = 0;
        l < context.proofs["sba_data"]["public_outputs"].length;
        l++
      ) {
        if (l == 0) {
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][0]);
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][1]);
        } else {
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][0]);
        }
      }

      for (var l = 0; l < context.proofs["mpt_last_data"].length; l++) {
        console.log(context.proofs["mpt_last_data"][l]["public_outputs"][2]);
        if (
          !sbaHashes.delete(
            context.proofs["mpt_last_data"][l]["public_outputs"][2]
          )
        ) {
          return false;
        }
      }

      if (sbaHashes.size != 0) {
        return false;
      }

      return true;
    },
  ],
  [
    "check sba latest balance commitments is equal with solvency banlance commitment in pol circuit",
    async function () {
      var l = context.proofs["sba_data"]["public_outputs"].length;
      if (
        context.proofs["pol_data"]["public_outputs"][1] ==
        context.proofs["sba_data"]["public_outputs"][l - 1][2]
      ) {
        return true;
      }
      return false;
    },
  ],
  [
    "check ecdsa commitments is equal with mpt",
    async function () {
      var l = context.proofs["ecdsa_data"]["public_outputs"].length;
      if (
        context.proofs["ecdsa_data"]["public_outputs"][1] ==
        context.proofs["mpt_last_data"]["public_outputs"][l - 1][3]
      ) {
        return true;
      }
      return false;
    },
  ],
];

verifyStages = [
  [
    "Verifying the ECDSA signatures...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["ecdsa_data"].length; i++) {
        console.log(
          "ecdsa_data",
          context.proofs["ecdsa_data"][i]["public_outputs"]
        );
        try {
          if (
            await window.sigmab.verifyECDSA(
              context.proofs["ecdsa_data"][i]["public_outputs"],
              context.proofs["ecdsa_data"][i]["proof"]
            )
          ) {
            return true;
          }
        } catch (error) {
          console.error(error);
        }
      }
    },
  ],
  [
    "Verifying the Merkle-Patricia-Trie leaf nodes...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["mpt_last_data"].length; i++) {
        try {
          await window.sigmab.verifyMPTLast(
            context.proofs["mpt_last_data"][i]["public_outputs"],
            context.proofs["mpt_last_data"][i]["proof"]
          );
        } catch (error) {
          console.error(error);
          return false;
        }
      }
      return true;
    },
  ],
  [
    "Verifying the Merkle-Patricia-Trie intermediary nodes...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["mpt_path_data"].length; i++) {
        for (
          var j = 0;
          j < context.proofs["mpt_path_data"][i]["proofs"].length;
          j++
        ) {
          try {
            await window.sigmab.verifyMPTPath(
              context.proofs["mpt_path_data"][i]["public_outputs"][j],
              context.proofs["mpt_path_data"][i]["proofs"][j]
            );
          } catch (error) {
            console.error(error);
          }
        }
      }
      return true;
    },
  ],
  [
    "Verifying stealth balance additions...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["sba_data"]["proofs"].length; i++) {
        console.log(
          context.proofs["sba_data"]["public_outputs"][i],
          context.proofs["sba_data"]["proofs"][i]
        );
        try {
          await window.sigmab.verifySBA(
            context.proofs["sba_data"]["public_outputs"][i],
            context.proofs["sba_data"]["proofs"][i]
          );
        } catch (error) {
          console.error(error);
        }
      }
      return true;
    },
  ],
  [
    "Verifying existence in the liability tree...",
    async function () {
      await sleep(200);
      try {
        if (
          await window.sigmab.verifyPOL(
            context.proofs["pol_data"]["public_outputs"],
            context.proofs["pol_data"]["proof"]
          )
        ) {
          return true;
        }
      } catch (error) {
        console.error(error);
      }
    },
  ],
];

document.addEventListener("DOMContentLoaded", function () {
  var verifyButton = document.getElementById("verifyButton");

  var content = document.getElementById("content");
  var spinner = document.getElementById("progress");

  verifyButton.addEventListener("click", async function () {
    content.style.display = "none";
    spinner.style.display = "block";

    context.verification_state = "init";

    if (context.proof !== null) {
      for (var i = 0; i < validationStages.length; i++) {
        var spinnerStage = document.getElementById("spinner-stage");
        spinnerStage.innerHTML = validationStages[i][0];

        var result = await validationStages[i][1]();
        if (result) {
          console.log(`${validationStages[i][0]} passed`);
        } else {
          console.log(`${validationStages[i][0]} failed`);
          context.verification_state = `failed ${validationStages[i][0]}`;

          content.style.display = "block";
          spinner.style.display = "none";
          return;
        }
      }

      for (var i = 0; i < verifyStages.length; i++) {
        var spinnerStage = document.getElementById("spinner-stage");
        spinnerStage.innerHTML = verifyStages[i][0];

        var result = await verifyStages[i][1]();
        if (result) {
          context.verification_state = `passed ${verifyStages[i][0]}`;
          console.log(`${verifyStages[i][0]} passed`);
        } else {
          context.verification_state = `failed ${verifyStages[i][0]}`;
          console.log(`${verifyStages[i][0]} failed`);

          content.style.display = "block";
          spinner.style.display = "none";
          return;
        }
      }

      content.style.display = "block";
      spinner.style.display = "none";
      context.verification_state = "done";
    } else {
      content.style.display = "block";
      spinner.style.display = "none";
      context.verification_state = "no proof";
      alert("No proof to verify!");
    }
  });

  setInterval(function () {
    if (context.verification_state === null) {
      return;
    }

    var verificationResult = document.getElementById("result");
    var verificationResultText = document.getElementById("result-text");
    if (context.verification_state == "done") {
      verificationResult.style.display = "block";
      verificationResult.style.opacity = 1;
      verificationResult.style.backgroundColor = "green";
      verificationResultText.innerHTML = "Proof verified successfully";

      setInterval(function () {
        if (verificationResult.style.display == "none") return;
        verificationResult.style.opacity =
          verificationResult.style.opacity - 0.005;
      }, 10);
      setTimeout(function () {
        verificationResult.style.display = "none";
        verificationResult.style.opacity = 1;
      }, 2000);
    } else if (context.verification_state.startsWith("failed")) {
      verificationResult.style.display = "block";
      verificationResult.style.opacity = 1;
      verificationResult.style.backgroundColor = "red";
      verificationResultText.innerHTML = "Proof verification failed";

      setInterval(function () {
        if (verificationResult.style.display == "none") return;
        verificationResult.style.opacity =
          verificationResult.style.opacity - 0.005;
      }, 10);
      setTimeout(function () {
        verificationResult.style.display = "none";
        verificationResult.style.opacity = 1;
      }, 2000);
    }
    console.log(context.verification_state);
    context.verification_state = null;
  }, 100);
});
