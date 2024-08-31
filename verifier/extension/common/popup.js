const FIELD_SIZE =
  "21888242871839275222246405745257275088548364400416034343698204186575808495617";

var context = {
  proofs: null,
  amount: null,
  uid: null,
  verification_state: null,
};
var blockNumber = 20268439; // TODO :must come from proofs

function addSlice(array) {
  if (array.slice) {
    return array;
  }

  array.slice = function () {
    const args = Array.prototype.slice.call(arguments);
    return addSlice(new Uint8Array(Array.prototype.slice.apply(array, args)));
  };

  return array;
}

function isHexString(value, length) {
  if (typeof value !== "string" || !value.match(/^0x[0-9A-Fa-f]*$/)) {
    return false;
  }
  if (length && value.length !== 2 + 2 * length) {
    return false;
  }
  return true;
}

function isInteger(value) {
  return typeof value === "number" && value == value && value % 1 === 0;
}

function isBytes(value) {
  if (value == null) {
    return false;
  }

  if (value.constructor === Uint8Array) {
    return true;
  }
  if (typeof value === "string") {
    return false;
  }
  if (!isInteger(value.length) || value.length < 0) {
    return false;
  }

  for (let i = 0; i < value.length; i++) {
    const v = value[i];
    if (!isInteger(v) || v < 0 || v >= 256) {
      return false;
    }
  }
  return true;
}

function arrayify(value, options) {
  if (!options) {
    options = {};
  }

  if (typeof value === "number") {
    const result = [];
    while (value) {
      result.unshift(value & 0xff);
      value = parseInt(String(value / 256));
    }
    if (result.length === 0) {
      result.push(0);
    }

    return addSlice(new Uint8Array(result));
  }

  if (
    options.allowMissingPrefix &&
    typeof value === "string" &&
    value.substring(0, 2) !== "0x"
  ) {
    value = "0x" + value;
  }

  // if (isHexable(value)) { value = value.toHexString(); }

  if (isHexString(value)) {
    let hex = value.substring(2);
    if (hex.length % 2) {
      if (options.hexPad === "left") {
        hex = "0" + hex;
      } else if (options.hexPad === "right") {
        hex += "0";
      } else {
      }
    }

    const result = [];
    for (let i = 0; i < hex.length; i += 2) {
      result.push(parseInt(hex.substring(i, i + 2), 16));
    }

    return addSlice(new Uint8Array(result));
  }

  if (isBytes(value)) {
    return addSlice(new Uint8Array(value));
  }
}

function concat(items) {
  const objects = items.map((item) => arrayify(item));
  const length = objects.reduce((accum, item) => accum + item.length, 0);

  const result = new Uint8Array(length);

  objects.reduce((offset, object) => {
    result.set(object, offset);
    return offset + object.length;
  }, 0);

  return addSlice(result);
}

function toUtf8Bytes(str) {
  let result = [];
  for (let i = 0; i < str.length; i++) {
    const c = str.charCodeAt(i);

    if (c < 0x80) {
      result.push(c);
    } else if (c < 0x800) {
      result.push((c >> 6) | 0xc0);
      result.push((c & 0x3f) | 0x80);
    } else if ((c & 0xfc00) == 0xd800) {
      i++;
      const c2 = str.charCodeAt(i);

      if (i >= str.length || (c2 & 0xfc00) !== 0xdc00) {
        throw new Error("invalid utf-8 string");
      }

      // Surrogate Pair
      const pair = 0x10000 + ((c & 0x03ff) << 10) + (c2 & 0x03ff);
      result.push((pair >> 18) | 0xf0);
      result.push(((pair >> 12) & 0x3f) | 0x80);
      result.push(((pair >> 6) & 0x3f) | 0x80);
      result.push((pair & 0x3f) | 0x80);
    } else {
      result.push((c >> 12) | 0xe0);
      result.push(((c >> 6) & 0x3f) | 0x80);
      result.push((c & 0x3f) | 0x80);
    }
  }

  return arrayify(result);
}

function hexToBytes(hex) {
  if (hex.length % 2 !== 0) {
    hex = "0" + hex;
  }
  let bytes = [];
  for (let i = 0; i < hex.length; i += 2) {
    bytes.push(parseInt(hex.substr(i, 2), 16));
  }
  return bytes;
}

function hashMessage(message) {
  const messagePrefix = "\x19Ethereum Signed Message:\n";
  if (typeof message === "string") {
    message = toUtf8Bytes(message);
  }

  return window.keccak256(
    arrayify(
      concat([
        toUtf8Bytes(messagePrefix),
        toUtf8Bytes(String(message.length)),
        message,
      ])
    )
  );
}

