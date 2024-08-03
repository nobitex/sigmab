function talk() {
  console.log();
  data = {
    proofs: PROOF_DATA,
    amount: "",
    uid: "blue@gmail.com",
  };
  console.log("Triggering SigmaB with data: ", data);
  window.dispatchEvent(new CustomEvent("TriggerSigmaB", { detail: data }));
}
