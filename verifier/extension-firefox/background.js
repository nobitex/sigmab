browser.runtime.onMessage.addListener(function (request, sender) {
  let width = 350;
  let height = 550;
  let right = 100;
  let left = request.windowWidth - width - right;

  browser.windows.create(
    {
      url: "popup.html",
      type: "popup",
      height: height,
      width: width,
      left: left,
      focused: true,
    },
    function (window) {
      browser.tabs.onUpdated.addListener(function listener(
        tabId,
        changeInfo,
        tab
      ) {
        if (tabId === window.tabs[0].id && changeInfo.status === "complete") {
          browser.tabs.sendMessage(tabId, { data: request.data });
          browser.tabs.onUpdated.removeListener(listener);
        }
      });
    }
  );
});
