from elden_ring_builder.extensions import app, db
from elden_ring_builder.main.routes import main
from elden_ring_builder.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
