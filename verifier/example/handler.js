function talk() {
  console.log();
  data = {
    proofs: PROOF_DATA,
    amount: "13768760000",
    uid: "blue@gmail.com",
    liability_salt: "ebbbcd268156dbd845744be48ab6df3118d42e87c1bd36e789ea5944ffd6fdc5"
  };
  console.log("Triggering SigmaB with data: ", data);
  window.dispatchEvent(new CustomEvent("TriggerSigmaB", { detail: data }));
}
