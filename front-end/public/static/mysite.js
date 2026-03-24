/* =========================
   1) AUTO HIDE ALERTS
========================= */
function initializeAlerts() {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.display = 'none';
        });
    }, 5000);
}

/* =========================
   2) DARK MODE
========================= */
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');

    const icon = document.querySelector('#clicked i');
    if (icon) {
        icon.className = document.body.classList.contains('dark-mode')
            ? 'fa-solid fa-moon'
            : 'fa-solid fa-sun';
    }

    localStorage.setItem(
        'darkMode',
        document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled'
    );
}

function loadDarkMode() {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        const icon = document.querySelector('#clicked i');
        if (icon) {
            icon.className = 'fa-solid fa-moon';
        }
    }
}

/* =========================
   3) TO DO LIST
========================= */
function addCloseButton(li) {
    const span = document.createElement('span');
    span.className = 'close';
    span.textContent = '\u00D7';
    span.onclick = function () {
        li.style.display = 'none';
    };
    li.appendChild(span);
}

function initializeTodoList() {
    const todoRoot = document.getElementById('myUL');
    if (!todoRoot) return;

    todoRoot.querySelectorAll('li').forEach(li => {
        if (!li.querySelector('.close')) {
            addCloseButton(li);
        }
    });

    todoRoot.addEventListener('click', function (ev) {
        if (ev.target.tagName === 'LI') {
            ev.target.classList.toggle('checked');
        }
    });
}

function newElement() {
    const input = document.getElementById('myInput');
    const ul = document.getElementById('myUL');

    if (!input || !ul) return;

    const inputValue = input.value.trim();
    if (inputValue === '') {
        alert('You must write something!');
        return;
    }

    const li = document.createElement('li');
    li.appendChild(document.createTextNode(inputValue));
    ul.appendChild(li);
    addCloseButton(li);
    input.value = '';
}

window.newElement = newElement;

/* =========================
   4) SNAKE GAME
========================= */
function initializeSnakeGame() {
    const board = document.getElementById('board-1');
    if (!board || board.dataset.initialized === 'true') return;
    board.dataset.initialized = 'true';

    const scoreBox = document.getElementById('scoreBox');
    const highScoreBox = document.getElementById('hiscoreBox');
    const snakeBoardSize = 18;
    const speed = 100;

    let score = 0;
    let highScore = Number(localStorage.getItem('snakeHighScore') || 0);
    let snake = [{ x: 9, y: 9 }];
    let food = { x: 5, y: 5 };
    let dx = 0;
    let dy = 0;
    let changingDirection = false;
    let gameEnded = false;

    function clearBoard() {
        board.innerHTML = '';
    }

    function drawFood() {
        const foodElement = document.createElement('div');
        foodElement.style.gridRowStart = food.y;
        foodElement.style.gridColumnStart = food.x;
        foodElement.classList.add('food');
        board.appendChild(foodElement);
    }

    function drawSnake() {
        snake.forEach((segment, index) => {
            const snakeElement = document.createElement('div');
            snakeElement.style.gridRowStart = segment.y;
            snakeElement.style.gridColumnStart = segment.x;
            snakeElement.classList.add('snake');
            if (index === 0) snakeElement.classList.add('snake-head');
            board.appendChild(snakeElement);
        });
    }

    function generateFood() {
        let nextFood;
        do {
            nextFood = {
                x: Math.floor(Math.random() * snakeBoardSize) + 1,
                y: Math.floor(Math.random() * snakeBoardSize) + 1
            };
        } while (snake.some(segment => segment.x === nextFood.x && segment.y === nextFood.y));
        food = nextFood;
    }

    function updateScoreUI() {
        if (scoreBox) scoreBox.textContent = 'Score: ' + score;
        if (highScoreBox) highScoreBox.textContent = 'HighScore: ' + highScore;
    }

    function moveSnake() {
        const head = {
            x: snake[0].x + dx,
            y: snake[0].y + dy
        };

        snake.unshift(head);
        const hasEatenFood = head.x === food.x && head.y === food.y;

        if (hasEatenFood) {
            score += 10;
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('snakeHighScore', String(highScore));
            }
            updateScoreUI();
            generateFood();
        } else {
            snake.pop();
        }
    }

    function hasGameEnded() {
        for (let i = 1; i < snake.length; i++) {
            if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) return true;
        }

        const hitLeftWall = snake[0].x < 1;
        const hitRightWall = snake[0].x > snakeBoardSize;
        const hitTopWall = snake[0].y < 1;
        const hitBottomWall = snake[0].y > snakeBoardSize;

        return hitLeftWall || hitRightWall || hitTopWall || hitBottomWall;
    }

    function showGameOver() {
        const overlay = document.createElement('div');
        overlay.className = 'snake-game-over';
        overlay.innerHTML = '<strong>Game Over</strong><span>Refresh the page to play again.</span>';
        board.appendChild(overlay);
    }

    function main() {
        if (gameEnded) return;

        setTimeout(() => {
            changingDirection = false;
            clearBoard();
            drawFood();
            moveSnake();

            if (hasGameEnded()) {
                gameEnded = true;
                clearBoard();
                drawFood();
                drawSnake();
                showGameOver();
                return;
            }

            drawSnake();
            main();
        }, speed);
    }

    function changeDirection(event) {
        if (changingDirection) return;

        const key = event.key;
        const goingUp = dy === -1;
        const goingDown = dy === 1;
        const goingRight = dx === 1;
        const goingLeft = dx === -1;

        if ((key === 'ArrowLeft' || key === 'Left') && !goingRight) {
            dx = -1;
            dy = 0;
            changingDirection = true;
        }

        if ((key === 'ArrowUp' || key === 'Up') && !goingDown) {
            dx = 0;
            dy = -1;
            changingDirection = true;
        }

        if ((key === 'ArrowRight' || key === 'Right') && !goingLeft) {
            dx = 1;
            dy = 0;
            changingDirection = true;
        }

        if ((key === 'ArrowDown' || key === 'Down') && !goingUp) {
            dx = 0;
            dy = 1;
            changingDirection = true;
        }
    }

    document.addEventListener('keydown', changeDirection);
    updateScoreUI();
    drawFood();
    drawSnake();
    main();
}