function messageHash(message) {
  const eth_encoded_msg = toUtf8Bytes(message);
  const message_hash = window.sha256(eth_encoded_msg);

  const signable = BigInt("0x" + hashMessage(hexToBytes(message_hash)));

  function b2a(n, k, x) {
    const mod = BigInt(2 ** n);
    const ret = [];
    for (let i = 0; i < k; i++) {
      ret.push(x % mod);
      x = x / mod;
    }
    return ret.map(String);
  }

  return b2a(64, 4, signable);
}
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(async function (request, sender) {
  context.proofs = request.data["proofs"];
  context.amount = request.data["amount"]; //String(request.data["amount"] * WEI_PER_ETHER)
  context.uid = request.data["uid"];
  context.uid_salt = request.data["proofs"]["liability_salt"];

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
    let nodes = [
      "https://eth.llamarpc.com",
      "https://eth-mainnet.public.blastapi.io",
      "https://rpc.ankr.com/eth",
      "https://public.stackup.sh/api/v1/node/ethereum-mainnet",
      "https://nodes.mewapi.io/rpc/eth",
      "https://cloudflare-eth.com/",
    ];
    for (var idx in nodes) {
      let w = new window.Web3(nodes[idx]);
      try {
        let block = await w.eth.getBlock(blockNumber);
        var d = new Date(block.timestamp * 1000);

        dateElement.innerHTML += `( ${d.getFullYear()}/${d.getMonth() + 1
          }/${d.getDate()} )`;
        return true;
      } catch (error) {
        console.error(error);
        return false;
      }
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
  [
    "Check state-root on the block which proof provided is equal with the mpt last commitment in the proof",
    async function () {
      let nodes = [
        "https://eth.llamarpc.com",
        "https://eth-mainnet.public.blastapi.io",
        "https://rpc.ankr.com/eth",
        "https://public.stackup.sh/api/v1/node/ethereum-mainnet",
        "https://nodes.mewapi.io/rpc/eth",
        "https://cloudflare-eth.com/",
      ];
      for (var idx in nodes) {
        let w = new window.Web3(nodes[idx]);
        try {
          let block = await w.eth.getBlock(context.proofs["block_number"]);
          let stateRoot = BigInt(block.stateRoot) % BigInt(FIELD_SIZE);
          let len = context.proofs["mpt_path_data"].length;
          for (let i = 0; i < len; i++) {
            let pub_output_len =
              context.proofs["mpt_path_data"][i]["public_outputs"].length;
            if (
              stateRoot.toString() !==
              context.proofs["mpt_path_data"][i]["public_outputs"][
              pub_output_len - 1
              ][0]
            ) {
              continue;
            }
          }
          var d = new Date(block.timestamp * 1000);
          context.date = `${d.getFullYear()}/${d.getMonth() + 1
            }/${d.getDate()}`;
          return true;
        } catch (error) {
          continue;
        }
      }
      return "دسترسی به نود های عمومی اتریوم امکان‌پذیر نیست!";
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
  [
    "Verifying the ECDSA msg hash...",
    async function () {
      await sleep(200);
      const signableHash = messageHash("I am nobitex.ir!");

      for (let i = 0; i < context.proofs["ecdsa_data"].length; i++) {
        try {
          const publicOutputs =
            context.proofs["ecdsa_data"][i]["public_outputs"];
          if (
            publicOutputs[2] === signableHash[0] &&
            publicOutputs[3] === signableHash[1] &&
            publicOutputs[4] === signableHash[2] &&
            publicOutputs[5] === signableHash[3]
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
];

// Verification stages
const verifyStages = [
  [
    "Verifying existence in the liability tree...",
    async function () {
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
            BigInt(`0x${window.sha256(context.uid + "-" + context.uid_salt)}`) % BigInt(FIELD_SIZE) &&
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
  var verifyButton = document.getElementById("verifyButton");
  var checkbox = document.getElementById("accept");
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

  checkbox.addEventListener("change", () => {
    verifyButton.disabled = !checkbox.checked;
  });

  document.getElementById("close-btn").addEventListener("click", function () {
    window.close();
  });
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
        if (result === true) {
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
        if (result === true) {
          console.log(`${validationStages[i][0]} passed`);
        } else {
          if (result) {
            document.getElementById("result-details").innerHTML = result;
            console.log(result);
          }
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
      resultDetails = document.getElementById("result-details");
      resultDetails.innerHTML =
        "صادرکننده با موفقیت ثابت کرد که موجودی حساب کاربری شما را در حساب‌های اندوخته خود در نظر گرفته است.";
      verificationResult.style.display = "block";
    } else if (context.verification_state.startsWith("failed")) {
      resultImg = document.getElementById("result-img");
      verificationResult.style.display = "block";
      verificationResult.style.opacity = 1;
      resultImg.src = "./img/error.png"; // Change the path to the image you want to show on failure
      resultImg.style.width = "5rem";
      verificationResultText.innerHTML = "صحت‌سنجی با مشکل روبه رو شد";
    }
    context.verification_state = null;
  }, 100);
});