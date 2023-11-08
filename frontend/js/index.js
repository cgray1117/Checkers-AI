//initializes the environment
const board = [null, 0, null, 1, null, 2, null, 3, 
            4, null, 5, null, 6, null, 7, null,
            null, 8, null, 9, null, 10, null, 11, 
            null, null, null, null, null, null, null, null, 
            null, null, null, null, null, null, null, null, 
            12, null, 13, null, 14, null, 15, null, 
            null, 16, null, 17, null, 18, null, 19, 
            20, null, 21, null, 22, null, 23, null]; 

const cells = document.querySelectorAll("td");
let whitePieces = document.querySelectorAll(".white-piece");
let redPieces = document.querySelectorAll(".red-piece");

let turn = true; // red goes first
let redScore = 12; // 1 point for each piece
let whiteScore = 12; // 1 point for each piece
let playerPieces; // represents each players available piece when it's their turn


//initializes the state and action space for the agent
let selectedPiece = { 
    pieceId: -1,
    boardIndex: -1,
    isKing: false,
    addSeventhPiece: false, // move white one space forward left or king red one space backwards left
    addNinthPiece: false, // move white one space forward right or king red one space backwards right
    addFourteenthPiece: false, // move white two space forward left or king red two space backwards left
    addEighteenthPiece: false, // move white two space forward right or king red two space backwards right
    minusSeventhPiece: false, // move red one space forward left or king white one space backwards left
    minusNinthPiece: false, // move red one space forward right or king white one space backwards right
    minusFourteenthPiece: false, // move red two space forward left or king white two space backwards left
    minusEighteenthPiece: false // move red two space forward right or king white two space backwards right
}

function resetSelectedPiece() {
    selectedPiece.pieceId = -1,
    selectedPiece.boardIndex = -1,
    selectedPiece.isKing = false,
    selectedPiece.addSeventhPiece = false, 
    selectedPiece.addNinthPiece = false, 
    selectedPiece.addFourteenthPiece = false, 
    selectedPiece.addEighteenthPiece = false, 
    selectedPiece.minusSeventhPiece = false, 
    selectedPiece.minusNinthPiece = false, 
    selectedPiece.minusFourteenthPiece = false, 
    selectedPiece.minusEighteenthPiece = false 
}

// waits for pieces to be click
function pieceEventListeners() {
    if(turn) { // if it's red turn
        for(let i=0; i < redPieces.length; i++) {
            redPieces[i].addEventListener("click", getPlayerPieces);
        }
    } else { // if it's white turn
        for(let i=0; i < whitePieces.length; i++) {
            whitePieces[i].addEventListener("click", getPlayerPieces);
        }
    } 
}

// get the properties of the selected piece
function getSelectedPiece(event) {
    let id = event.target.id
    selectedPiece.pieceId = parseInt(id)
    selectedPiece.boardIndex = function(id) {return board.indexOf(parseInt(id))}
    isPieceKing();
}

// gets all available pieces for player whose turn it is
function getPlayerPieces() {
    if (turn) {
        playerPieces = redPieces;
    } else {
        playerPieces = whitePieces;
    }
    removeCellonClick()
}

function resetBorders() {
    for (let i = 0; i < playerPieces.length; i++) {
        playerPieces[i].style.border = "1px solid white"
    }
    resetSelectedPiece();
    getSelectedPiece();
}

function removeCellonClick() {
    for (let i = 0; i < cells.length; i++) {
        cells[i].removeAttribute("onclick")
    }
}

function getAvailableSpaces() {
    if (board[selectedPiece.boardIndex + 7] === null &&
        cells[selectedPiece.boardIndex + 7].classList.contains('empty-cell') !== true) {
            selectedPiece.addSeventhPiece = true
        }
    if (board[selectedPiece.boardIndex + 9] === null &&
        cells[selectedPiece.boardIndex + 9].classList.contains('empty-cell') !== true) {
            selectedPiece.addNinthPiece = true
        }
    if (board[selectedPiece.boardIndex - 7] === null &&
            cells[selectedPiece.boardIndex - 7].classList.contains('empty-cell') !== true) {
                selectedPiece.minusSeventhPiece = true
        }
    if (board[selectedPiece.boardIndex - 9] === null &&
            cells[selectedPiece.boardIndex - 9].classList.contains('empty-cell') !== true) {
                selectedPiece.minusNinthPiece = true
        }
}

// highlights the cells of the selected piece and its legal moves
function hightlightCells(piece_id) {
    document.getElementById(piece_id).parentElement.style.border = '1px blue solid';
}

// checks to see if the game is over
function checkWin() {
    if (redScore === 0) {
        // WHITE WINS
    } else if (whiteScore === 0) {
        // RED WINS
    } else {
        // KEEP PLAYING
        changePlayer();
    }
}

// switches to next player if the game is not over
function changePlayer() {
    if (turn) {
        turn = false;
    } else {
        turn = true;
    }
    pieceEventListeners();
}

pieceEventListeners()
