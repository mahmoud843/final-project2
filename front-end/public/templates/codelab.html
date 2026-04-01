<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Lab - معمل البرمجة | PAD</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/dracula.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/xml/xml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/css/css.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/htmlmixed/htmlmixed.min.js"></script>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

    <style>
        :root {
            --bg-main: #070b17;
            --bg-panel: #0f1933;
            --text-light: #eaf0ff;
            --text-muted: #8fa5de;
            --primary: #1b74e4;
            --success: #22c55e;
            --danger: #ef4444;
            --border: rgba(145,175,255,0.1);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-main);
            margin: 0;
            padding: 0;
            color: var(--text-light);
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        .top-bar {
            padding: 20px 30px 0 30px;
        }

        .back-btn {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            text-decoration: none;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid var(--border);
            transition: 0.3s;
        }

        .back-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            transform: translateX(-3px);
        }

        .header {
            background: rgba(15, 25, 51, 0.8);
            border-bottom: 1px solid var(--border);
            margin: 15px 30px 0 30px;
            padding: 0 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 70px;
            z-index: 1000;
            border-radius: 16px 16px 0 0;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 30px;
        }

        .header-title h1 {
            margin: 0;
            font-size: 20px;
            color: #fff;
        }

        .header-title p {
            margin: 0;
            font-size: 12px;
            color: var(--text-muted);
        }

        .lang-tabs {
            display: flex;
            gap: 10px;
            background: rgba(0,0,0,0.3);
            padding: 5px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }

        .lang-btn {
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .lang-btn:hover {
            color: #fff;
        }

        .lang-btn.active {
            background: var(--primary);
            color: #fff;
            box-shadow: 0 0 15px rgba(27, 116, 228, 0.4);
        }
        
        .main-container {
            display: flex;
            flex: 1;
            overflow: hidden;
            margin: 0 30px 30px 30px;
            border-radius: 0 0 16px 16px;
        }

        .sidebar {
            width: 300px;
            background: var(--bg-panel);
            border-left: 1px solid var(--border);
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .sidebar::-webkit-scrollbar {
            width: 4px;
        }

        .sidebar::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 10px;
        }

        .sidebar h3 {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #fff;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }

        .challenge-item {
            background: rgba(255, 255, 255, 0.03);
            padding: 12px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid transparent;
        }

        .challenge-item:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .challenge-item.active {
            background: rgba(27, 116, 228, 0.15);
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(27, 116, 228, 0.2);
        }

        .challenge-title {
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 5px;
            color: #fff;
        }

        .difficulty {
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 20px;
            color: #fff;
            font-weight: bold;
        }

        .diff-beginner { background: var(--success); }
        .diff-intermediate { background: #eab308; }

        .codelab-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
            background: transparent;
        }

        .codelab-content::-webkit-scrollbar {
            width: 6px;
        }

        .codelab-content::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        
        .challenge-info {
            background: var(--bg-panel);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid var(--border);
        }

        .challenge-info h2 {
            margin: 0 0 10px 0;
            color: #fff;
            font-size: 20px;
        }

        .challenge-info p {
            color: var(--text-muted);
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 0;
        }

        .sample-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            border: 1px dashed var(--border);
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }

        .sample-col {
            flex: 1;
        }

        .sample-col strong {
            color: #fff;
            font-size: 13px;
            display: block;
            margin-bottom: 8px;
        }

        .sample-box pre {
            margin: 0;
            font-family: monospace;
            font-size: 14px;
            color: var(--success);
            direction: ltr;
            text-align: left;
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 6px;
        }

        .editor-section {
            background: var(--bg-panel);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            flex: 1;
        }

        .editor-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .editor-header h3 {
            margin: 0;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
        }

        .ai-btn { 
            background: linear-gradient(135deg, #a855f7, #6366f1);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
            animation: pulse-glow 2s infinite;
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(168, 85, 247, 0); }
            100% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0); }
        }

        .ai-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
            filter: brightness(1.1);
            animation: none;
        }

        .run-button {
            background: var(--success);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .run-button:hover {
            background: #16a34a;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(34, 197, 94, 0.3);
        }

        .CodeMirror {
            height: 280px;
            border-radius: 10px;
            font-size: 15px;
            text-align: left;
            direction: ltr;
            border: 1px solid var(--border);
            padding: 10px 0;
        }
        
        .output-section {
            margin-top: 15px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }

        .output-box {
            background: #000;
            color: #fff;
            padding: 15px;
            border-radius: 10px;
            min-height: 120px;
            font-family: monospace;
            font-size: 14px;
            direction: ltr;
            text-align: left;
            border: 1px solid var(--border);
            overflow-y: auto;
        }
        
        .html-preview-frame {
            width: 100%;
            height: 180px;
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 10px;
            display: none;
            margin-top: 10px;
        }

        .ai-response {
            background: rgba(168, 85, 247, 0.1);
            border-left: 4px solid #a855f7;
            padding: 15px;
            border-radius: 0 8px 8px 0;
            margin-top: 10px;
            color: #eaf0ff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            direction: rtl;
            text-align: right;
        }

        .ai-response strong {
            color: #a855f7;
        }
        .ai-response strong {
  color: #a855f7;
}

/* 👇 حطي الكود هنا 👇 */

.levels {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.level {
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.level.beginner {
  background-color: #00c853 !important;
}

.level.intermediate {
  background-color: #e6b800 !important;
}

.level.advanced {
  background-color: #ff4d4d !important;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: white;
}
.levels {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.level {
    flex: 1;
    padding: 10px 8px;
    font-size: 14px;
    border-radius: 20px;
    text-align: center;
    justify-content: center;
}
.level.active.beginner {
    background-color: #22c55e !important;
}

.level.active.intermediate {
    background-color: #facc15 !important;
    color: black !important;
}

.level.active.advanced {
    background-color: #ef4444 !important;
}
    </style>
</head>
<body>

<div class="top-bar">
    <a href="{{ url_for('home_page') }}" class="back-btn">
        <i class="fa-solid fa-arrow-right"></i>
        العودة إلى الرئيسية
    </a>
</div>

<div class="header">
    <div class="header-left">
        <div class="header-title">
            <h1>🧪 PAD Code Lab</h1>
            <p>Interactive Coding Workspace</p>
        </div>
        <div class="lang-tabs">
            <button class="lang-btn active" onclick="switchLanguage('python')" id="tab-python"><i class="fa-brands fa-python"></i> Python</button>
            <button class="lang-btn" onclick="switchLanguage('web')" id="tab-web"><i class="fa-brands fa-html5"></i> HTML/CSS</button>
        </div>
    </div>
</div>

<div class="main-container">
    <div class="sidebar" id="sidebar">
       <div class="levels">

<button class="level beginner" onclick="showLevel('beginner')">
    <span class="dot"></span> Beginner
</button>

<button class="level intermediate" onclick="showLevel('intermediate')">
    <span class="dot"></span> Intermediate
</button>

<button class="level advanced" onclick="showLevel('advanced')">
    <span class="dot"></span> advanced
</button>

</div>

<h3 id="sidebar-title">📄 تحديات Python</h3>
<div id="challenges-list"></div>
    </div>

    <div class="codelab-content">
        <div class="challenge-info">
            <h2 id="current-title">جاري التحميل...</h2>
            <p id="current-desc"></p>
            <div class="sample-box">
                <div class="sample-col"><strong>📥 المدخلات أو الشروط:</strong><pre id="current-input">-</pre></div>
                <div class="sample-col"><strong>📤 المخرجات المتوقعة:</strong><pre id="current-output">-</pre></div>
            </div>
        </div>

        <div class="editor-section">
            <div class="editor-header">
                <h3 id="editor-title"><i class="fa-brands fa-python" style="color:#fbbf24;"></i> محرر بايثون</h3>
                <div class="action-buttons">
                    <button onclick="askAI()" class="ai-btn" title="اطلب المساعدة من الذكاء الاصطناعي">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> فحص بالذكاء الاصطناعي
                    </button>
                    <button onclick="checkCode()" class="run-button"><i class="fa-solid fa-play"></i> تشغيل الكود</button>
                </div>
            </div>
            
            <textarea id="code-editor"></textarea>
            
            <div class="output-section">
                <h3 style="margin: 0 0 5px 0; font-size: 14px; color: var(--text-muted);">📊 نافذة المخرجات (Console)</h3>
                <div class="output-box" id="output-box">
                    <span style="color: #666;">اضغط على "تشغيل الكود" أو "فحص بالذكاء الاصطناعي"...</span>
                </div>
                <iframe id="html-preview" class="html-preview-frame" sandbox="allow-scripts"></iframe>
            </div>
        </div>
    </div>
</div>
<script>
const allChallenges = {
  python: {{ challenges | tojson | safe }}
};
let currentLevel = "beginner";

function showLevel(level) {
  currentLevel = level;
  renderSidebar();
}

    let currentLanguage = 'python';
    let currentChallengeId = 1;
    let editor;

    window.onload = function() {
        editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
            mode: "python",
            theme: "dracula",
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true,
            specialChars: /[\u0000-\u001f\u007f-\u009f\u00ad\u061c\u200b-\u200f\u2028\u202e\ufeff\ufff9-\ufffc]/g
        });
        loadLanguageEnvironment('python');
    };

    function switchLanguage(lang) {
        currentLanguage = lang;
        document.getElementById('tab-python').classList.remove('active');
        document.getElementById('tab-web').classList.remove('active');
        document.getElementById(`tab-${lang}`).classList.add('active');
        loadLanguageEnvironment(lang);
    }

    function loadLanguageEnvironment(lang) {
        const challenges = allChallenges[lang];
        currentChallengeId = challenges[0].id;

        if (lang === 'python') {
            document.getElementById('sidebar-title').innerText = "📋 تحديات Python";
            document.getElementById('editor-title').innerHTML = '<i class="fa-brands fa-python" style="color:#fbbf24;"></i> محرر بايثون';
            editor.setOption("mode", "python");
            document.getElementById('html-preview').style.display = 'none';
        } else {
            document.getElementById('sidebar-title').innerText = "📋 تحديات HTML/CSS";
            document.getElementById('editor-title').innerHTML = '<i class="fa-brands fa-html5" style="color:#e34f26;"></i> محرر الويب';
            editor.setOption("mode", "htmlmixed");
            document.getElementById('html-preview').style.display = 'block';
        }

    
        loadChallenge(currentChallengeId);
    }

    function renderSidebar() {
        const listDiv = document.getElementById('challenges-list');
        listDiv.innerHTML = '';

       allChallenges[currentLanguage].forEach(challenge => {
console.log("LEVEL:", currentLevel);
    console.log("DATA:", challenge.difficulty);

            if (challenge.difficulty !== currentLevel) return;
            const diffClass = challenge.difficulty === 'beginner' ? 'diff-beginner' : 'diff-intermediate';
            listDiv.innerHTML += `
                <div class="challenge-item ${challenge.id === currentChallengeId ? 'active' : ''}" onclick="loadChallenge(${challenge.id})">
                    <div class="challenge-title">${challenge.title}</div>
                    <span class="difficulty ${diffClass}">${challenge.difficulty}</span>
                </div>
            `;
        });
    }

    function loadChallenge(id) {
        currentChallengeId = id;
        const challenge = allChallenges[currentLanguage].find(c => c.id === id);

        document.getElementById('current-title').innerText = challenge.title;
        document.getElementById('current-desc').innerText = challenge.description;
        document.getElementById('current-input').innerText = challenge.sample_input;
        document.getElementById('current-output').innerText = challenge.sample_output;

        const initialText = currentLanguage === 'python'
            ? "# Write your Python code here\n"
            : "<!-- Write your HTML/CSS code here -->\n";

        editor.setValue(initialText);
        editor.clearHistory();

        document.getElementById('output-box').innerHTML = '<span style="color: #666;">في انتظار الكود...</span>';
        if (currentLanguage === 'web') {
            document.getElementById('html-preview').srcdoc = "";
        }

        
    }

    function askAI() {
        const code = editor.getValue().trim();
        const outputBox = document.getElementById('output-box');

        if (code === "" || code.startsWith("#") || code.startsWith("<!--")) {
            outputBox.innerHTML = `<span style="color:#ef4444;">❌ عذراً، لا يوجد كود لفحصه. الرجاء كتابة الحل أولاً!</span>`;
            return;
        }

        outputBox.innerHTML = `<span style="color:#a855f7;"><i class="fa-solid fa-spinner fa-spin"></i> PAD AI يقوم بتحليل الكود الخاص بك...</span>`;

        setTimeout(() => {
            let aiFeedback = "";
            const codeLower = code.toLowerCase();

            if (currentLanguage === 'python') {
                if (!codeLower.includes("print")) {
                    aiFeedback = "أرى أنك نسيت استخدام دالة <code>print()</code>. في بايثون، لا يمكن عرض النتيجة على الشاشة بدون هذه الدالة.";
                } else if (!code.includes("PAD") && currentChallengeId === 1) {
                    aiFeedback = "لقد استخدمت دالة الطباعة بشكل صحيح، ولكن النص المكتوب داخلها لا يطابق المطلوب. تأكد من كتابة 'Hello, PAD!' بالضبط.";
                } else {
                    aiFeedback = "ممتاز جداً! 🎉 بناءية الكود (Syntax) تبدو صحيحة. اضغط على زر 'تشغيل الكود' لتتأكد من مطابقة النتيجة.";
                }
            } else {
                if (!code.includes("<") || !code.includes(">")) {
                    aiFeedback = "تذكر أن أكواد الـ HTML تُكتب دائماً داخل أقواس زاوية هكذا: <code>&lt;tag&gt;</code>. الكود الخاص بك يفتقر إلى هذه الأقواس.";
                } else {
                    aiFeedback = "الهيكل الأساسي للكود سليم! 👍 يمكنك تشغيله الآن لرؤية المعاينة الحية (Live Preview) في الأسفل.";
                }
            }

            outputBox.innerHTML = `
                <div class="ai-response">
                    <strong><i class="fa-solid fa-robot"></i> PAD AI:</strong><br>
                    ${aiFeedback}
                </div>
            `;
        }, 1200);
    }

    function checkCode() {
        const code = editor.getValue().trim();
        const outputBox = document.getElementById('output-box');
        const iframe = document.getElementById('html-preview');
        const challenge = allChallenges[currentLanguage].find(c => c.id === currentChallengeId);

        if (code === "" || code.startsWith("#") || code.startsWith("<!--")) return;

        outputBox.innerHTML = `<div style="color:#38bdf8;"><i class="fa-solid fa-terminal"></i> جاري التشغيل...</div>`;

setTimeout(() => {

    let resultHTML = `<div style="color:#38bdf8; font-family: monospace;">> python main.py</div><br>`;

    try {
        let output = "";

        const print = (text) => {
            output += text + "<br>";
        };

        eval(code);

        resultHTML += `<div style="color:#fff;">${output}</div>`;
    } catch (error) {
        resultHTML += `<div style="color:red;">${error}</div>`;
    }

    outputBox.innerHTML = resultHTML;

}, 500)
    }

</script>

</body>
</html>
