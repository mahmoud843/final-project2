from flask import Flask, request, redirect, url_for, session, render_template, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Post, Comment, Like, Todo, Challenge, ChallengeSubmission
import os

from models import db, User, Post, Comment, Like, Todo

# ==========================================
# إعداد المسارات
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, '..', 'front-end', 'public')

app = Flask(
    __name__,
    static_folder=os.path.join(PUBLIC_DIR, 'static'),
    template_folder=os.path.join(PUBLIC_DIR, 'templates')
)

# ==========================================
# الإعدادات الأساسية
# ==========================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://root@localhost/fp'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(PUBLIC_DIR, 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# إنشاء فولدر الصور لو مش موجود
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==========================================
# تهيئة قاعدة البيانات
# ==========================================
db.init_app(app)

# ==========================================
# تهيئة Login Manager
# ==========================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'
login_manager.login_message = 'Please login first'

# ==========================================
# السماح بامتدادات صور معينة فقط
# ==========================================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# User Loader
# ==========================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================
# Routes
# ==========================================
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    return render_template('index3.html')


@app.route('/home')
@login_required
def home_page():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('html.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return render_template('login.html', message="⚠️ Please fill all fields")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home_page'))
        else:
            return render_template('login.html', message="❌ Invalid email or password")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        programming_level = request.form.get('programming', '').strip()

        if not username or not email or not password:
            return render_template('signup.html', message="⚠️ Please fill all fields")

        if len(password) < 6:
            return render_template('signup.html', message="⚠️ Password must be at least 6 characters")

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            return render_template('signup.html', message="⚠️ Email or username already exists")

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            gender=gender,
            programming_level=programming_level
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login_page'))

    return render_template('signup.html')
@app.route('/api/leaderboard')
@login_required
def leaderboard():
    top_users = User.query.order_by(User.points.desc(), User.level.desc()).limit(10).all()

    return jsonify([
        {
            'id': u.id,
            'username': u.username,
            'points': u.points,
            'level': u.level,
            'profile_image': u.profile_image
        }
        for u in top_users
    ])
@app.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project_page():
    if request.method == 'POST':
        post_type = request.form.get('post_type', 'project').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        code_content = request.form.get('code_content', '').strip()
        css_content = request.form.get('css_content', '').strip()
        js_content = request.form.get('js_content', '').strip()
        programming_language = request.form.get('programming_language', '').strip()

        new_post = Post(
            user_id=current_user.id,
            post_type=post_type,
            title=title,
            description=description,
            code_content=code_content,
            css_content=css_content,
            js_content=js_content,
            programming_language=programming_language
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('create-project.html')

@app.route('/profile')
@login_required
def profile():
    projects = Post.query.filter_by(user_id=current_user.id, post_type='project').all()
    followers_count = current_user.followers.count()
    labs_count = ChallengeSubmission.query.filter_by(user_id=current_user.id, is_passed=True).count()

    leaderboard_users = User.query.order_by(User.points.desc(), User.level.desc()).limit(5).all()

    return render_template(
        'profile.html',
        user=current_user,
        projects=projects,
        followers_count=followers_count,
        labs_count=labs_count,
        is_following=False,
        leaderboard_users=leaderboard_users
    )

@app.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    projects = Post.query.filter_by(user_id=user_id, post_type='project').all()
    followers_count = user.followers.count()
    is_following = current_user.is_following(user)
    labs_count = Post.query.filter_by(user_id=user_id, post_type='lab').count()

    return render_template(
        'profile.html',
        user=user,
        projects=projects,
        followers_count=followers_count,
        labs_count=labs_count,
        is_following=is_following
    )


@app.route('/api/add-project', methods=['POST'])
@login_required
def add_project():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    new_project = Post(
        user_id=current_user.id,
        post_type='project',
        title=data.get('name', '').strip(),
        description=data.get('description', '').strip()
    )

    db.session.add(new_project)
    db.session.commit()

    return jsonify({
        'success': True,
        'project': {
            'id': new_project.id,
            'name': new_project.title,
            'description': new_project.description
        }
    })


@app.route('/api/delete-project/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    project = Post.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(project)
    db.session.commit()

    return jsonify({'success': True})


# ==========================================
# Followers APIs
# ==========================================
@app.route('/api/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot follow yourself'}), 400

    user_to_follow = User.query.get_or_404(user_id)

    if current_user.is_following(user_to_follow):
        current_user.unfollow(user_to_follow)
        followed = False
    else:
        current_user.follow(user_to_follow)
        followed = True

    db.session.commit()

    return jsonify({
        'success': True,
        'followed': followed,
        'followers_count': user_to_follow.followers.count()
    })


@app.route('/api/followers/<int:user_id>')
@login_required
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    followers_list = user.followers.all()

    return jsonify([{
        'id': f.id,
        'username': f.username,
        'profile_image': f.profile_image
    } for f in followers_list])


@app.route('/api/suggestions')
@login_required
def get_suggestions():
    users = User.query.filter(User.id != current_user.id).all()
    suggestions = [u for u in users if not current_user.is_following(u)][:5]

    return jsonify([{
        'id': u.id,
        'username': u.username,
        'profile_image': u.profile_image
    } for u in suggestions])


# ==========================================
# Likes & Comments APIs
# ==========================================
@app.route('/api/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    Post.query.get_or_404(post_id)

    like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if like:
        db.session.delete(like)
        liked = False
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        liked = True

    db.session.commit()

    likes_count = Like.query.filter_by(post_id=post_id).count()

    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    })


