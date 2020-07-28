from flask import current_app, render_template, Flask, redirect, request, url_for
import firestore
import storage
import email_helper
from google.cloud import error_reporting

app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif']),
)

app.debug = False
app.testing = False


@app.route("/")
def list_items():
    print("List_item called")
    start_after = request.args.get('start_after', None)
    items, last_item_id = firestore.next_page(start_after=start_after)
    return render_template("item_list.html", items=items, last_item_id=last_item_id)


# Add an error handler that reports exceptions to Stackdriver Error
# Reporting. Note that this error handler is only used when debug
# is False
@app.errorhandler(500)
def server_error(e):
    client = error_reporting.Client()
    client.report_exception(
        http_context=error_reporting.build_flask_context(request))
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
