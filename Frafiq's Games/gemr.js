const canvas = document.getElementById("game-canvas");
const ctx = canvas.getContext("2d");

// Game settings
const canvasWidth = window.innerWidth;
const canvasHeight = window.innerHeight;
const snakeSize = 10; // The width and height of each snake segment
const segmentRadius = 5; // Radius for rounded corners
let snake1 = [{ x: 50, y: 50 }, { x: 40, y: 50 }, { x: 30, y: 50 }]; // 3 segments initially
let snake2 = [{ x: 300, y: 200 }, { x: 310, y: 200 }, { x: 320, y: 200 }]; // 3 segments initially
let direction1 = "RIGHT";
let direction2 = "LEFT";
let food = generateFood(220); // Start with 220 food items (red circles)
let score1 = 0;
let score2 = 0;
let isGameOver = false;
let isPaused = false;
let moveSpeed = 100; // Initial speed

// Set the canvas size to fill the window
canvas.width = canvasWidth;
canvas.height = canvasHeight;

// Listen to key events for Snake 1 (Arrow keys) and Snake 2 (WASD keys)
document.addEventListener("keydown", changeDirection);

// Main game loop
function gameLoop() {
    if (isGameOver) {
        setTimeout(() => {
            alert(`Game Over! Player ${score1 > score2 ? 1 : 2} wins!`);
            resetGame();
        }, 10);
    } else if (!isPaused) {
        setTimeout(() => {
            clearCanvas();
            drawScore();
            drawSnakes();
            moveSnakes();
            checkCollisions();
            drawFood();
            gameLoop();
        }, moveSpeed);
    }
}

// Clear the canvas
function clearCanvas() {
    ctx.fillStyle = "#2e2e2e"; // Dark gray background
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Draw the snakes
function drawSnakes() {
    drawSnake(snake1, "green");  // Player 1 snake color
    drawSnake(snake2, "lightblue");  // Player 2 snake color
}

// Draw a snake with rounded corners
function drawSnake(snake, color) {
    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = color;
        drawRoundedRect(snake[i].x, snake[i].y, snakeSize, snakeSize, segmentRadius);
    }
}

// Draw a rectangle with rounded corners
function drawRoundedRect(x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.arcTo(x + width, y, x + width, y + height, radius);
    ctx.arcTo(x + width, y + height, x, y + height, radius);
    ctx.arcTo(x, y + height, x, y, radius);
    ctx.arcTo(x, y, x + width, y, radius);
    ctx.closePath();
    ctx.fill();
}

