// Array to hold the leaderboard data
let leaderboard = [];

// Function to load the leaderboard from localStorage
function loadLeaderboard() {
    const savedLeaderboard = localStorage.getItem('leaderboard');
    
    // If data exists in localStorage, parse it and use it
    if (savedLeaderboard) {
        leaderboard = JSON.parse(savedLeaderboard);
    }

    // Display the leaderboard
    displayLeaderboard();
}

// Function to add a score to the leaderboard
function addScore() {
    // Get the values from the input fields
    const name = document.getElementById('name').value;
    const score = parseInt(document.getElementById('score').value);

    if (!name || isNaN(score)) {
        alert("Please enter both a name and a valid score.");
        return;
    }

    // Add the new score to the leaderboard array
    leaderboard.push({ name: name, score: score });

    // Sort the leaderboard by score in descending order
    leaderboard.sort((a, b) => b.score - a.score);

    // Clear the input fields after submission
    document.getElementById('name').value = '';
    document.getElementById('score').value = '';

    // Save the updated leaderboard to localStorage
    localStorage.setItem('leaderboard', JSON.stringify(leaderboard));

    // Update the displayed leaderboard
    displayLeaderboard();
}

// Function to display the leaderboard in the table
function displayLeaderboard() {
    const leaderboardTable = document.getElementById('leaderboard').getElementsByTagName('tbody')[0];
    
    // Clear the existing rows
    leaderboardTable.innerHTML = '';

    // Add the sorted leaderboard rows to the table
    leaderboard.forEach((entry, index) => {
        const row = leaderboardTable.insertRow();

        // Create the cells for rank, name, and score
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        const cell3 = row.insertCell(2);

        cell1.textContent = index + 1; // Rank (1, 2, 3...)
        cell2.textContent = entry.name;
        cell3.textContent = entry.score;
    });
}

// Load the leaderboard when the page loads
window.onload = loadLeaderboard;
