from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('M', 'F', 'Other'), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(32))
    is_email_confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    reviews = db.relationship('Review', back_populates='user', cascade="all,delete")
    appointments = db.relationship('Appointment', back_populates='user', cascade="all,delete")

    @property
    def age(self):
        from datetime import date
        return date.today().year - self.birth_date.year - ((date.today().month, date.today().day) < (self.birth_date.month, self.birth_date.day))


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(64))
    doctors = db.relationship('Doctor', back_populates='city', cascade="all,delete")


class Specialization(db.Model):
    __tablename__ = 'specializations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    doctors = db.relationship('Doctor', back_populates='specialization', cascade="all,delete")


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    visit_type = db.Column(db.Enum('gabinet', 'online', 'both'), nullable=False, default='both')
    address = db.Column(db.String(255))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(255))
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    experience_years = db.Column(db.Integer, default=0)
    photo_url = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    working_hours = db.Column(db.String(255), default="08:00-16:00")  # Przykład: "08:00-16:00"
    working_days = db.Column(db.String(20), default="01234")  # np. "01234" = pn-pt
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    specialization = db.relationship('Specialization', back_populates='doctors')
    city = db.relationship('City', back_populates='doctors')
    services = db.relationship('Service', secondary='doctor_services', back_populates='doctors')
    reviews = db.relationship('Review', back_populates='doctor', cascade="all,delete")
    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all,delete")


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable=False)
    doctors = db.relationship('Doctor', secondary='doctor_services', back_populates='services')


class DoctorService(db.Model):
    __tablename__ = 'doctor_services'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)  # Dodana kolumna
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())  # Dodana kolumna

    doctor = db.relationship('Doctor', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
    appointment = db.relationship('Appointment', backref=db.backref('review', lazy=True, uselist=False))  # Dodana relacja

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending','confirmed','completed','cancelled'), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    doctor = db.relationship('Doctor', back_populates='appointments')
    user = db.relationship('User', back_populates='appointments')