/* =========================
   5) ROCK PAPER SCISSORS
========================= */
function playAgainstComputer(playerChoice) {
    const choices = ['rock', 'paper', 'scissors'];
    const computerChoice = choices[Math.floor(Math.random() * 3)];
    const computerChoiceElement = document.getElementById('computer-choice');
    const resultElement = document.getElementById('rps-result') || document.getElementById('result');

    if (computerChoiceElement) {
        computerChoiceElement.innerText = `Computer chose: ${computerChoice}`;
    }

    if (!resultElement) return;

    if (playerChoice === computerChoice) {
        resultElement.innerText = "It's a tie!";
    } else if (
        (playerChoice === 'rock' && computerChoice === 'scissors') ||
        (playerChoice === 'paper' && computerChoice === 'rock') ||
        (playerChoice === 'scissors' && computerChoice === 'paper')
    ) {
        resultElement.innerText = 'You win!';
    } else {
        resultElement.innerText = 'Computer wins!';
    }
}

function playWithFriend(playerChoice, player) {
    const result2Element = document.getElementById('result2');

    if (player === 'player1') {
        const player1ChoiceElement = document.getElementById('player1-choice');
        if (player1ChoiceElement) {
            player1ChoiceElement.innerText = 'Player 1 has made his choice';
        }
        sessionStorage.setItem('player1Choice', playerChoice);
    } else if (player === 'player2') {
        const player2ChoiceElement = document.getElementById('player2-choice');
        if (player2ChoiceElement) {
            player2ChoiceElement.innerText = `Player 2 chose: ${playerChoice}`;
        }

        sessionStorage.setItem('player2Choice', playerChoice);
        const player1Choice = sessionStorage.getItem('player1Choice');
        const player2Choice = playerChoice;

        if (!result2Element || !player1Choice || !player2Choice) return;

        if (player1Choice === player2Choice) {
            result2Element.innerText = "It's a tie!";
        } else if (
            (player1Choice === 'rock' && player2Choice === 'scissors') ||
            (player1Choice === 'paper' && player2Choice === 'rock') ||
            (player1Choice === 'scissors' && player2Choice === 'paper')
        ) {
            result2Element.innerText = 'Player 1 wins!';
        } else {
            result2Element.innerText = 'Player 2 wins!';
        }
    }
}

window.playAgainstComputer = playAgainstComputer;
window.playWithFriend = playWithFriend;

