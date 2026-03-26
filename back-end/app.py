from flask import Flask, request, redirect, url_for, session, render_template, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Post, Comment, Like, Todo, Challenge, ChallengeSubmission
from datetime import datetime
import os

# ==========================================
# إعداد المسارات
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# خليه مرن لو front-end جوه نفس المجلد أو بره
PUBLIC_CANDIDATES = [
    os.path.join(BASE_DIR, 'front-end', 'public'),
    os.path.join(BASE_DIR, '..', 'front-end', 'public'),
]
PUBLIC_DIR = next((p for p in PUBLIC_CANDIDATES if os.path.isdir(p)), PUBLIC_CANDIDATES[0])

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
# بيانات المتجر
# ==========================================
SHOP_PRODUCTS = [
    {
        "id": 1,
        "name": "HTML5 Visual Guide",
        "category": "frontend",
        "price": 80,
        "desc": "Learn the structure of the web. Perfect for absolute beginners.",
        "icon": "fa-html5",
        "color": "#e34f26",
        "stock": 25
    },
    {
        "id": 2,
        "name": "CSS3 Mastery Book",
        "category": "frontend",
        "price": 120,
        "desc": "Master styling, Flexbox, and Grid to build beautiful responsive websites.",
        "icon": "fa-css3-alt",
        "color": "#1572b6",
        "stock": 20
    },
    {
        "id": 3,
        "name": "JavaScript Deep Dive",
        "category": "frontend",
        "price": 150,
        "desc": "Understand JS mechanics, DOM manipulation, and ES6+ features.",
        "icon": "fa-js",
        "color": "#f7df1e",
        "stock": 18
    },
    {
        "id": 4,
        "name": "Python for Backend",
        "category": "backend",
        "price": 200,
        "desc": "Learn Python programming, logic, and how to build strong backend systems.",
        "icon": "fa-python",
        "color": "#3776ab",
        "stock": 15
    }
]


# ==========================================
# Helpers
# ==========================================
def get_product_by_id(product_id):
    for product in SHOP_PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_cart():
    cart = session.get('cart', [])
    return cart if isinstance(cart, list) else []


def save_cart(cart):
    session['cart'] = cart
    session.modified = True


def clear_cart():
    session['cart'] = []
    session.modified = True


def get_user_orders():
    orders = session.get('orders_history', [])
    return orders if isinstance(orders, list) else []


def save_user_orders(orders):
    session['orders_history'] = orders
    session.modified = True


def calculate_cart_totals(cart):
    total = 0
    count = 0

    for item in cart:
        qty = int(item.get('qty', 0))
        price = float(item.get('price', 0))
        total += qty * price
        count += qty

    return {
        "items_count": count,
        "total_price": round(total, 2)
    }


def award_points(user, points):
    if not user:
        return
    user.points = int(user.points or 0) + int(points)
    user.update_level()


def normalize_order_for_profile(order):
    items = order.get('items')
    if not items:
        items = order.get('cart', [])
    return {
        "order_id": order.get("order_id"),
        "created_at": order.get("created_at"),
        "total": order.get("total", 0),
        "items": items
    }


def get_shop_stats():
    cart = get_cart()
    orders = get_user_orders()

    total_spent = sum(float(order.get('total', 0)) for order in orders)
    total_orders = len(orders)
    total_items_bought = sum(
        sum(int(item.get('qty', 0)) for item in order.get('items', order.get('cart', [])))
        for order in orders
    )
    last_order = orders[-1] if orders else None

    return {
        "cart": cart,
        "cart_summary": calculate_cart_totals(cart),
        "shop_orders": [normalize_order_for_profile(order) for order in reversed(orders)],
        "orders_count": total_orders,
        "total_spent": round(total_spent, 2),
        "total_items_bought": total_items_bought,
        "last_order": last_order
    }


def build_profile_context(user):
    projects = Post.query.filter_by(user_id=user.id, post_type='project').order_by(Post.created_at.desc()).all()
    followers_count = user.followers.count()

    try:
        labs_count = ChallengeSubmission.query.filter_by(user_id=user.id, is_passed=True).count()
    except Exception:
        labs_count = Post.query.filter_by(user_id=user.id, post_type='lab').count()

    leaderboard_users = User.query.order_by(User.points.desc(), User.level.desc()).limit(5).all()

    context = {
        "user": user,
        "projects": projects,
        "followers_count": followers_count,
        "labs_count": labs_count,
        "leaderboard_users": leaderboard_users,
        "is_following": current_user.is_authenticated and current_user.id != user.id and current_user.is_following(user),
        "todos": [],
        "orders_count": 0,
        "total_spent": 0,
        "shop_orders": []
    }

    if current_user.is_authenticated and current_user.id == user.id:
        context["todos"] = Todo.query.filter_by(user_id=user.id).order_by(
            Todo.is_completed.asc(),
            Todo.created_at.desc()
        ).all()
        context.update(get_shop_stats())

    return context


