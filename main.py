import datetime
from flask import Flask, request, render_template, redirect, abort, jsonify, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from sqlalchemy.orm import joinedload

from data import db_session
from data.tours import Tour
from data.users import User, AnonymousUser
from data.bookings import Booking
from forms.loginform import LoginForm
from forms.user import RegisterForm
from forms.tour_form import TourForm
from forms.booking_form import BookingForm
from forms.user_profile_form import UserProfileForm

from apis.users_api import users_api
from apis.tours_api import tours_api
from apis.bookings_api import bookings_api
from apis.ai_api import ai_api

app = Flask(__name__)
app.config["SECRET_KEY"] = "just_simple_key"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("404.html"), 404


# ========== ГЛАВНАЯ ==========
@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')

    query = db_sess.query(Tour).filter(Tour.is_active == True)

    if search_query:
        query = query.filter(Tour.title.contains(search_query) | Tour.location.contains(search_query))
    if category:
        query = query.filter(Tour.category == category)

    tours = query.all()

    # Добавляем иконки категорий для отображения
    category_icons = {
        'hiking': '🏔️',
        'city': '🏙️',
        'adventure': '🚣',
        'cultural': '🏛️',
        'food': '🍜',
        'nature': '🌿',
        'extreme': '⚡'
    }

    category_names = {
        'hiking': 'Походы',
        'city': 'Городские',
        'adventure': 'Приключения',
        'cultural': 'Культура',
        'food': 'Гастрономия',
        'nature': 'Природа',
        'extreme': 'Экстрим'
    }

    for tour in tours:
        tour.category_icon = category_icons.get(tour.category, '📍')
        tour.category_name = category_names.get(tour.category, tour.category)

    return render_template("index.html",
                           tours=tours,
                           search_query=search_query,
                           category=category)


# ========== AI ПОМОЩНИК ==========
@app.route("/ai-chat")
def ai_chat():
    return render_template("ai_chat.html", title="AI-помощник")


