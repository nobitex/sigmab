window.addEventListener(
  "TriggerSigmaB",
  function (evt) {
    browser.runtime.sendMessage({
      data: evt.detail,
      windowWidth: window.outerWidth,
    });
  },
  false
);

window.addEventListener("CheckExtensionInstalled", function () {
  window.dispatchEvent(new CustomEvent("ExtensionIsInstalled"));
});
