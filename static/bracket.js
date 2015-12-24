function getResults(rounds) {
    var results = [];
    for(var i = 0; i < rounds.length-1; i += 1) {
        var resultRound = []
        var players = rounds[i];
        var winners = rounds[i+1];
        for(var j = 0; j < players.length; j += 2) {
            if (players[j] == winners[j/2]) {
                resultRound.push([1,0]);
            } else {
                resultRound.push([0,1]);
            }
        }
        results.push(resultRound);
    }
    return results;
}

function updateClick(rounds, player, round) {
    var match = Math.floor(rounds[round].indexOf(player) / 2);
    round += 1;
    var originalWinner = rounds[round][match];
    var nextWinner = rounds[round][match];
    while (originalWinner == nextWinner) {
        rounds[round][match] = player;
        round += 1;
        match = Math.floor(match / 2);
        if (round < rounds.length) {
            nextWinner = rounds[round][match]; 
        } else {
            nextWinner = "";
        }
    }
}

// Update the displayed rankings
function updateDisplayedRankings(rankings) {
    var rankingsList = [];
    for (var player in rankings) {
        rankingsList.push([player, rankings[player]]);
    }
    rankingsList.sort(function sort(a, b) {return b[1] - a[1]});
    var rankingsDiv = $('#rankings');
    rankingsDiv.empty();
    for (var i = 0; i < rankingsList.length; i++) {
        $('<div/>')
            .text(rankingsList[i][0])
            .addClass('ranking-player')
            .appendTo(rankingsDiv);
        $('<div/>')
            .text(rankingsList[i][1])
            .addClass('ranking-points')
            .appendTo(rankingsDiv);
    }
}

// Based on results
function calcRankings(rankings, rounds, points) {
    var newRankings = $.extend({}, rankings);
    for(var i = 0; i < rounds.length-1; i += 1) {
        var players = rounds[i];
        var winners = rounds[i+1];
        for(var j = 0; j < players.length; j += 2) {
            if (players[j] == winners[j/2]) {
                newRankings[players[j+1]] += points[i];
            } else {
                newRankings[players[j]] += points[i];
            }
        }
    }
    var winner = rounds[rounds.length-1][0];
    newRankings[winner] += points[points.length-1];
    return newRankings;
}

var numRounds = Math.log2(players.length / 2);

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

matches = [];
for (var i = 0; i < players.length; i += 2) {
    var match = [players[i], players[i+1]];
    matches.push(match);
}

var results = getResults(rounds);

var data = {
        teams : matches,
        results : [results]
    };
  
$(function() {
    $('#bracket .main').bracket({
        skipConsolationRound: true,
        init: data})
    });

var newRankings = calcRankings(rankings, rounds, points);
updateDisplayedRankings(newRankings);
    
$( "body" ).click(function( event ) {
    var origTarget = event.target;
    var target = event.target;
    if (!isInArray("team", target.parentElement.classList)) {
        console.log("Bad click");
        return;
    }
    var teamId = $(target.parentElement).attr("data-teamid");
    if (teamId == "-1") {
        console.log("Not on person");
        return;
    }
    while ( target != null && 
            !isInArray("round", target.classList)) {
        target = target.parentElement;
    }
    if (target != null) {
        var round = Math.log2($(target).children().length);
        round = numRounds - round;
    }
    
    var player = players[teamId];
    updateClick(rounds, player, round);
    
    var newResults = getResults(rounds); 
    var newData = {
            teams : matches,
            results : [newResults]
    };
    
    $('#bracket .main').bracket({
        skipConsolationRound: true,
        init: newData });
    
    var newRankings = calcRankings(rankings, rounds, points);
    updateDisplayedRankings(newRankings);
});