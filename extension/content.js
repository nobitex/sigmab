chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'convert') {
        document.documentElement.style.filter = 'grayscale(100%)';
        sendResponse({ message: 'Website converted to black and white.' });
    } else if (request.action === 'reset') {
        document.documentElement.style.filter = 'none';
        sendResponse({ message: 'Website reset to original colors.' });
    }
});