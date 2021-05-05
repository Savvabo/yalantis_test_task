from flask import Flask, jsonify, request, g
from flask_restx import Api, Resource
from models import Models
from datetime import timedelta, datetime
from db_models import db, Course
from sqlalchemy import or_, and_
from utils import row_to_dict, get_courses_columns
from const import date_format

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonsqlite.db'
db.init_app(app)
api = Api(app, title='Courses api', description='Courses api')
default_namespace = api.namespace('courses')
models = Models(api, default_namespace)

course_data_model = models.get_course_data_model()


@default_namespace.route('/add_course')
class AddCourse(Resource):
    @staticmethod
    @default_namespace.expect(course_data_model)
    def post():
        req = request.json
        try:
            course = Course(title=req['title'],
                            start_date=datetime.strptime(req['start_date'], date_format),
                            end_date=datetime.strptime(req['end_date'], date_format),
                            lectures_count=req['lectures_count'])
        except KeyError as e:
            return jsonify(ERROR=f'{e} not provided')
        db.session.add(course)
        db.session.commit()
        course_id = course.id
        return jsonify(id=course_id)


@default_namespace.route('/get_courses_list')
class GetCoursesList(Resource):
    @staticmethod
    def get():
        courses_list = list(map(row_to_dict, Course.query.all()))
        return jsonify(courses_list)


@default_namespace.route('/get_courses_by_attribute')
@default_namespace.doc(params=
                       dict(id='1', title='Some Course', start_date='20-05-2021', end_date='20-05-2021'))
class GetCourse(Resource):
    @staticmethod
    # todo refactor
    def get():
        args = request.args
        try:
            start_date_filter = datetime.strptime(args["start_date"], date_format).date()
        except:
            start_date_filter = 0
        try:
            end_date_filter = datetime.strptime(args["end_date"], date_format).date()
        except:
            end_date_filter = 0
        # user can pass empty string or no attribute
        id_filter = int(args['id']) if args.get('id') else None
        title_filter = args['title'] if args.get('title') else None
        delta = end_date_filter - start_date_filter
        id_title_filter = and_()
        filters = []
        if id_filter:
            id_title_filter = and_(id_title_filter, Course.id == id_filter)
        if title_filter:
            id_title_filter = and_(id_title_filter, Course.title == title_filter)
        if delta:
            for i in (range(delta.days + 1))[1:]:
                day = (start_date_filter + timedelta(days=i))
                delta_filter = and_(Course.end_date >= day, Course.start_date <= day, id_title_filter)
                filters.append(delta_filter)
        else:
            filters.append(id_title_filter)

        filtered_rows = db.session.query(Course).filter(or_(*filters)).all()
        response = list(map(row_to_dict, filtered_rows))
        return jsonify(response)


@default_namespace.route('/change_attributes/<course_id>')
class ChangeAttributes(Resource):
    @staticmethod
    @default_namespace.expect(course_data_model)
    def post(course_id):
        course = Course.query.filter_by(id=int(course_id)).first()
        req = request.json
        is_valid, error_msg = ChangeAttributes.validate(course_id, course, req)
        if not is_valid:
            return jsonify(ERROR=error_msg)
        for k, v in req.items():
            if k in ['start_date', 'end_date']:
                v = datetime.strptime(req['end_date'], date_format)
            setattr(course, k, v)
        db.session.commit()
        return jsonify(success=True)

    @staticmethod
    def validate(course_id, course, req):
        columns = get_courses_columns()
        if course is None:
            return False, f'No id \"{course_id}\" in db'
        for k, v in req.items():
            if k not in columns:
                return False, f'No column \"{k}\" in schema'
        return True, ''


@default_namespace.route('/delete_course/<course_id>')
class DeleteCourse(Resource):
    @staticmethod
    def delete(course_id):
        in_db = bool(Course.query.filter_by(id=int(course_id)).delete())
        db.session.commit()
        response = {'ERROR': f'No id \"{course_id}\" in db'} if in_db is False else {'SUCCESS': True}
        return jsonify(response)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000)
