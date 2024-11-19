from your_app.models import Admin, db
admin = Admin()
admin.password = "books"
db.session.add(admin)
db.session.commit()
