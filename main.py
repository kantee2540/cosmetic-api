import flask
from product import product
from beautyset import beauty_set, show_beauty_set,\
    save_beauty_set, delete_beauty_save_set, beauty_check_liked, set_like, set_unlike,\
    get_beauty_set, get_my_beauty_set, add_beauty_set, delete_beauty_set, edit_beauty_set
from brand import brand
from categories import categories
from user import get_user_profile, create_user, update_user, delete_user, upload_profile
from cosmetic_desk import add_product_to_desk,\
    delete_product_from_desk, check_product_is_saved,\
    get_cosmetic_desk, get_cosmetic_desk_favorite,\
    update_favorite
from home import home_display
from share import share_product, share_beauty_set
from flask_cors import CORS

UPLOAD_FOLDER = './static'

app = flask.Flask(__name__, static_url_path="", static_folder="static")
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/', methods=["GET"])
def root_url():
    return {
        "version": "1.0.0"
    }


@app.route('/profile_img/<path:filename>')
def base_static(filename):
    return flask.send_from_directory(UPLOAD_FOLDER + '/profile', filename)


@app.route('/beautyset_cover/<path:filename>')
def base_beautyset_cover(filename):
    return flask.send_from_directory(UPLOAD_FOLDER + "/beauty_set_cover", filename)


@app.route('/image/<path:filename>')
def base_cosmetic_image(filename):
    return flask.send_from_directory(UPLOAD_FOLDER + "/Images", filename)


app.add_url_rule("/home", view_func=home_display)
app.add_url_rule("/product", view_func=product)

app.add_url_rule("/beautyset", view_func=beauty_set)
app.add_url_rule("/beautyset/<topic_id>", view_func=show_beauty_set)
app.add_url_rule("/beautyset/my_set/save", view_func=save_beauty_set, methods=["POST"])
app.add_url_rule("/beautyset/my_set/delete", view_func=delete_beauty_save_set, methods=["POST"])
app.add_url_rule("/beautyset/my_set/is_liked", view_func=beauty_check_liked, methods=["POST"])
app.add_url_rule("/beautyset/my_set/set_like", view_func=set_like, methods=["POST"])
app.add_url_rule("/beautyset/my_set/set_unlike", view_func=set_unlike, methods=["POST"])
app.add_url_rule("/beautyset/my_set/saved_set", view_func=get_beauty_set, methods=["POST"])
app.add_url_rule("/beautyset/my_set", view_func=get_my_beauty_set, methods=["POST"])
app.add_url_rule("/beautyset/add", view_func=add_beauty_set, methods=["POST"])
app.add_url_rule("/beautyset/delete", view_func=delete_beauty_set, methods=["POST"])
app.add_url_rule("/beautyset/edit", view_func=edit_beauty_set, methods=["POST"])

app.add_url_rule("/brand", view_func=brand)
app.add_url_rule("/categories", view_func=categories)
app.add_url_rule("/user", view_func=get_user_profile, methods=["POST"])
app.add_url_rule("/user/create", view_func=create_user, methods=["POST"])
app.add_url_rule("/user/update", view_func=update_user, methods=["POST"])
app.add_url_rule("/user/delete", view_func=delete_user, methods=["POST"])
app.add_url_rule("/user/upload_profile", view_func=upload_profile, methods=["POST"])

app.add_url_rule("/cosmetic_desk/check", view_func=check_product_is_saved, methods=["POST"])
app.add_url_rule("/cosmetic_desk/add", view_func=add_product_to_desk, methods=["POST"])
app.add_url_rule("/cosmetic_desk/delete", view_func=delete_product_from_desk, methods=["POST"])

app.add_url_rule("/cosmetic_desk/list", view_func=get_cosmetic_desk, methods=["POST"])
app.add_url_rule("/cosmetic_desk/favorite", view_func=get_cosmetic_desk_favorite, methods=["POST"])
app.add_url_rule("/cosmetic_desk/update_favorite", view_func=update_favorite, methods=["POST"])

app.add_url_rule("/brand", view_func=brand)
app.add_url_rule("/categories", view_func=categories)

app.add_url_rule("/share/product", view_func=share_product)
app.add_url_rule("/share/beautyset", view_func=share_beauty_set)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
