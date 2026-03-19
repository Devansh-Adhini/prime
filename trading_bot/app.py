from flask import Flask, render_template, request, jsonify
from bot import setup_logging, get_client, get_market_price, get_balance, place_order, get_open_orders, cancel_order, get_positions, close_position, get_listen_key
from bot.client import is_mock
import os

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Setup logging
setup_logging()

# Initialize API Client (Mock by default if keys missing)
get_client()

@app.route("/")
def index():
    return render_template("index.html", mock_mode=is_mock())

@app.route("/api/market_data", methods=["GET"])
def api_market_data():
    symbol = request.args.get("symbol", "BTCUSDT")
    price = get_market_price(symbol)
    balance = get_balance()
    return jsonify({
        "symbol": symbol,
        "price": price,
        "balance": balance
    })

@app.route("/api/place_order", methods=["POST"])
def api_place_order():
    data = request.json
    try:
        symbol = data.get("symbol")
        side = data.get("side")
        order_type = data.get("order_type")
        quantity = float(data.get("quantity"))
        price = data.get("price")
        if price:
            price = float(price)

        success, response = place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Order placed successfully!",
                "data": response
            })
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error", "Unknown error occurred")
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route("/api/open_orders", methods=["GET"])
def api_open_orders():
    symbol = request.args.get("symbol", "BTCUSDT")
    orders = get_open_orders(symbol)
    return jsonify({
        "status": "success",
        "data": orders
    })

@app.route("/api/cancel_order", methods=["POST"])
def api_cancel_order():
    data = request.json
    try:
        symbol = data.get("symbol")
        order_id = data.get("orderId")
        if not symbol or not order_id:
            raise ValueError("symbol and orderId are required")
        
        success, response = cancel_order(symbol, int(order_id))
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Order canceled successfully!",
                "data": response
            })
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error", "Unknown error occurred")
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route("/api/positions", methods=["GET"])
def api_positions():
    symbol = request.args.get("symbol", "BTCUSDT")
    positions = get_positions(symbol)
    return jsonify({
        "status": "success",
        "data": positions
    })

@app.route("/api/close_position", methods=["POST"])
def api_close_position():
    data = request.json
    try:
        symbol = data.get("symbol")
        if not symbol:
            raise ValueError("symbol is required")
        
        success, response = close_position(symbol)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Position closed successfully!",
                "data": response
            })
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error", "Unknown error occurred")
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route("/api/listen_key", methods=["GET"])
def api_listen_key():
    key = get_listen_key()
    if key:
        return jsonify({"status": "success", "listenKey": key})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
