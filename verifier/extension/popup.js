var context = {
  proofs: null,
  amount: null,
  uid: null,
  verification_state: null,
};
var blockNumber = 20268439; // TODO :must come from proofs

// Listen for messages from the background script
chrome.runtime.onMessage.addListener(async function (request, sender) {
  context.proofs = request.data["proofs"];
  context.amount = request.data["amount"]; //String(request.data["amount"] * WEI_PER_ETHER)
  context.uid = request.data["uid"];

  let rootHash = BigInt(
    context.proofs["pol_data"]["public_outputs"][0]
  ).toString(16);

  // Update UI elements with received data
  var amountElement = document.getElementById("amount");
  amountElement.innerHTML = Web3.utils.fromWei(context.amount) + " ETH";

  var rootHashElement = document.getElementById("tree-root");
  rootHashElement.innerHTML = rootHash.slice(0, 12);

  var dateElement = document.getElementById("date");
  dateElement.innerHTML = `#${blockNumber} `;
  (async () => {
    let w = new window.Web3(
      "https://public.stackup.sh/api/v1/node/ethereum-mainnet"
    ); // TODO: Change this to the correct RPC endpoint
    try {
      // let blockN = await w.eth.getBlockNumber();
      let block = await w.eth.getBlock(blockNumber);
      var d = new Date(block.timestamp * 1000);

      dateElement.innerHTML += `( ${d.getFullYear()}/${
        d.getMonth() + 1
      }/${d.getDate()} )`;
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  })();

  var uidElement = document.getElementById("uid");
  uidElement.innerHTML = context.uid;
});

// Utility function to introduce a delay
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Validation stages
const validationStages = [
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
  // [
  //     "Check state-root on the block which proof provided is equal with the mpt last commitment in the proof",
  //     async function () {
  //         let w = new window.Web3("https://public.stackup.sh/api/v1/node/ethereum-mainnet"); // TODO: Change this to the correct RPC endpoint
  //         try {
  //             let block = await w.eth.getBlock(context.proofs["block_number"]);
  //             let stateRoot = w.utils.toBN(block.stateRoot);
  //             let len = context.proofs["mpt_path_data"].length;
  //             if (stateRoot.toString() !== context.proofs["mpt_last_data"][len - 1]["public_outputs"][0][0]) {
  //                 return false;
  //             }
  //             return true;
  //         } catch (error) {
  //             console.error(error);
  //             return false;
  //         }
  //     }
  // ],
  [
    "Checking if the same salt is being used across account...",
    async function () {
      await sleep(500);
      var saltHashes = new Set();
      for (var l = 0; l < context.proofs["mpt_last_data"].length; l++) {
        saltHashes.add(context.proofs["mpt_last_data"][l]["public_outputs"][4]);
      }
      return saltHashes.size <= 1;
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
        if (l === 0) {
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][0]);
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][1]);
        } else {
          sbaHashes.add(context.proofs["sba_data"]["public_outputs"][l][0]);
        }
      }
      for (var l = 0; l < context.proofs["mpt_last_data"].length; l++) {
        if (
          !sbaHashes.delete(
            context.proofs["mpt_last_data"][l]["public_outputs"][2]
          )
        ) {
          return false;
        }
      }
      return sbaHashes.size === 0;
    },
  ],
  [
    "Check SBA latest balance commitments is equal with solvency balance commitment in pol circuit",
    async function () {
      var l = context.proofs["sba_data"]["public_outputs"].length;
      return (
        context.proofs["pol_data"]["public_outputs"][1] ===
        context.proofs["sba_data"]["public_outputs"][l - 1][2]
      );
    },
  ],
  [
    "Check ECDSA commitments is equal with MPT",
    async function () {
      var l = context.proofs["ecdsa_data"].length;
      for (var i = 0; i < l; i++) {
        if (
          context.proofs["ecdsa_data"][i]["public_outputs"][1] !==
          context.proofs["mpt_last_data"][i]["public_outputs"][3]
        ) {
          return false;
        }
      }
      return true;
    },
  ],
];

