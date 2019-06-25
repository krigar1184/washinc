from flask import Response, Blueprint, request, current_app
from flask.json import jsonify
from wash import service


api = Blueprint('api', __name__, url_prefix='/')


@api.errorhandler(404)
def not_found(e):
    return 'Page not found', 404


@api.route("/")
def index():
    return 'Nothing of interest here, sorry'


@api.route("/price/retail", methods=["GET", "PUT"])
def retail_price_view():
    if request.method == 'GET':
        return jsonify({'retail_price': service.get_retail_price()}), 200

    service.set_retail_price(request.json['retail_price'])
    return '', 204


@api.route("/reservations/get")
def get_reservations_view():
    return jsonify({"reservations_count": str(service.get_reservations())})


@api.route("/reservations/create", methods=["PUT"])
def create_reservation_view():
    return '', 204


@api.route("/reservations/cancel", methods=["DELETE"])
def cancel_reservation_view():
    return '', 204
