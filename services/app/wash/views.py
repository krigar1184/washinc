from flask import Response, Blueprint, request, current_app, url_for
from flask.json import jsonify
from wash import service
from wash.models import Product


api = Blueprint('api', __name__, url_prefix='/')


@api.errorhandler(404)
def not_found(*args, **kwargs):
    return 'Page not found', 404


@api.route("/")
def index():
    return 'Nothing of interest here, sorry'


@api.route("/price/retail/<product_id>", methods=["GET", "PUT"])
def retail_price_view(product_id):
    if request.method == 'GET':
        return jsonify({'retail_price': service.get_retail_price()}), 200

    service.set_retail_price(request.json['retail_price'])
    return '', 204


@api.route("/reservations/<product_id>", methods=["GET", "PUT", "DELETE"])
def reservations(product_id):
    product = Product.get(id=product_id)

    if request.method == 'GET':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass


@api.route("/reservations/get")
def get_reservations_view():
    return jsonify({"reservations_count": str(service.get_reservations())})


@api.route("/reservations/create", methods=["PUT"])
def create_reservation_view():
    return '', 204


@api.route("/reservations/cancel", methods=["DELETE"])
def cancel_reservation_view():
    return '', 204


@api.route("/product/create", methods=["PUT"])
def create_product():
    try:
        product = service.create_product(**request.json)
    except Exception:
        return '', 400

    return jsonify({"product_url": url_for('api.product', product_id=product.id)}), 201


@api.route("/product/<product_id>", methods=["GET", "DELETE", "PUT"])
def product(product_id):
    try:
        product = Product.get(id=product_id)
    except Exception:
        return '', 404

    if request.method == 'GET':
        return jsonify(product.as_dict()), 200
    
    if request.method == "PUT":
        try:
            service.update_product(product_id, **request.json)
        except Exception as e:
            return '', 400

        return jsonify({"product_url": url_for('api.product', product_id=product.id)}), 200

    if request.method == "DELETE":
        try:
            service.delete_product(product_id)
        except Exception:
            return '', 400

        return '', 204
