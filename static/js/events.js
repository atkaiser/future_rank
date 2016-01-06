// Methods related to click events


// Update based on someone clicking on the bracket
function respondToClick( event ) {
    var origTarget = event.target;
    var target = event.target;
    if (!isInArray("team", target.parentElement.classList)) {
        return;
    }
    var teamId = $(target.parentElement).attr("data-teamid");
    if (teamId == "-1") {
        return;
    }
    while ( target != null && 
            !isInArray("round", target.classList)) {
        target = target.parentElement;
    }
    if (target != null) {
        var round = Math.log2($(target).children().length) + 1;
        round = numRounds(rounds) - round;
    }
    
    var startRound = numRounds(rounds) - displayedRounds;
    
    var player = rounds[startRound][teamId];
    if (player != "Bye") {
        updateRoundsOnClick(rounds, player, round);
        
        updateDisplayedBracket(rounds, displayedRounds);
        
        var newRankings = calcRankings(rankings, rounds, points);
        updateDisplayedRankings(newRankings);
    }
}

// Based on rounds results calculate rankings
function calcRankings(rankings, rounds, points) {
    var newRankings = $.extend({}, rankings);
    for(var i = 0; i < rounds.length-1; i += 1) {
        var players = rounds[i];
        var winners = rounds[i+1];
        for(var j = 0; j < players.length; j += 2) {
            if (players[j] == winners[j/2]) {
                if (players[j+1] != "Bye") {
                    if (players[j+1] in newRankings) {
                        newRankings[players[j+1]] += points[i];
                    } else {
                        newRankings[players[j+1]] = points[i];
                    }
                }
            } else {
                if (players[j] != "Bye") {
                    if (players[j] in newRankings) {
                        newRankings[players[j]] += points[i];
                    } else {
                        newRankings[players[j]] = points[i];
                    }
                }
            }
        }
    }
    var winner = rounds[rounds.length-1][0];
    newRankings[winner] += points[points.length-1];
    return newRankings;
}

function hideRound() {
    if (displayedRounds > 0) {
        displayedRounds -= 1;
    }
    _updateButtons();
    updateDisplayedBracket(rounds, displayedRounds);
}

function showRound() {
    if (displayedRounds < 7) {
        displayedRounds += 1;
    }
    _updateButtons();
    updateDisplayedBracket(rounds, displayedRounds);
}

function _updateButtons() {
    if (displayedRounds >= numRounds(rounds)) {
        $("#showRound").prop("disabled", true)
    } else {
        $("#showRound").prop("disabled", false)
    }
    if (displayedRounds <= 1) {
        $("#hideRound").prop("disabled", true)
    } else {
        $("#hideRound").prop("disabled", false)
    }
}