/* =========================
   6) TIC TAC TOE (X/O)
========================= */
let currentPlayer = 'X';
let gameBoard = ['', '', '', '', '', '', '', '', ''];
const winningCombos = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

function getXOResultElement() {
    return document.getElementById('xo-result') || document.getElementById('result');
}

function checkWinner() {
    return winningCombos.some(combo => {
        if (
            gameBoard[combo[0]] &&
            gameBoard[combo[0]] === gameBoard[combo[1]] &&
            gameBoard[combo[1]] === gameBoard[combo[2]]
        ) {
            highlightWinnerCells(combo);
            return true;
        }
        return false;
    });
}

function highlightWinnerCells(combo) {
    combo.forEach(index => {
        const cell = document.querySelector(`[data-index="${index}"]`);
        if (cell) cell.style.backgroundColor = 'lightgreen';
    });
}

function handleMove(event) {
    const cell = event.target;
    const index = cell.dataset.index;
    const resultElement = getXOResultElement();

    if (gameBoard[index] === '' && !checkWinner()) {
        gameBoard[index] = currentPlayer;
        cell.innerText = currentPlayer;
        cell.classList.add(currentPlayer.toLowerCase());
        cell.style.pointerEvents = 'none';

        if (checkWinner()) {
            if (resultElement) resultElement.innerText = `Player ${currentPlayer} wins!`;
        } else if (gameBoard.every(value => value !== '')) {
            if (resultElement) resultElement.innerText = "It's a tie!";
        } else {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        }
    }
}

function handleRestartGame() {
    gameBoard = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';

    document.querySelectorAll('.cell').forEach(cell => {
        cell.innerText = '';
        cell.style.pointerEvents = 'auto';
        cell.style.backgroundColor = '#f0f0f0';
        cell.classList.remove('x', 'o');
    });

    const resultElement = getXOResultElement();
    if (resultElement) resultElement.innerText = '';
}

function initializeXOGame() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.removeEventListener('click', handleMove);
        cell.addEventListener('click', handleMove);
    });

    const restartButton = document.querySelector('.game--restart');
    if (restartButton) {
        restartButton.removeEventListener('click', handleRestartGame);
        restartButton.addEventListener('click', handleRestartGame);
    }
}

/* =========================
   7) FOLLOW BUTTONS
========================= */
function initializeFollowButtons() {
    document.querySelectorAll('.follow-btn').forEach(button => {
        if (button.dataset.bound === 'true') return;

        button.addEventListener('click', () => {
            const text = button.textContent.trim();
            if (text === 'Follow') {
                button.textContent = 'Followed';
                button.classList.add('followed');
            } else if (text === 'Followed') {
                button.textContent = 'Follow';
                button.classList.remove('followed');
            }
        });

        button.dataset.bound = 'true';
    });
}

/* =========================
   8) COMMUNITIES BAR
========================= */
function initializeCommunitiesBar() {
    const btn = document.getElementById('communitiesBtn');
    const bar = document.getElementById('languagesBar');
    const communitiesSection = document.getElementById('communitiesSection');

    if (!btn || !bar || !communitiesSection) return;
    if (bar.dataset.initialized === 'true') return;
    bar.dataset.initialized = 'true';

    btn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        bar.classList.toggle('show');
    });

    document.addEventListener('click', e => {
        if (!communitiesSection.contains(e.target)) {
            bar.classList.remove('show');
        }
    });

    communitiesSection.addEventListener('mouseenter', () => {
        bar.classList.add('show');
    });

    communitiesSection.addEventListener('mouseleave', () => {
        bar.classList.remove('show');
    });

    bar.addEventListener('click', e => {
        e.stopPropagation();
    });

    bar.querySelectorAll('li').forEach(item => {
        item.addEventListener('click', function () {
            const language = this.textContent.trim();
            alert(`You selected: ${language}`);
            bar.classList.remove('show');
        });
    });
}

