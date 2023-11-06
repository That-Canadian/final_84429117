from waitress import serve
import app
serve(app.app, host='0.0.0.0', port=50627, url_prefix='/add_new')
