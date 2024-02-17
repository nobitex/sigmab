chrome.runtime.onMessage.addListener(function (request, sender) {
    let width = 350;
    let height = 450;
    let right = 100;
    let left = request.options.message.windowWidth - width - right;
    
    chrome.windows.create({
        url: "popup.html",
        type: "popup",
        height: height,
        width: width,
        left: left,
        focused: true
    });
});