@app.route('/api/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    comment_text = data.get('comment', '').strip()

    if not comment_text:
        return jsonify({'error': 'Comment cannot be empty'}), 400

    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        comment_text=comment_text
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        'success': True,
        'comment': {
            'id': new_comment.id,
            'username': current_user.username,
            'text': comment_text,
            'created_at': new_comment.created_at.strftime('%Y-%m-%d %H:%M')
        }
    })


@app.route('/api/comments/<int:post_id>')
@login_required
def get_comments(post_id):
    Post.query.get_or_404(post_id)

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()

    return jsonify([{
        'id': c.id,
        'username': c.author.username,
        'text': c.comment_text,
        'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
    } for c in comments])


@app.route('/api/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['avatar']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = f"avatar_{current_user.id}_{secure_filename(file.filename)}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    current_user.profile_image = filename
    db.session.commit()

    return jsonify({'success': True, 'filename': filename})


@app.route('/api/update-bio', methods=['POST'])
@login_required
def update_bio():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    new_bio = data.get('bio', '').strip()
    current_user.bio = new_bio
    db.session.commit()

    return jsonify({'success': True, 'bio': new_bio})


# ==========================================
# صفحات إضافية
# ==========================================
@app.route('/ai')
@login_required
def ai_page():
    return render_template('Ai.html')


@app.route('/codelab')
@login_required
def codelab_page():
    return render_template('codelab.html')


@app.route('/shop')
@login_required
def shop_page():
    return render_template('shop.html')

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json()

    cart = data.get("cart", [])
    total = data.get("total", 0)

    if not cart:
        return jsonify({"status": "error", "message": "Cart is empty"})

    return jsonify({
        "status": "success",
        "message": f"Order completed successfully! Total paid: {total} EGP"
    })
@app.route('/hosting')
@login_required
def hosting_page():
    return render_template('hosting.html')


@app.route('/hosting/about')
@login_required
def about_page():
    return render_template('about.html')


@app.route('/hosting/status')
@login_required
def status_page():
    return render_template('status.html')


@app.route('/hosting/careers')
@login_required
def careers_page():
    return render_template('careers.html')


@app.route('/hosting/contact')
@login_required
def contact_page():
    return render_template('contact.html')


@app.route('/hosting/docs')
@login_required
def docs_page():
    return render_template('docs.html')


@app.route('/hosting/migration')
@login_required
def migration_page():
    return render_template('migration.html')


@app.route('/hosting/blog')
@login_required
def blog_page():
    return render_template('blog.html')


@app.route('/hosting/support')
@login_required
def support_page():
    return render_template('support.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login_page'))


# ==========================================
# تهيئة قاعدة البيانات
# ==========================================
def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_database()
    app.run(debug=True, port=5000)