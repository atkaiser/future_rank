function updateRoundsOnClick(rounds, player, round) {
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

//Update the displayed rankings
function updateDisplayedRankings(rankings) {
    var rankingsList = [];
    for (var player in rankings) {
        rankingsList.push([player, rankings[player]]);
    }
    rankingsList.sort(function sort(a, b) {return b[1] - a[1]});
    var rankingsTable = $('#rankings');
    rankingsTable.empty();
    var tableHeader = $('<tr/>');
    $('<th/>').text('Rank').appendTo(tableHeader);
    $('<th/>').text('Name').appendTo(tableHeader);
    $('<th/>').text('Points').appendTo(tableHeader);
    tableHeader.appendTo(rankingsTable);
    for (var i = 0; i < rankingsList.length; i++) {
        var tableRow = $('<tr/>');
        $('<td/>')
            .text(i+1)
            .appendTo(tableRow);
        $('<td/>')
            .text(rankingsList[i][0])
            .addClass("player")
            .appendTo(tableRow);
        $('<td/>')
            .text(rankingsList[i][1])
            .appendTo(tableRow);
        tableRow.appendTo(rankingsTable);
    }
}

function updateDisplayedBracket(rounds, roundsToDisplay) {
    
    var startRound = (rounds.length-1) - roundsToDisplay;
    
    var matches = [];
    for (var i = 0; i < rounds[startRound].length; i += 2) {
        var match = [rounds[startRound][i], rounds[startRound][i+1]];
        matches.push(match);
    }
    
    var results = getResults(rounds, roundsToDisplay);

    var data = {
            teams : matches,
            results : [results]
        };
      
    $(function initBracket() {
        $('#bracket .main').bracket({
            skipConsolationRound: true,
            init: data})
        });
}

function getResults(rounds, roundsToDisplay) {
    var startValue = (rounds.length-1) - roundsToDisplay;
    var results = [];
    for(var i = startValue; i < rounds.length-1; i += 1) {
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