# ========== ДЕТАЛИ ТУРА ==========
@app.route("/tour/<int:tour_id>")
def tour_detail(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour:
        abort(404)

    category_names = {
        'hiking': 'Походы и трекинг',
        'city': 'Городские экскурсии',
        'adventure': 'Приключения',
        'cultural': 'Культура и искусство',
        'food': 'Гастрономия',
        'nature': 'Природа',
        'extreme': 'Экстрим'
    }

    booking_form = BookingForm()

    return render_template("tour_detail.html",
                           tour=tour,
                           category_name=category_names.get(tour.category, tour.category),
                           booking_form=booking_form)


# ========== БРОНИРОВАНИЕ ==========
@app.route("/tour/<int:tour_id>/book", methods=["POST"])
@login_required
def book_tour(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour:
        abort(404)

    form = BookingForm()

    if form.validate_on_submit():
        total_price = tour.price * form.people_count.data

        booking = Booking(
            people_count=form.people_count.data,
            total_price=total_price,
            message=form.message.data,
            traveler_id=current_user.id,
            tour_id=tour_id,
            status='pending'
        )

        db_sess.add(booking)
        db_sess.commit()

        return redirect(url_for('my_bookings'))

    return redirect(url_for('tour_detail', tour_id=tour_id))


# ========== ЛИЧНЫЙ КАБИНЕТ ==========
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserProfileForm()
    db_sess = db_session.create_session()
    user = db_sess.get(User, current_user.id)

    user = db_sess.query(User).options(joinedload(User.tours)).filter(User.id == current_user.id).first()

    if not user:
        abort(404)

    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.about.data = user.about
        form.phone.data = user.phone
        form.role.data = user.role
        form.avatar_url.data = user.avatar_url

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.phone = form.phone.data
        user.role = form.role.data
        user.avatar_url = form.avatar_url.data

        db_sess.commit()

        return redirect(url_for('profile'))

    return render_template("profile.html", form=form, user=user)


# ========== МОИ БРОНИРОВАНИЯ ==========
@app.route("/my-bookings")
@login_required
def my_bookings():
    db_sess = db_session.create_session()
    bookings = db_sess.query(Booking).filter(Booking.traveler_id == current_user.id).all()

    status_names = {
        'pending': '⏳ Ожидает подтверждения',
        'confirmed': '✅ Подтверждено',
        'cancelled': '❌ Отменено',
        'completed': '✔️ Завершено'
    }

    return render_template("my_bookings.html", bookings=bookings, status_names=status_names)


# ========== МОИ ТУРЫ (ДЛЯ ГИДА) ==========
@app.route("/my-tours")
@login_required
def my_tours():
    if not current_user.is_guide():
        abort(403)

    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).filter(Tour.guide_id == current_user.id).all()

    return render_template("my_tours.html", tours=tours)


# ========== СОЗДАНИЕ ТУРА ==========
@app.route("/create-tour", methods=["GET", "POST"])
@login_required
def create_tour():
    form = TourForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        tour = Tour(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            duration_days=form.duration_days.data,
            price=form.price.data,
            location=form.location.data,
            max_people=form.max_people.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            image_url=form.image_url.data,
            includes=form.includes.data,
            itinerary=form.itinerary.data,
            organizer_type=form.organizer_type.data,
            is_active=form.is_active.data
        )

        # Устанавливаем изображения
        images_list = form.get_images_list()
        if images_list:
            tour.set_images_list(images_list)

        # Заполняем данные в зависимости от типа организатора
        if form.organizer_type.data == 'company':
            tour.company_name = form.company_name.data or "WildRoutes"
            tour.company_description = form.company_description.data
            tour.company_phone = form.company_phone.data
            tour.company_email = form.company_email.data
            tour.company_website = form.company_website.data
            tour.guide_id = None
        else:  # guide
            tour.guide_id = current_user.id
            # Очищаем поля компании
            tour.company_name = None
            tour.company_description = None
            tour.company_phone = None
            tour.company_email = None
            tour.company_website = None

        db_sess.add(tour)
        db_sess.commit()

        return redirect(url_for('my_tours'))

    return render_template("create_tour.html", form=form, title="Создать тур")


# ========== РЕДАКТИРОВАНИЕ ТУРА ==========
@app.route("/edit-tour/<int:tour_id>", methods=["GET", "POST"])
@login_required
def edit_tour(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour or tour.guide_id != current_user.id:
        abort(404)

    form = TourForm()

    if request.method == "GET":
        form.title.data = tour.title
        form.description.data = tour.description
        form.category.data = tour.category
        form.duration_days.data = tour.duration_days
        form.price.data = tour.price
        form.location.data = tour.location
        form.max_people.data = tour.max_people
        form.start_date.data = tour.start_date
        form.end_date.data = tour.end_date
        form.image_url.data = tour.image_url
        form.includes.data = tour.includes
        form.itinerary.data = tour.itinerary
        form.is_active.data = tour.is_active

        # Поля для организатора
        if tour.organizer_type == 'company':
            form.organizer_type.data = 'company'
            form.company_name.data = tour.company_name
            form.company_description.data = tour.company_description
            form.company_phone.data = tour.company_phone
            form.company_email.data = tour.company_email
            form.company_website.data = tour.company_website
        else:
            form.organizer_type.data = 'guide'

        # Загружаем изображения
        images = tour.get_images_list()
        if images:
            form.images.data = ', '.join(images)

    if form.validate_on_submit():
        tour.title = form.title.data
        tour.description = form.description.data
        tour.category = form.category.data
        tour.duration_days = form.duration_days.data
        tour.price = form.price.data
        tour.location = form.location.data
        tour.max_people = form.max_people.data
        tour.start_date = form.start_date.data
        tour.end_date = form.end_date.data
        tour.image_url = form.image_url.data
        tour.includes = form.includes.data
        tour.itinerary = form.itinerary.data
        tour.is_active = form.is_active.data
        tour.organizer_type = form.organizer_type.data

        # Обновляем изображения
        images_list = form.get_images_list()
        if images_list:
            tour.set_images_list(images_list)
        else:
            tour.set_images_list([])

        # Обновляем данные организатора
        if form.organizer_type.data == 'company':
            tour.company_name = form.company_name.data or "WildRoutes"
            tour.company_description = form.company_description.data
            tour.company_phone = form.company_phone.data
            tour.company_email = form.company_email.data
            tour.company_website = form.company_website.data
            tour.guide_id = None
        else:
            tour.guide_id = current_user.id
            tour.company_name = None
            tour.company_description = None
            tour.company_phone = None
            tour.company_email = None
            tour.company_website = None

        db_sess.commit()

        return redirect(url_for('my_tours'))

    return render_template("create_tour.html", form=form, title="Редактировать тур")


# ========== УДАЛЕНИЕ ТУРА ==========
@app.route("/delete-tour/<int:tour_id>")
@login_required
def delete_tour(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour or tour.guide_id != current_user.id:
        abort(404)

    db_sess.delete(tour)
    db_sess.commit()

    return redirect(url_for('my_tours'))


# ========== ОТМЕНА БРОНИРОВАНИЯ ==========
@app.route("/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    db_sess = db_session.create_session()
    booking = db_sess.get(Booking, booking_id)

    if not booking or booking.traveler_id != current_user.id:
        abort(404)

    booking.status = 'cancelled'
    db_sess.commit()

    return redirect(url_for('my_bookings'))


# ========== АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ ==========
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   message="Пароли не совпадают", form=form)

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Регистрация",
                                   message="Такой пользователь уже есть", form=form)

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            role=form.role.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect("/login")

    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or "/")

    return render_template("login.html", title="Авторизация", f=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html", title="О нас")


@app.route("/contacts", methods=["GET", "POST"])
def get_feedback():
    return render_template("contacts.html", title="Обратная связь")


if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(users_api)
    app.register_blueprint(tours_api)
    app.register_blueprint(bookings_api)
    app.register_blueprint(ai_api)
    app.run(host="127.0.0.1", port=5000, debug=True)
    profile