from flask import Blueprint, jsonify, request, abort
from data import db_session
from data.tours import Tour

tours_api = Blueprint("tours_api", __name__, url_prefix="/api/tours")


def tour_to_dict(tour):
    return {
        "id": tour.id,
        "title": tour.title,
        "description": tour.description,
        "category": tour.category,
        "duration_days": tour.duration_days,
        "price": tour.price,
        "location": tour.location,
        "max_people": tour.max_people,
        "start_date": tour.start_date.isoformat() if tour.start_date else None,
        "end_date": tour.end_date.isoformat() if tour.end_date else None,
        "image_url": tour.image_url,
        "includes": tour.includes,
        "itinerary": tour.itinerary,
        "guide_id": tour.guide_id,
        "is_active": tour.is_active,
        "created_date": tour.created_date.isoformat() if tour.created_date else None
    }


@tours_api.get("/")
def get_tours():
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).filter(Tour.is_active == True).all()
    return jsonify([tour_to_dict(t) for t in tours])


@tours_api.get("/<int:tour_id>")
def get_tour(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)
    if not tour:
        abort(404)
    return jsonify(tour_to_dict(tour))


@tours_api.get("/guide/<int:guide_id>")
def get_guide_tours(guide_id):
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).filter(Tour.guide_id == guide_id).all()
    return jsonify([tour_to_dict(t) for t in tours])


@tours_api.post("/")
def create_tour():
    data = request.json
    db_sess = db_session.create_session()

    tour = Tour(
        title=data["title"],
        description=data["description"],
        category=data["category"],
        duration_days=data["duration_days"],
        price=data["price"],
        location=data["location"],
        max_people=data["max_people"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        image_url=data.get("image_url"),
        includes=data.get("includes"),
        itinerary=data.get("itinerary"),
        guide_id=data["guide_id"],
        is_active=data.get("is_active", True)
    )

    db_sess.add(tour)
    db_sess.commit()

    return jsonify({"status": "ok", "id": tour.id})


@tours_api.put("/<int:tour_id>")
def update_tour(tour_id):
    data = request.json
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour:
        abort(404)

    for key, value in data.items():
        if hasattr(tour, key):
            setattr(tour, key, value)

    db_sess.commit()
    return jsonify({"status": "updated"})


@tours_api.delete("/<int:tour_id>")
def delete_tour(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.get(Tour, tour_id)

    if not tour:
        abort(404)

    db_sess.delete(tour)
    db_sess.commit()

    return jsonify({"status": "deleted"})