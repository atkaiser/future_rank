function createRounds(players) {
    var rounds = [players];
    while (rounds[rounds.length-1].length > 1) {
        var newRound = [];
        var lastRound = rounds[rounds.length-1];
        for (var i = 0; i < lastRound.length; i += 2) {
            var winner;
            if (seeds[lastRound[i]] > seeds[lastRound[i+1]]) {
                winner = lastRound[i+1];
            } else {
                winner = lastRound[i];
            }
            newRound.push(winner);
        }
        rounds.push(newRound);
    }
    return rounds
}