/* =========================
   9) DELETE POST
========================= */
function initializeDeletePost() {
    if (document.body.dataset.deletePostBound === 'true') return;
    document.body.dataset.deletePostBound = 'true';

    document.addEventListener('click', async function (e) {
        const deleteButton = e.target.closest('.delete-btn');
        if (!deleteButton) return;

        const postId = deleteButton.getAttribute('data-post-id');
        if (!postId) return;

        if (confirm('هل أنت متأكد أنك تريد حذف هذا المنشور نهائيًا؟')) {
            try {
                const response = await fetch(`/api/delete_post/${postId}`, {
                    method: 'POST'
                });
                const result = await response.json();

                if (result.status === 'success') {
                    const postElement = deleteButton.closest('.post-main');
                    if (postElement) postElement.remove();
                } else {
                    alert('❌ خطأ: ' + (result.message || 'Unable to delete post'));
                }
            } catch (error) {
                console.error('Delete post error:', error);
                alert('❌ حدث خطأ في الاتصال بالخادم.');
            }
        }
    });
}

/* =========================
   10) PROFILE NAVIGATION
========================= */
function navigateToProfile() {
    window.location.href = '/profile';
}
window.navigateToProfile = navigateToProfile;

/* =========================
   11) SUGGESTIONS
========================= */
function loadSuggestions() {
    const container = document.getElementById('suggestions-container');
    if (!container) return;

    fetch('/api/suggestions')
        .then(response => response.json())
        .then(users => {
            if (!Array.isArray(users) || users.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#888;padding:10px;">No suggestions</p>';
                return;
            }

            container.innerHTML = '';
            users.forEach(user => {
                const userHtml = `
                    <div class="profile-follow profile-foolow-hovering" data-user-id="${user.id}">
                        <div class="profile-follow-left">
                            <div class="profile-follow-image">
                                <img src="/static/images/${user.profile_image}" alt="${user.username}" onerror="this.src='https://via.placeholder.com/40'">
                            </div>
                            <div class="profile-follow-content">
                                <p class="profile-id">${user.username}</p>
                                <p class="profile-name">suggested</p>
                            </div>
                        </div>
                        <span class="clickable follow-btn" onclick="followSuggestion(${user.id}, this)">Follow</span>
                    </div>
                `;
                container.innerHTML += userHtml;
            });
            initializeFollowButtons();
        })
        .catch(error => console.error('Error loading suggestions:', error));
}

function followSuggestion(userId, btn) {
    fetch('/api/follow/' + userId, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                btn.innerText = 'Following';
                btn.style.background = '#22c55e';
                btn.style.color = '#fff';
                setTimeout(loadSuggestions, 900);
            }
        })
        .catch(error => console.error('Follow suggestion error:', error));
}
window.followSuggestion = followSuggestion;

/* =========================
   12) LIKE POSTS
========================= */
function toggleLike(postId, element) {
    fetch('/api/like/' + postId, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.liked) element.classList.add('liked');
                else element.classList.remove('liked');

                const likesCount = document.getElementById('likes-' + postId);
                const likesText = document.getElementById('likes-text-' + postId);
                if (likesCount) likesCount.innerText = data.likes_count;
                if (likesText) likesText.innerText = data.likes_count + ' people';
            }
        })
        .catch(error => console.error('Like error:', error));
}
window.toggleLike = toggleLike;

/* =========================
   13) COMMENTS API
========================= */
function addComment(postId) {
    const input = document.getElementById('comment-' + postId);
    if (!input) return;

    const commentText = input.value.trim();
    if (!commentText) {
        alert('Please enter a comment');
        return;
    }

    fetch('/api/comment/' + postId, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment: commentText })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Error: ' + (data.error || 'Unknown error'));
                return;
            }

            const commentsList = document.getElementById('comments-' + postId);
            if (!commentsList) return;

            const noComments = commentsList.querySelector('.no-comments');
            if (noComments) noComments.remove();

            const newComment = document.createElement('div');
            newComment.className = 'comment-item';
            newComment.innerHTML = `
                <span>${data.comment.username}:</span> ${data.comment.text}
                <small style="color:#888;font-size:10px;"> just now</small>
            `;
            commentsList.appendChild(newComment);
            input.value = '';

            const countSpan = document.getElementById('comments-count-' + postId);
            if (countSpan) {
                countSpan.innerText = parseInt(countSpan.innerText || '0', 10) + 1;
            }

            const successMsg = document.getElementById('success-' + postId);
            if (successMsg) {
                successMsg.style.display = 'block';
                setTimeout(() => {
                    successMsg.style.display = 'none';
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Add comment error:', error);
            alert('Error adding comment');
        });
}

