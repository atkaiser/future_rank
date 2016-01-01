function isInArray(value, array) {
    for(var i = 0; i < array.length; i++) {
        if (array[i] === value) {
            return true;
        }
    }
    return false;
}

function numRounds(rounds) {
    return rounds.length - 1;
}