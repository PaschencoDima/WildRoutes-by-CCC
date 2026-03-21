from flask import Blueprint, jsonify, request, abort
from data import db_session
from data.bookings import Booking

bookings_api = Blueprint("bookings_api", __name__, url_prefix="/api/bookings")


def booking_to_dict(booking):
    return {
        "id": booking.id,
        "people_count": booking.people_count,
        "total_price": booking.total_price,
        "status": booking.status,
        "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
        "message": booking.message,
        "traveler_id": booking.traveler_id,
        "tour_id": booking.tour_id
    }


@bookings_api.get("/")
def get_bookings():
    db_sess = db_session.create_session()
    bookings = db_sess.query(Booking).all()
    return jsonify([booking_to_dict(b) for b in bookings])


@bookings_api.get("/<int:booking_id>")
def get_booking(booking_id):
    db_sess = db_session.create_session()
    booking = db_sess.get(Booking, booking_id)
    if not booking:
        abort(404)
    return jsonify(booking_to_dict(booking))


@bookings_api.get("/traveler/<int:traveler_id>")
def get_traveler_bookings(traveler_id):
    db_sess = db_session.create_session()
    bookings = db_sess.query(Booking).filter(Booking.traveler_id == traveler_id).all()
    return jsonify([booking_to_dict(b) for b in bookings])


@bookings_api.get("/tour/<int:tour_id>")
def get_tour_bookings(tour_id):
    db_sess = db_session.create_session()
    bookings = db_sess.query(Booking).filter(Booking.tour_id == tour_id).all()
    return jsonify([booking_to_dict(b) for b in bookings])


@bookings_api.post("/")
def create_booking():
    data = request.json
    db_sess = db_session.create_session()

    booking = Booking(
        people_count=data["people_count"],
        total_price=data["total_price"],
        status=data.get("status", "pending"),
        message=data.get("message"),
        traveler_id=data["traveler_id"],
        tour_id=data["tour_id"]
    )

    db_sess.add(booking)
    db_sess.commit()

    return jsonify({"status": "ok", "id": booking.id})


@bookings_api.put("/<int:booking_id>")
def update_booking(booking_id):
    data = request.json
    db_sess = db_session.create_session()
    booking = db_sess.get(Booking, booking_id)

    if not booking:
        abort(404)

    if "status" in data:
        booking.status = data["status"]
    if "message" in data:
        booking.message = data["message"]

    db_sess.commit()
    return jsonify({"status": "updated"})


@bookings_api.delete("/<int:booking_id>")
def delete_booking(booking_id):
    db_sess = db_session.create_session()
    booking = db_sess.get(Booking, booking_id)

    if not booking:
        abort(404)

    db_sess.delete(booking)
    db_sess.commit()

    return jsonify({"status": "deleted"})