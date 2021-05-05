from flask_restx import fields


class Models:
    def __init__(self, api, api_namespace):
        self.api = api
        self.api_namespace = api_namespace

        self.add_course_data_model = {
            'title': fields.String(example='Yalantis Python School', required=False),
            'start_date': fields.String(example='17-05-2021', required=False),
            'end_date': fields.String(example='30-08-2021', required=True),
            'lectures_count': fields.Integer(example=22, required=False)}

    def get_course_data_model(self):
        data_model = self.api_namespace.model('add_course_data_model', self.add_course_data_model)
        return data_model
