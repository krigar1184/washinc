import uuid
from flask import Response, Blueprint, request, current_app, url_for, session, redirect
from flask.json import jsonify
from wash import service
from wash.models import Product


api = Blueprint('api', __name__, url_prefix='/')


@api.errorhandler(404)
def not_found(*args, **kwargs):
    return 'Page not found', 404


@api.route("/")
def index():
    return redirect(url_for('create_product_view'))


@api.route("/reservations")
def reservations_list_view():
    customer_id = session.get('customer_id', None)

    if customer_id is None:
        session.permanent = True
        customer_id = str(uuid.uuid4())
        session['customer_id'] = customer_id

    try:
        reservations = service.get_reservations(customer_id)
    except Exception:
        return '', 500

    return jsonify([r.as_dict() for r in reservations]), 200

@api.route("/reservation/<product_id>", methods=["PUT", "DELETE"])
def reservation_view(product_id):
    try:
        Product.get(id=product_id)  # crutch: making sure the product exists
    except Exception:
        return '', 404

    customer_id = session.get('customer_id', None)

    if customer_id is None:
        session.permanent = True
        customer_id = str(uuid.uuid4())
        session['customer_id'] = customer_id

    if request.method == 'PUT':
        try:
            service.create_reservation(product_id, customer_id)
        except Exception:
            return '', 500

        return '', 201

    if request.method == 'DELETE':
        try:
            service.cancel_reservation(product_id, customer_id)
        except Exception:
            return '', 500

        return '', 204


@api.route("/products", methods=["PUT", 'GET'])
def create_product_view():
    if request.method == 'PUT':
        try:
            product = service.create_product(**request.json)
        except Exception:
            return '', 400

        return jsonify({"product_url": url_for('api.product_view', product_id=product.id)}), 201
    
    if request.method == 'GET':
        return jsonify([p.as_dict() for _, p in Product.all().items()]), 200


@api.route("/product/<product_id>", methods=["GET", "DELETE", "PUT"])
def product_view(product_id):
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

        return jsonify({"product_url": url_for('api.product_view', product_id=product.id)}), 200

    if request.method == "DELETE":
        try:
            service.delete_product(product_id)
        except Exception:
            return '', 400

        return '', 204
