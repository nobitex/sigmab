chrome.runtime.onMessage.addListener(function (request, sender) {
    let width = 350;
    let height = 550;
    let right = 100;
    let left = request.windowWidth - width - right;

    chrome.windows.create({
        url: "popup.html",
        type: "popup",
        height: height,
        width: width,
        left: left,
        focused: true
    }, function (window) {
        setTimeout(function () {
            chrome.tabs.sendMessage(window.tabs[0].id, { data: request.data });
        }, 1000);
    });
});