# ==========================================
# User Loader
# ==========================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================================
# Context Processor
# ==========================================
@app.context_processor
def inject_global_cart_data():
    cart_summary = calculate_cart_totals(get_cart())
    return {
        "global_cart_count": cart_summary["items_count"],
        "global_cart_total": cart_summary["total_price"]
    }


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


@app.route('/book-details/<int:id>')
@login_required
def book_details(id):
    product = get_product_by_id(id)

    if not product:
        return "Book not found", 404

    return render_template('book-details.html', product=product)


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
            session.setdefault('cart', [])
            session.setdefault('orders_history', [])
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home_page'))

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


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login_page'))


@app.route('/checkout')
@login_required
def checkout_page():
    return render_template('checkout.html')


@app.route('/success')
@login_required
def success_page():
    return render_template('success.html')


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
        award_points(current_user, 10)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('create-project.html')


@app.route('/profile')
@login_required
def profile():
    context = build_profile_context(current_user)
    return render_template('profile.html', **context)


@app.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    context = build_profile_context(user)
    return render_template('profile.html', **context)


@app.route('/api/profile/summary')
@login_required
def profile_summary():
    context = build_profile_context(current_user)
    return jsonify({
        "success": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "profile_image": current_user.profile_image,
            "bio": current_user.bio,
            "points": current_user.points,
            "level": current_user.level
        },
        "stats": {
            "projects_count": len(context["projects"]),
            "followers_count": context["followers_count"],
            "labs_count": context["labs_count"],
            "orders_count": context["orders_count"],
            "total_spent": context["total_spent"],
            "todos_count": len(context["todos"])
        }
    })


@app.route('/api/add-project', methods=['POST'])
@login_required
def add_project():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    title = data.get('name', '').strip()
    description = data.get('description', '').strip()

    if not title:
        return jsonify({'error': 'Project name is required'}), 400

    new_project = Post(
        user_id=current_user.id,
        post_type='project',
        title=title,
        description=description
    )

    db.session.add(new_project)
    award_points(current_user, 10)
    db.session.commit()

    return jsonify({
        'success': True,
        'project': {
            'id': new_project.id,
            'name': new_project.title,
            'description': new_project.description
        },
        'user_points': current_user.points,
        'user_level': current_user.level
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
        award_points(user_to_follow, 2)
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
    post = Post.query.get_or_404(post_id)

    like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if like:
        db.session.delete(like)
        liked = False
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        liked = True

        if post.author and post.author.id != current_user.id:
            award_points(post.author, 1)

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
    post = Post.query.get_or_404(post_id)
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

    if post.author and post.author.id != current_user.id:
        award_points(post.author, 2)

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


# ==========================================
# Avatar & Bio APIs
# ==========================================
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
# Todos APIs
# ==========================================
@app.route('/api/todos', methods=['GET', 'POST'])
@login_required
def todos_api():
    if request.method == 'GET':
        todos = Todo.query.filter_by(user_id=current_user.id).order_by(
            Todo.is_completed.asc(),
            Todo.created_at.desc()
        ).all()
        return jsonify({
            "success": True,
            "todos": [
                {
                    "id": todo.id,
                    "task_text": todo.task_text,
                    "is_completed": todo.is_completed,
                    "created_at": todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for todo in todos
            ]
        })

    data = request.get_json() or {}
    task_text = data.get('task_text', '').strip()

    if not task_text:
        return jsonify({'error': 'Task text is required'}), 400

    todo = Todo(user_id=current_user.id, task_text=task_text)
    db.session.add(todo)
    award_points(current_user, 1)
    db.session.commit()

    return jsonify({
        "success": True,
        "todo": {
            "id": todo.id,
            "task_text": todo.task_text,
            "is_completed": todo.is_completed,
            "created_at": todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
        },
        "user_points": current_user.points,
        "user_level": current_user.level
    })


@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    todo.is_completed = not todo.is_completed
    if todo.is_completed:
        award_points(current_user, 2)

    db.session.commit()

    return jsonify({
        "success": True,
        "id": todo.id,
        "is_completed": todo.is_completed
    })


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"success": True})


# ==========================================
# Shop APIs
# ==========================================
@app.route('/api/shop/products')
@login_required
def shop_products():
    category = request.args.get('category', '').strip().lower()
    search = request.args.get('search', '').strip().lower()

    products = SHOP_PRODUCTS

    if category and category != 'all':
        products = [p for p in products if p['category'] == category]

    if search:
        products = [
            p for p in products
            if search in p['name'].lower() or search in p['desc'].lower()
        ]

    return jsonify({
        "success": True,
        "products": products
    })


@app.route('/api/shop/cart', methods=['GET'])
@login_required
def shop_cart():
    cart = get_cart()
    summary = calculate_cart_totals(cart)

    return jsonify({
        "success": True,
        "cart": cart,
        "items_count": summary["items_count"],
        "total_price": summary["total_price"]
    })


@app.route('/api/shop/cart/add', methods=['POST'])
@login_required
def add_to_cart_api():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))

    if not product_id:
        return jsonify({"success": False, "message": "product_id is required"}), 400

    product = get_product_by_id(int(product_id))
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    if qty <= 0:
        qty = 1

    cart = get_cart()
    existing = next((item for item in cart if item["id"] == product["id"]), None)

    if existing:
        existing["qty"] += qty
    else:
        cart.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "category": product["category"],
            "qty": qty,
            "icon": product.get("icon"),
            "desc": product.get("desc")
        })

    save_cart(cart)
    summary = calculate_cart_totals(cart)

    return jsonify({
        "success": True,
        "message": f"{product['name']} added to cart",
        "cart": cart,
        "items_count": summary["items_count"],
        "total_price": summary["total_price"]
    })


