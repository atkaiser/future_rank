/*
 * Functions that update what is displayed.
 */

/**
 * Takes in what round and player were clicked on and sets them as the winner
 * in that round, and any following rounds that the person they beat had won.
 * Doesn't return anything just updates the rounds variable.
 */
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

/**
 * Takes in the new rankings and updates the rankings table with those rankings
 * and updates the up down arrows in that table.
 */
function updateDisplayedRankings(rankings) {
    var rankingsList = [];
    for (var player in rankings) {
        rankingsList.push([player, rankings[player]]);
    }
    rankingsList.sort(function sort(a, b) {return b[1] - a[1];});
    var rankingsTable = $('#rankings');
    rankingsTable.empty();
    var tableHeader = $('<tr/>');
    $('<th/>').text('Rank').appendTo(tableHeader);
    $('<th/>').text('').appendTo(tableHeader);
    $('<th/>').text('Name').appendTo(tableHeader);
    $('<th/>').text('Points').appendTo(tableHeader);
    tableHeader.appendTo(rankingsTable);
    for (var i = 0; i < rankingsList.length; i++) {
        player = rankingsList[i][0];
        var tableRow = $('<tr/>');
        $('<td/>')
            .text(i+1)
            .appendTo(tableRow);
        var diff = oldRankings[player] - (i+1);
        if (diff > 0) {
            $('<td/>')
                .html("&#x25B2;" + diff)
                .addClass("up-arrow")
                .appendTo(tableRow);
        } else if (diff < 0) {
            $('<td/>')
                .html("&#x25BC;" + Math.abs(diff))
                .addClass("down-arrow")
                .appendTo(tableRow);
        } else {
            $('<td/>')
                .text('')
                .appendTo(tableRow);
        }
        $('<td/>')
            .text(player)
            .addClass("player")
            .appendTo(tableRow);
        $('<td/>')
            .text(rankingsList[i][1])
            .appendTo(tableRow);
        tableRow.appendTo(rankingsTable);
    }
}

/**
 * Takes in rounds and how many rounds to display and updates the displayed
 * bracket
 */
function updateDisplayedBracket(rounds, roundsToDisplay) {
    
    var startRound = (rounds.length-1) - roundsToDisplay;
    
    var matches = [];
    for (var i = 0; i < rounds[startRound].length; i += 2) {
        var match = [shortenName(rounds[startRound][i]), shortenName(rounds[startRound][i+1])];
        matches.push(match);
    }
    
    var results = generateResults(rounds, roundsToDisplay);

    var data = {
            teams : matches,
            results : [results]
        };
      
    $(function initBracket() {
        $('#bracket .main').bracket({
            skipConsolationRound: true,
            init: data});
        });
}

/**
 * Takes a name and returns the first letter of the first name and then the last name.
 * (If it is Bye, it will just return Bye)
 */
function shortenName(name) {
    if (name == "Bye") {
      return name;
    } else {
      var name_parts = name.split(" ");
      name_parts[0] = name_parts[0][0] + ".";
      return name_parts.join(" ");
    }
}

/**
 * Takes in rounds and how many rounds are going to be played and returns an
 * array of who won each match that can be fed into jQuerry Bracket
 */
function generateResults(rounds, roundsToDisplay) {
    var startValue = (rounds.length-1) - roundsToDisplay;
    var results = [];
    for(var i = startValue; i < rounds.length-1; i += 1) {
        var resultRound = [];
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