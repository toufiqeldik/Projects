const gridSize = 10; // 10x10 grid
const numMines = 10; // Number of mines
let grid = [];
let mines = [];
let revealedCount = 0;
let flaggedCount = 0;
let timerInterval;
let timeElapsed = 0;

const gridElement = document.getElementById('grid');
const timerElement = document.getElementById('timer');
const minesLeftElement = document.getElementById('minesLeft');
const resetButton = document.getElementById('reset');
const backgroundVideo = document.getElementById('deathVideo');

// Ensure the video plays continuously
window.onload = () => {
    backgroundVideo.style.display = 'none'; // Keep video hidden in the UI
    backgroundVideo.loop = true; // Loop the video
    backgroundVideo.play(); // Start playing the video
    initializeGame();
};

// Initialize the game grid and start the game
function initializeGame() {
    grid = [];
    mines = [];
    revealedCount = 0;
    flaggedCount = 0;
    timeElapsed = 0;

    gridElement.innerHTML = '';
    minesLeftElement.textContent = numMines;

    // Create grid cells
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const cell = document.createElement('div');
            cell.setAttribute('data-row', i);
            cell.setAttribute('data-col', j);
            cell.classList.add('green'); // Default green square
            cell.addEventListener('click', () => revealCell(i, j));
            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                toggleFlag(i, j);
            });
            grid.push(cell);
            gridElement.appendChild(cell);
        }
    }

    // Place mines
    placeMines();
    startTimer();
}

// Place random mines on the grid
function placeMines() {
    let minesPlaced = 0;
    while (minesPlaced < numMines) {
        const row = Math.floor(Math.random() * gridSize);
        const col = Math.floor(Math.random() * gridSize);
        if (!mines.some(mine => mine.row === row && mine.col === col)) {
            mines.push({ row, col });
            minesPlaced++;
        }
    }
}

// Start the timer
function startTimer() {
    timerInterval = setInterval(() => {
        timeElapsed++;
        timerElement.textContent = timeElapsed;
    }, 1000);
}

// Reveal a cell
function revealCell(row, col) {
    const cell = grid.find(cell => cell.getAttribute('data-row') == row && cell.getAttribute('data-col') == col);

    // If already revealed or flagged, do nothing
    if (cell.classList.contains('revealed') || cell.classList.contains('flagged')) return;

    if (mines.some(mine => mine.row === row && mine.col === col)) {
        cell.classList.remove('green'); // Remove green state
        cell.classList.add('red'); // Add red state
        gameOver(); // Trigger game over
        return;
    }

    // Reveal the cell
    const mineCount = countAdjacentMines(row, col);
    cell.classList.add('revealed');
    cell.textContent = mineCount > 0 ? mineCount : '';
    revealedCount++;

    if (revealedCount === (gridSize * gridSize - numMines)) {
        alert('You Win!');
        resetGame();
    }

    // Reveal surrounding cells if no mines around
    if (mineCount === 0) {
        for (let i = row - 1; i <= row + 1; i++) {
            for (let j = col - 1; j <= col + 1; j++) {
                if (i >= 0 && i < gridSize && j >= 0 && j < gridSize && !(i === row && j === col)) {
                    revealCell(i, j);
                }
            }
        }
    }
}

// Count the number of mines surrounding a cell
function countAdjacentMines(row, col) {
    let mineCount = 0;
    for (let i = row - 1; i <= row + 1; i++) {
        for (let j = col - 1; j <= col + 1; j++) {
            if (i >= 0 && i < gridSize && j >= 0 && j < gridSize) {
                if (mines.some(mine => mine.row === i && mine.col === j)) {
                    mineCount++;
                }
            }
        }
    }
    return mineCount;
}

// Toggle flag on a cell
function toggleFlag(row, col) {
    const cell = grid.find(cell => cell.getAttribute('data-row') == row && cell.getAttribute('data-col') == col);
    if (cell.classList.contains('revealed')) return;

    if (cell.classList.contains('flagged')) {
        cell.classList.remove('flagged');
        flaggedCount--;
    } else {
        cell.classList.add('flagged');
        flaggedCount++;
    }

    minesLeftElement.textContent = numMines - flaggedCount;
}

// End the game
function gameOver() {
    clearInterval(timerInterval);

    alert('Game Over!');
    resetGame();
}

// Reset the game
function resetGame() {
    initializeGame();
}

// Add reset button functionality
resetButton.addEventListener('click', resetGame);
