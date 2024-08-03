from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Reservation, db
from datetime import datetime

reservations = Blueprint('reservations', __name__)

@reservations.route('/reserve', methods=['POST'])
@jwt_required()
def make_reservation():
    data = request.get_json()
    user_id = get_jwt_identity()
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    reservation = Reservation(date=date, user_id=user_id)
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation made successfully"}), 201

@reservations.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    user_id = get_jwt_identity()
    user_reservations = Reservation.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": r.id, "date": r.date.isoformat()} for r in user_reservations]), 200