@app.route('/api/shop/cart/update', methods=['POST'])
@login_required
def update_cart_item_api():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))

    if not product_id:
        return jsonify({"success": False, "message": "product_id is required"}), 400

    cart = get_cart()
    item = next((item for item in cart if item["id"] == int(product_id)), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found in cart"}), 404

    if qty <= 0:
        cart = [i for i in cart if i["id"] != int(product_id)]
    else:
        item["qty"] = qty

    save_cart(cart)
    summary = calculate_cart_totals(cart)

    return jsonify({
        "success": True,
        "message": "Cart updated successfully",
        "cart": cart,
        "items_count": summary["items_count"],
        "total_price": summary["total_price"]
    })


@app.route('/api/shop/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_cart_item_api(product_id):
    cart = get_cart()
    cart = [item for item in cart if item["id"] != product_id]
    save_cart(cart)
    summary = calculate_cart_totals(cart)

    return jsonify({
        "success": True,
        "message": "Item removed from cart",
        "cart": cart,
        "items_count": summary["items_count"],
        "total_price": summary["total_price"]
    })


@app.route('/api/shop/cart/clear', methods=['POST'])
@login_required
def clear_cart_api():
    clear_cart()
    return jsonify({
        "success": True,
        "message": "Cart cleared successfully"
    })


@app.route('/api/shop/orders')
@login_required
def shop_orders_api():
    orders = get_user_orders()
    return jsonify({
        "success": True,
        "orders_count": len(orders),
        "orders": [normalize_order_for_profile(order) for order in reversed(orders)]
    })


# ==========================================
# Challenges APIs
# ==========================================

def get_challenge_points(difficulty):
    """إرجاع نقاط التحدي حسب الصعوبة"""
    points_map = {
        'beginner': 10,
        'intermediate': 25,
        'advanced': 50
    }
    return points_map.get(difficulty, 10)


def award_challenge_points(user, difficulty):
    """منح نقاط للمستخدم عند حل التحدي"""
    points = get_challenge_points(difficulty)
    user.points = int(user.points or 0) + points
    user.update_level()
    db.session.commit()
    return points


def verify_python_solution(user_code, expected_output):
    """التحقق من حل Python"""
    try:
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            exec(user_code)
            output = captured_output.getvalue().strip()
            return output == expected_output.strip()
        except Exception:
            return False
        finally:
            sys.stdout = old_stdout
    except Exception:
        return False


def verify_html_solution(user_code, expected_output):
    """التحقق من حل HTML/CSS"""
    code_lower = user_code.lower()
    expected_lower = expected_output.lower()
    return expected_lower in code_lower


@app.route('/api/challenges')
@login_required
def get_challenges():
    """جلب قائمة التحديات"""
    language = request.args.get('language', 'python')
    challenges = Challenge.query.filter_by(language=language).all()
    
    solved_challenge_ids = set()
    submissions = ChallengeSubmission.query.filter_by(
        user_id=current_user.id,
        is_passed=True
    ).all()
    
    for sub in submissions:
        solved_challenge_ids.add(sub.challenge_id)
    
    return jsonify({
        'success': True,
        'challenges': [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'difficulty': c.difficulty,
            'points': get_challenge_points(c.difficulty),
            'sample_input': c.sample_input,
            'sample_output': c.sample_output,
            'starter_code': c.starter_code,
            'solved': c.id in solved_challenge_ids
        } for c in challenges]
    })


@app.route('/api/challenges/<int:challenge_id>/starter')
@login_required
def get_starter_code(challenge_id):
    """جلب starter code للتحدي"""
    challenge = Challenge.query.get_or_404(challenge_id)
    return jsonify({
        'success': True,
        'starter_code': challenge.starter_code or ''
    })


@app.route('/api/challenges/<int:challenge_id>/submit', methods=['POST'])
@login_required
def submit_challenge(challenge_id):
    """حل التحدي والتحقق من صحة الكود"""
    data = request.get_json()
    user_code = data.get('code', '').strip()
    
    if not user_code:
        return jsonify({'success': False, 'error': 'No code provided'}), 400
    
    challenge = Challenge.query.get_or_404(challenge_id)
    
    existing_submission = ChallengeSubmission.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id,
        is_passed=True
    ).first()
    
    if existing_submission:
        return jsonify({
            'success': False, 
            'error': 'You have already completed this challenge!',
            'already_completed': True
        }), 400
    
    is_correct = False
    if challenge.language == 'python':
        is_correct = verify_python_solution(user_code, challenge.sample_output)
    elif challenge.language == 'web':
        is_correct = verify_html_solution(user_code, challenge.sample_output)
    
    submission = ChallengeSubmission(
        user_id=current_user.id,
        challenge_id=challenge_id,
        code=user_code,
        is_passed=is_correct
    )
    db.session.add(submission)
    
    if is_correct:
        points_earned = award_challenge_points(current_user, challenge.difficulty)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_correct': True,
            'message': f'✅ Correct! You earned {points_earned} points!',
            'points_earned': points_earned,
            'user_points': current_user.points,
            'user_level': current_user.level
        })
    else:
        db.session.commit()
        return jsonify({
            'success': True,
            'is_correct': False,
            'message': '❌ Your solution is incorrect. Try again!',
            'expected_output': challenge.sample_output
        })