function loadMoreComments(btn) {
    const postId = btn.getAttribute('data-post-id');
    if (!postId) return;

    fetch('/api/comments/' + postId)
        .then(response => response.json())
        .then(comments => {
            const commentsList = document.getElementById('comments-' + postId);
            if (!commentsList) return;

            commentsList.innerHTML = '';
            comments.forEach(comment => {
                const commentDiv = document.createElement('div');
                commentDiv.className = 'comment-item';
                commentDiv.innerHTML = `
                    <span>${comment.username}:</span> ${comment.text}
                    <small style="color:#888;font-size:10px;"> ${comment.created_at.split(' ')[1]}</small>
                `;
                commentsList.appendChild(commentDiv);
            });

            btn.style.display = 'none';
        })
        .catch(error => console.error('Load comments error:', error));
}

function focusComment(postId) {
    const input = document.getElementById('comment-' + postId);
    if (input) input.focus();
}

window.addComment = addComment;
window.loadMoreComments = loadMoreComments;
window.focusComment = focusComment;

/* =========================
   14) PAGE INIT
========================= */
function initializePage() {
    initializeAlerts();
    loadDarkMode();

    const clickedBtn = document.getElementById('clicked');
    if (clickedBtn && clickedBtn.dataset.bound !== 'true') {
        clickedBtn.addEventListener('click', toggleDarkMode);
        clickedBtn.dataset.bound = 'true';
    }

    initializeTodoList();
    initializeSnakeGame();
    initializeXOGame();
    initializeFollowButtons();
    initializeCommunitiesBar();
    initializeDeletePost();
    loadSuggestions();
}