// Verification stages
const verifyStages = [
  [
    "Verifying existence in the liability tree...",
    async function () {
      const FIELD_SIZE =
        "21888242871839275222246405745257275088548364400416034343698204186575808495617";
      await sleep(200);
      try {
        if (
          await window.sigmab.sigmab.verifyPOL(
            context.proofs["pol_data"]["public_outputs"],
            context.proofs["pol_data"]["proof"]
          )
        ) {
          if (
            BigInt(context.proofs["pol_data"]["public_outputs"][2]) ===
              BigInt(`0x${window.sha256(context.uid)}`) % BigInt(FIELD_SIZE) &&
            BigInt(context.proofs["pol_data"]["public_outputs"][3]) ===
              BigInt(context.amount)
          ) {
            return true;
          }
        }
      } catch (error) {
        console.error(error);
        return false;
      }
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
            await window.sigmab.sigmab.verifyMPTPath(
              context.proofs["mpt_path_data"][i]["public_outputs"][j],
              context.proofs["mpt_path_data"][i]["proofs"][j]
            );
          } catch (error) {
            console.error(error);
            return false;
          }
        }
      }
      return true;
    },
  ],
  [
    "Verifying the ECDSA signatures...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["ecdsa_data"].length; i++) {
        try {
          if (
            await window.sigmab.sigmab.verifyECDSA(
              context.proofs["ecdsa_data"][i]["public_outputs"],
              context.proofs["ecdsa_data"][i]["proof"]
            )
          ) {
            return true;
          }
        } catch (error) {
          console.error(error);
          return false;
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
          await window.sigmab.sigmab.verifyMPTLast(
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
    "Verifying stealth balance additions...",
    async function () {
      await sleep(200);
      for (var i = 0; i < context.proofs["sba_data"]["proofs"].length; i++) {
        try {
          await window.sigmab.sigmab.verifySBA(
            context.proofs["sba_data"]["public_outputs"][i],
            context.proofs["sba_data"]["proofs"][i]
          );
        } catch (error) {
          console.error(error);
          return false;
        }
      }
      return true;
    },
  ],
];

// DOMContentLoaded event listener to initialize the script
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("close-btn").addEventListener("click", function () {
    window.close();
  });

  var verifyButton = document.getElementById("verifyButton");

  var content = document.getElementById("content");
  var spinner = document.getElementById("progress");
  var verificationResult = document.getElementById("result");
  var verificationResultText = document.getElementById("result-text");
  var progressStages = [];
  for (let i = 0; i < 6; i++) {
    progressStages.push({
      progressLevel: document.getElementById(`progress-${i + 1}`),
      progressBorder: document.getElementById(`progress-${i + 1}-border`),
    });
  }

  var submitResult = document.getElementById("submit-result");
  var closeBtn = document.getElementById("close-btn");

  submitResult.addEventListener("click", () => {
    window.close();
    verificationResult.style.display = "none";
  });

  verifyButton.addEventListener("click", async function () {
    content.style.display = "none";
    spinner.style.display = "block";
    context.verification_state = "init";
    if (context.proofs !== null) {
      for (var i = 0; i < verifyStages.length; i++) {
        i >= 1
          ? progressStages[i - 1].progressBorder.classList.add("border-purple")
          : null;
        progressStages[i].progressLevel.classList.add("active-step");

        var result = await verifyStages[i][1]();
        if (result) {
          context.verification_state = `passed ${verifyStages[i][0]}`;
          console.log(`${verifyStages[i][0]} passed`);
        } else {
          context.verification_state = `failed ${verifyStages[i][0]}`;
          console.log(`${verifyStages[i][0]} failed`);
          spinner.style.display = "none";
          return;
        }
      }

      for (var i = 0; i < validationStages.length; i++) {
        var result = await validationStages[i][1]();
        if (result) {
          console.log(`${validationStages[i][0]} passed`);
        } else {
          console.log(`${validationStages[i][0]} failed`);
          context.verification_state = `failed ${validationStages[i][0]}`;
          spinner.style.display = "none";
          return;
        }
      }

      progressStages[4].progressBorder.classList.add("border-purple");
      progressStages[5]?.progressLevel.classList.add("active-step");

      setInterval(() => {
        spinner.style.display = "none";
        context.verification_state = "done";
      }, 3000);
    } else {
      spinner.style.display = "none";
      context.verification_state = "no proof";
      alert("No proof to verify!");
    }
  });

  setInterval(function () {
    if (context.verification_state === null) {
      return;
    }

    if (context.verification_state == "done") {
      verificationResult.style.display = "block";
    } else if (context.verification_state.startsWith("failed")) {
      resultImg = document.getElementById("result-img");
      verificationResult.style.display = "block";
      verificationResult.style.opacity = 1;
      resultImg.src = "./img/error.png"; // Change the path to the image you want to show on failure
      resultImg.style.width = "5rem";
      verificationResultText.innerHTML = "صحت سنجی با مشکل روبه رو شد";
    }
    context.verification_state = null;
  }, 100);
});
