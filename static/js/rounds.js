/**
 * Fills out the rest of the bracket, showing who advances for each round based
 * on the seeds given.
 */
function createRounds(players, seeds) {
    var match = 0;
    var rounds = [players];
    while (rounds[rounds.length-1].length > 1) {
        var newRound = [];
        var lastRound = rounds[rounds.length-1];
        for (var i = 0; i < lastRound.length; i += 2) {
            var winner;
            if (match in results) {
                if (results[match] == lastRound[i]) {
                    winner = lastRound[i];
                } else {
                    winner = lastRound[i+1];
                }
            } else {
                if (seeds[lastRound[i]] > seeds[lastRound[i+1]]) {
                    winner = lastRound[i+1];
                } else {
                    winner = lastRound[i];
                }
            }
            newRound.push(winner);
            match++;
        }
        rounds.push(newRound);
    }
    return rounds;
}