// Draw the food (red circles)
function drawFood() {
    for (let i = 0; i < food.length; i++) {
        const ball = food[i];
        ctx.beginPath();
        ctx.fillStyle = ball.color; // Always red
        ctx.arc(ball.x + snakeSize / 2, ball.y + snakeSize / 2, snakeSize / 2, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Draw the score
function drawScore() {
    // Player 1's score in green
    ctx.fillStyle = "green";
    ctx.font = "20px Arial";
    ctx.fillText(`Player 1: ${score1}`, 10, 30);

    // Player 2's score in light blue
    ctx.fillStyle = "lightblue";
    ctx.font = "20px Arial";
    ctx.fillText(`Player 2: ${score2}`, canvas.width - 120, 30);
}

// Move the snakes
function moveSnakes() {
    moveSnake(snake1, direction1);
    moveSnake(snake2, direction2);
}

// Move the snake
function moveSnake(snake, direction) {
    const head = { ...snake[0] };

    if (direction === "LEFT") head.x -= snakeSize;
    if (direction === "RIGHT") head.x += snakeSize;
    if (direction === "UP") head.y -= snakeSize;
    if (direction === "DOWN") head.y += snakeSize;

    // Teleport when snake goes off screen
    if (head.x < 0) head.x = canvasWidth - snakeSize;
    if (head.x >= canvasWidth) head.x = 0;
    if (head.y < 0) head.y = canvasHeight - snakeSize;
    if (head.y >= canvasHeight) head.y = 0;

    // Check if Snake 1 collides with Snake 2
    for (let i = 0; i < snake2.length; i++) {
        if (head.x === snake2[i].x && head.y === snake2[i].y) {
            isGameOver = true; // Snake 1 collides with Snake 2
            return;
        }
    }

    snake.unshift(head); // Add the head to the front

    // Check if Snake 1 eats food
    for (let i = 0; i < food.length; i++) {
        if (head.x === food[i].x && head.y === food[i].y) {
            if (snake === snake1) score1++;
            else score2++;
            food.splice(i, 1); // Remove eaten food
            food = food.concat(generateFood(1)); // Add new food
            return;
        }
    }

    // If no food eaten, remove tail
    snake.pop();
}

// Change the direction of the snakes
function changeDirection(e) {
    if (e.key === "a" && direction2 !== "RIGHT") direction2 = "LEFT";
    if (e.key === "d" && direction2 !== "LEFT") direction2 = "RIGHT";
    if (e.key === "w" && direction2 !== "DOWN") direction2 = "UP";
    if (e.key === "s" && direction2 !== "UP") direction2 = "DOWN";

    if (e.key === "ArrowLeft" && direction1 !== "RIGHT") direction1 = "LEFT";
    if (e.key === "ArrowRight" && direction1 !== "LEFT") direction1 = "RIGHT";
    if (e.key === "ArrowUp" && direction1 !== "DOWN") direction1 = "UP";
    if (e.key === "ArrowDown" && direction1 !== "UP") direction1 = "DOWN";

    // Toggle pause with the "P" key
    if (e.key === "p" || e.key === "P") {
        isPaused = !isPaused;
    }
}

// Check for collisions (self, between the snakes, and with food)
function checkCollisions() {
    const head1 = snake1[0];
    const head2 = snake2[0];

    // Check if Snake 1 collides with itself
    for (let i = 1; i < snake1.length; i++) {
        if (head1.x === snake1[i].x && head1.y === snake1[i].y) isGameOver = true;
    }

    // Check if Snake 2 collides with itself
    for (let i = 1; i < snake2.length; i++) {
        if (head2.x === snake2[i].x && head2.y === snake2[i].y) isGameOver = true;
    }

    // Check for collision between Snake 1 and Snake 2
    for (let i = 0; i < snake2.length; i++) {
        if (head1.x === snake2[i].x && head1.y === snake2[i].y) isGameOver = true;
    }

    for (let i = 0; i < snake1.length; i++) {
        if (head2.x === snake1[i].x && head2.y === snake1[i].y) isGameOver = true;
    }

    // Check if Snake 1 collides with red food
    for (let i = 0; i < food.length; i++) {
        if (head1.x === food[i].x && head1.y === food[i].y) {
            isGameOver = true; // Collision with food
        }
    }

    // Check if Snake 2 collides with red food
    for (let i = 0; i < food.length; i++) {
        if (head2.x === food[i].x && head2.y === food[i].y) {
            isGameOver = true; // Collision with food
        }
    }
}

// Generate random food items (only red circles)
function generateFood(count) {
    let foodItems = [];
    for (let i = 0; i < count; i++) {
        const x = Math.floor(Math.random() * (canvasWidth / snakeSize)) * snakeSize;
        const y = Math.floor(Math.random() * (canvasHeight / snakeSize)) * snakeSize;
        foodItems.push({ x, y, type: "red", color: "red" }); // Always red food
    }
    return foodItems;
}

// Reset the game to initial state
function resetGame() {
    snake1 = [{ x: 50, y: 50 }, { x: 40, y: 50 }, { x: 30, y: 50 }];
    snake2 = [{ x: 300, y: 200 }, { x: 310, y: 200 }, { x: 320, y: 200 }];
    direction1 = "RIGHT";
    direction2 = "LEFT";
    score1 = 0;
    score2 = 0;
    isGameOver = false;
    food = generateFood(220);
    gameLoop(); // Start a new game
}

// Start the game
gameLoop();
