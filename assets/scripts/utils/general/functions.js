export async function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

export function formatTimeToGameTime(elapsedTime) {
    const milliseconds = elapsedTime / 1000;
    const minutes = Math.floor(milliseconds / 60);
    const seconds = milliseconds % 60;

    const secondsFixed = seconds.toFixed(3)
    const secondsFormatted = seconds < 10 ? '0' + secondsFixed : secondsFixed;

    const dotPos = secondsFormatted.indexOf('.');
    const secondsToShow = secondsFormatted.substring(0, dotPos);
    const millisecondsToShow = secondsFormatted.substring(dotPos + 1);

    return `${minutes}:${secondsToShow}:${millisecondsToShow}`;
}