window.addEventListener(
  "TriggerSigmaB",
  function (evt) {
    chrome.runtime.sendMessage({
      data: evt.detail,
      windowWidth: window.outerWidth,
    });
  },
  false
);
