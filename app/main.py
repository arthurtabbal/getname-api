from routes.hello import hello
from routes.get_name import get_name
from routes.get_multiple_names import get_multiple_names
from routes.clear_cache import clear_cache
from routes.get_search_name import search_name
from flask_api import FlaskAPI
from flask_cors import CORS
from resources.cache import cache, config

app = FlaskAPI(__name__)
CORS(app)

cache.init_app(app, config)

# Rotas de views
app.add_url_rule("/", view_func=hello)
app.add_url_rule(
    "/<string:db_id>/patient-name/<int:idPatient>", view_func=get_name, methods=["GET"]
)
app.add_url_rule(
    "/<string:db_id>/search-name/<string:partial_name>",
    view_func=search_name,
    methods=["GET"],
)
app.add_url_rule(
    "/<string:db_id>/patient-name/multiple",
    view_func=get_multiple_names,
    methods=["POST"],
)
# Rota de limpeza do dache
app.add_url_rule("/patient-name/clear", view_func=clear_cache, methods=["GET"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context="adhoc")