@app.route('/api/user/stats')
@login_required
def get_user_stats():
    """جلب إحصائيات المستخدم للتحديث الديناميكي"""
    solved_labs = ChallengeSubmission.query.filter_by(
        user_id=current_user.id,
        is_passed=True
    ).count()
    
    return jsonify({
        'success': True,
        'labs_solved': solved_labs,
        'points': current_user.points,
        'level': current_user.level
    })


def seed_challenges():
    """إضافة تحديات أولية لقاعدة البيانات"""
    with app.app_context():
        if Challenge.query.count() == 0:
            challenges = [
                # Python - Beginner
                Challenge(
                    title="طباعة نص بسيط",
                    description="استخدم أمر الطباعة في بايثون لطباعة 'Hello, PAD!'",
                    language="python",
                    difficulty="beginner",
                    sample_input="لا يوجد",
                    sample_output="Hello, PAD!",
                    starter_code="# اكتب الكود هنا\nprint('Hello, PAD!')",
                    points=10
                ),
                Challenge(
                    title="حاصل الجمع",
                    description="اكتب برنامج يطبع ناتج جمع 5 و 3",
                    language="python",
                    difficulty="beginner",
                    sample_input="5 + 3",
                    sample_output="8",
                    starter_code="# اكتب الكود هنا\n# احسب 5 + 3 واطبع الناتج\n",
                    points=10
                ),
                Challenge(
                    title="التحقق من العدد الزوجي",
                    description="اكتب كود يطبع 'Even' لو العدد زوجي، و 'Odd' لو فردي",
                    language="python",
                    difficulty="beginner",
                    sample_input="num = 4",
                    sample_output="Even",
                    starter_code="# اكتب الكود هنا\nnum = 4\n\n# اكتب الشرط هنا\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
                    points=10
                ),
                Challenge(
                    title="حلقة for",
                    description="اطبع الأرقام من 1 إلى 5 باستخدام حلقة for",
                    language="python",
                    difficulty="intermediate",
                    sample_input="لا يوجد",
                    sample_output="1\n2\n3\n4\n5",
                    starter_code="# اكتب الكود هنا\nfor i in range(1, 6):\n    print(i)",
                    points=25
                ),
                Challenge(
                    title="دالة الجمع",
                    description="اكتب دالة sum_numbers(a, b) ترجع ناتج جمع رقمين",
                    language="python",
                    difficulty="intermediate",
                    sample_input="sum_numbers(3, 7)",
                    sample_output="10",
                    starter_code="# اكتب الكود هنا\ndef sum_numbers(a, b):\n    return a + b\n\n# اختبر الدالة\nprint(sum_numbers(3, 7))",
                    points=25
                ),
                # Web - Beginner
                Challenge(
                    title="عنوان رئيسي HTML",
                    description="قم بإنشاء عنوان من النوع الأول H1 واكتب بداخله 'PAD Platform'",
                    language="web",
                    difficulty="beginner",
                    sample_input="استخدم تاج <h1>",
                    sample_output="<h1>PAD Platform</h1>",
                    starter_code="<!-- اكتب كود HTML هنا -->\n<h1>PAD Platform</h1>",
                    points=10
                ),
                Challenge(
                    title="زر تفاعلي",
                    description="قم بإنشاء زر <button> واكتب عليه 'Click Me'",
                    language="web",
                    difficulty="beginner",
                    sample_input="تاج <button>",
                    sample_output="<button>Click Me</button>",
                    starter_code="<!-- اكتب كود HTML هنا -->\n<button>Click Me</button>",
                    points=10
                ),
                Challenge(
                    title="فقرة نصية",
                    description="قم بإنشاء فقرة <p> تحتوي على 'Welcome to PAD'",
                    language="web",
                    difficulty="beginner",
                    sample_input="تاج <p>",
                    sample_output="<p>Welcome to PAD</p>",
                    starter_code="<!-- اكتب كود HTML هنا -->\n<p>Welcome to PAD</p>",
                    points=10
                ),
                Challenge(
                    title="تنسيق CSS أساسي",
                    description="غير لون النص في الفقرة إلى اللون الأزرق",
                    language="web",
                    difficulty="intermediate",
                    sample_input="style color: blue",
                    sample_output="<p style='color: blue;'>نص أزرق</p>",
                    starter_code="<!-- اكتب كود HTML/CSS هنا -->\n<p style='color: blue;'>نص أزرق</p>",
                    points=25
                )
            ]
            
            for challenge in challenges:
                db.session.add(challenge)
            
            db.session.commit()
            print(f"✅ تمت إضافة {len(challenges)} تحدياً بنجاح!")
        else:
            print("⚠️ التحديات موجودة بالفعل في قاعدة البيانات")


