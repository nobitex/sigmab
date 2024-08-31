function talk() {
  console.log();
  data = {
    proofs: PROOF_DATA,
    amount: "13768760000",
    uid: "p.toolabi@yahoo.com"
  };
  console.log("Triggering SigmaB with data: ", data);
  window.dispatchEvent(new CustomEvent("TriggerSigmaB", { detail: data }));
}
