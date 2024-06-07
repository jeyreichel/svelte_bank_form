export function setTokenWithExpiry(tokenKey, tokenValue) {
    const expiryInMinutes = 10;
    const now = new Date();

    let item = localStorage.getItem(tokenKey);
    let expiryTime;
    try {
        if (item) {
            // If the token already exists, retain the original expiry time
            item = JSON.parse(item);
            expiryTime = item.expiry;
        } else {
            // If the token does not exist, set a new expiry time
            expiryTime = now.getTime() + expiryInMinutes * 60000;
        }
    } catch (e) {
        expiryTime = now.getTime() + expiryInMinutes * 60000;
    }

    localStorage.setItem(tokenKey, JSON.stringify({value: tokenValue, expiry: expiryTime}));
}

// Function to check and get the token
export function getTokenWithExpiry(tokenKey) {
    const itemStr = localStorage.getItem(tokenKey);
    if (!itemStr) {
        return null;
    }
    try {
        const item = JSON.parse(itemStr);
        const now = new Date();

        if (now.getTime() > item.expiry) {
            localStorage.removeItem(tokenKey);
            return null;
        }

        return item.value;
    } catch (e) {
        return null
    }
}

export function changeStep(step, backward = false) {
    step = backward ? step - 1 : step + 1
    setTokenWithExpiry('step', step.toString());
    return step
}
