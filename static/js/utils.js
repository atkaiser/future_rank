/**
 * Returns true if the value is in the array, otherwise false
 */
function isInArray(value, array) {
    for(var i = 0; i < array.length; i++) {
        if (array[i] === value) {
            return true;
        }
    }
    return false;
}

/**
 * Calculates how many rounds are in a tournament.
 */
function numRounds(rounds) {
    return rounds.length - 1;
}