# ==========================================
# Pages
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
    data = request.get_json() or {}

    incoming_cart = data.get("cart")
    incoming_total = data.get("total")

    cart = incoming_cart if incoming_cart is not None else get_cart()

    if not cart:
        return jsonify({"status": "error", "message": "Cart is empty"}), 400

    computed_summary = calculate_cart_totals(cart)
    total = float(incoming_total) if incoming_total is not None else computed_summary["total_price"]

    order_items = []
    for item in cart:
        order_items.append({
            "name": item.get("name"),
            "qty": int(item.get("qty", 1)),
            "price": float(item.get("price", 0))
        })

    order = {
        "order_id": f"ORD-{current_user.id}-{int(datetime.utcnow().timestamp())}",
        "user_id": current_user.id,
        "username": current_user.username,
        "items": order_items,
        "total": round(total, 2),
        "items_count": computed_summary["items_count"],
        "created_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

    orders = get_user_orders()
    orders.append(order)
    save_user_orders(orders)
    clear_cart()

    award_points(current_user, max(5, int(total // 50)))

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()

    return jsonify({
        "status": "success",
        "message": f"Order completed successfully! Total paid: {round(total, 2)} EGP",
        "order": order,
        "profile_redirect": url_for('profile'),
        "shop_stats": {
            "orders_count": len(orders),
            "total_spent": round(sum(float(order.get('total', 0)) for order in orders), 2)
        },
        "user_points": current_user.points,
        "user_level": current_user.level
    })


# ==========================================
# Hosting Pages
# ==========================================
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


# ==========================================
# DB init
# ==========================================
def init_database():
    with app.app_context():
        db.create_all()
        seed_challenges()
        print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_database()
    app.run(debug=True, port=5000)
