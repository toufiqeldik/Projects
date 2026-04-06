// When the game is over
function gameOver() {
    clearInterval(timerInterval); // Stop the timer
    gameOver = true;
    targets = []; // Remove targets
    document.getElementById('gameOverMessage').style.display = 'block'; // Show game over message
    document.getElementById('finalScore').textContent = score; // Show final score

    // Store the highest score in localStorage
    const previousHighScore = parseInt(localStorage.getItem('highestScore')) || 0;
    if (score > previousHighScore) {
        localStorage.setItem('highestScore', score); // Save new highest score
    }

    document.getElementById('buttonContainer').style.display = 'flex'; // Show retry and home buttons
}
