chrome.runtime.onMessage.addListener(function (request, sender) {
  let width = 350;
  let height = 690;
  let right = 100;
  let left = request.windowWidth - width - right;

  chrome.windows.create(
    {
      url: "popup.html",
      type: "popup",
      height: height,
      width: width,
      left: left,
      focused: true,
    },
    function (window) {
      chrome.tabs.onUpdated.addListener(function listener(
        tabId,
        changeInfo,
        tab
      ) {
        if (tabId === window.tabs[0].id && changeInfo.status === "complete") {
          chrome.tabs.sendMessage(tabId, { data: request.data });
          chrome.tabs.onUpdated.removeListener(listener);
        }
      });
    }
  );
});
