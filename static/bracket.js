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

var players = 
    [
        "Djoko",
        "Ferrer",
        "Kei",
        "Fed",
        "Tsonga",
        "Nadal",
        "Berdych",
        "Murray"
    ]

var seeds = {
        "Djoko": 1,
        "Fed": 2,
        "Kei": 3,
        "Murray": 4,
        "Tsonga": 5,
        "Nadal": 6,
        "Berdych": 7,
        "Ferrer": 8
}

var rankings = [
        ["Djoko", 1000],
        ["Fed", 920],
        ["Kei", 600],
        ["Murray", 700],
        ["Tsonga", 50],
        ["Nadal", 650],
        ["Berdych", 300],
        ["Ferrer", 10]
]

var points = [0, 100, 200];

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
    }
  
$(function() {
    $('#bracket .main').bracket({
        skipConsolationRound: true,
        init: data})
    })
    
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
    var match = Math.floor(rounds[round].indexOf(player) / 2);
    console.log(match);
    rounds[round+1][match] = player;
    
    var newResults = getResults(rounds); 
    
    var newData = {
            teams : matches,
            results : [newResults]
        }
    
    $('#bracket .main').bracket({
        skipConsolationRound: true,
        init: newData })
});