document.addEventListener('DOMContentLoaded', initializePage);
  // تشغيل محررات الأكواد
        window.onload = function() {
            // محرر HTML
            var htmlEditor = ace.edit("html-editor");
            htmlEditor.setTheme("ace/theme/monokai");
            htmlEditor.session.setMode("ace/mode/html");
            htmlEditor.setValue(`<!-- اكتب كود HTML هنا -->`, 1);
            htmlEditor.setOptions({
                fontSize: "14px",
                showPrintMargin: false,
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true
            });
            // محرر CSS
            var cssEditor = ace.edit("css-editor");
            cssEditor.setTheme("ace/theme/monokai");
            cssEditor.session.setMode("ace/mode/css");
            cssEditor.setValue(`/* اكتب كود CSS هنا */`, 1);
            cssEditor.setOptions({
                fontSize: "14px",
                showPrintMargin: false
            });
            // محرر JavaScript
            var jsEditor = ace.edit("js-editor");
            jsEditor.setTheme("ace/theme/monokai");
            jsEditor.session.setMode("ace/mode/javascript");
            jsEditor.setValue(`// اكتب كود JavaScript هنا`, 1);
            jsEditor.setOptions({
                fontSize: "14px",
                showPrintMargin: false
            });
        };
        // التبديل بين أنواع المنشورات
        function switchPostType(type) {
            // إخفاء كل النماذج
            document.querySelectorAll('.post-form').forEach(form => {
                form.classList.remove('active');
            });
            
            // إظهار النموذج المختار
            document.getElementById(type + 'Form').classList.add('active');
            
            // تحديث حالة الأزرار
            document.querySelectorAll('.type-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
        }
        // تشغيل المشروع
        function runProject() {
            var html = ace.edit("html-editor").getValue();
            var css = ace.edit("css-editor").getValue();
            var js = ace.edit("js-editor").getValue();
            var preview = document.getElementById('preview');
            
            var fullCode = `
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        * { margin: 0; padding: 0; box-sizing: border-box; }
                        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
                        ${css}
                    </style>
                </head>
                <body>
                    ${html}
                    <script>
                        ${js}
                    <\/script>
                </body>
                </html>
            `;
            preview.srcdoc = fullCode;
        }
        // نشر المنشور (مربوط بـ Flask API)
        async function publishPost() {
            const activeBtn = document.querySelector('.type-btn.active');
            if (!activeBtn) return;
            
            const activeType = activeBtn.classList.contains('question') ? 'question' : 
                               activeBtn.classList.contains('project') ? 'project' : 'code';
            
            let postData = {};
            
            if (activeType === 'question') {
                postData = {
                    type: 'question',
                    title: document.getElementById('questionTitle').value,
                    description: document.getElementById('questionDesc').value,
                    code: document.getElementById('questionCode').value,
                    language: document.getElementById('questionLanguage').value
                };
            } else {
                postData = {
                    type: activeType,
                    title: document.getElementById('questionTitle') ? document.getElementById('questionTitle').value : "New Project", // عشان لو مفيش title يبعت اسم افتراضي
                    description: "Project/Code from Code Lab",
                    html: ace.edit("html-editor").getValue(),
                    css: ace.edit("css-editor").getValue(),
                    js: ace.edit("js-editor").getValue()
                };
            }
            
            // تغيير نص الزرار عشان اليوزر يعرف إنه بيحمل
            const publishBtn = document.querySelector('.btn-primary[onclick="publishPost()"]');
            const originalBtnText = publishBtn.innerHTML;
            publishBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> جاري النشر...';
            publishBtn.disabled = true;

            try {
                // إرسال البيانات لسيرفر Flask
                const response = await fetch("{{ url_for('publish_post') }}", {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(postData)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert('✅ ' + result.message);
                    window.location.href = "{{ url_for('home_page') }}"; // التوجيه للصفحة الرئيسية
                } else {
                    alert('❌ خطأ: ' + result.message);
                    publishBtn.innerHTML = originalBtnText;
                    publishBtn.disabled = false;
                }
            } catch (error) {
                console.error('Error:', error);
                alert('❌ حدث خطأ في الاتصال بالخادم.');
                publishBtn.innerHTML = originalBtnText;
                publishBtn.disabled = false;
            }
        }
function publishPost() {
    const postTypeInput = document.getElementById('post_type_hidden');
    const titleInput = document.getElementById('title_hidden');
    const descriptionInput = document.getElementById('description_hidden');
    const codeInput = document.getElementById('code_content_hidden');
    const cssInput = document.getElementById('css_content_hidden');
    const jsInput = document.getElementById('js_content_hidden');
    const langInput = document.getElementById('programming_language_hidden');
    const form = document.getElementById('createProjectForm');

    if (!form || !postTypeInput) return;

    let activeType = 'question';
    const activeBtn = document.querySelector('.post-type-selector .type-btn.active');
    if (activeBtn) {
        if (activeBtn.classList.contains('project')) activeType = 'project';
        else if (activeBtn.classList.contains('code')) activeType = 'code';
        else activeType = 'question';
    }

    postTypeInput.value = activeType;

    if (activeType === 'question') {
        const title = (document.getElementById('questionTitle')?.value || '').trim();
        const description = (document.getElementById('questionDesc')?.value || '').trim();
        const code = (document.getElementById('questionCode')?.value || '').trim();
        const language = (document.getElementById('questionLanguage')?.value || '').trim();

        if (!title && !description && !code) {
            alert('اكتب عنوان أو وصف أو كود قبل النشر');
            return;
        }

        titleInput.value = title || 'سؤال جديد';
        descriptionInput.value = description;
        codeInput.value = code;
        cssInput.value = '';
        jsInput.value = '';
        langInput.value = language;
    } else {
        let htmlCode = '';
        let cssCode = '';
        let jsCode = '';

        try {
            if (window.htmlEditor) {
                htmlCode = window.htmlEditor.getValue().trim();
            } else if (document.getElementById('html-editor') && window.ace) {
                htmlCode = ace.edit('html-editor').getValue().trim();
            }
        } catch (e) {}

        try {
            if (window.cssEditor) {
                cssCode = window.cssEditor.getValue().trim();
            } else if (document.getElementById('css-editor') && window.ace) {
                cssCode = ace.edit('css-editor').getValue().trim();
            }
        } catch (e) {}

        try {
            if (window.jsEditor) {
                jsCode = window.jsEditor.getValue().trim();
            } else if (document.getElementById('js-editor') && window.ace) {
                jsCode = ace.edit('js-editor').getValue().trim();
            }
        } catch (e) {}

        if (!htmlCode && !cssCode && !jsCode) {
            alert('اكتب كود قبل النشر');
            return;
        }

        titleInput.value = activeType === 'code' ? 'كود جديد' : 'مشروع جديد';
        descriptionInput.value = activeType === 'code' ? 'تم إنشاء كود جديد' : 'تم إنشاء مشروع جديد';
        codeInput.value = htmlCode;
        cssInput.value = cssCode;
        jsInput.value = jsCode;
        langInput.value = 'html';
    }

    form.submit();
}