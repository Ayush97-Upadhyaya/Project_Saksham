import dash
import dash_auth
external_stylesheets = ['H:\PS2\Dashboard\external_stylesheet.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

VALID_USERNAME_PASSWORD_PAIRS=[['utcl-admin','utcl@456'],['123','123']]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
