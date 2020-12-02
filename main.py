import flask
from product import product
from beautyset import beauty_set, show_beauty_set
from brand import brand
from categories import categories
from user import get_user_profile
from cosmetic_desk import add_product_to_desk, delete_product_from_desk, check_product_is_saved

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False


@app.route('/', methods=["GET"])
def test():
    return "<h1>It's work!!</h1>"


app.add_url_rule("/api/v1/product", view_func=product)
app.add_url_rule("/api/v1/beautyset", view_func=beauty_set)
app.add_url_rule("/api/v1/beautyset/<topic_id>", view_func=show_beauty_set)
app.add_url_rule("/api/v1/brand", view_func=brand)
app.add_url_rule("/api/v1/categories", view_func=categories)
app.add_url_rule("/api/v1/user", view_func=get_user_profile, methods=["POST"])
app.add_url_rule("/api/v1/cosmetic_desk/check", view_func=check_product_is_saved, methods=["POST"])
app.add_url_rule("/api/v1/cosmetic_desk/add", view_func=add_product_to_desk, methods=["POST"])
app.add_url_rule("/api/v1/cosmetic_desk/delete", view_func=delete_product_from_desk, methods=["POST"])

app.run(host="192.168.1.211")
