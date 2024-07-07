function talk() {
  console.log();
  data = {
    proofs: PROOF_DATA,
    amount: "700",
    uid: "09168886497",
  };
  console.log("Triggering SigmaB with data: ", data);
  window.dispatchEvent(new CustomEvent("TriggerSigmaB", { detail: data }));
}
