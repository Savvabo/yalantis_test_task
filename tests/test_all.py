from flask_testing import TestCase
import unittest
from main import app
from db_models import db, Course
from utils import row_to_dict
from copy import deepcopy


class MyTest(TestCase):
    test_user = {
        "title": "Yalantis Python School",
        "start_date": "17-05-2021",
        "end_date": "30-08-2021",
        "lectures_count": 22
    }

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_course(self, course):
        response = self.client.post("/courses/add_course", json=course)
        added_id = response.json['id']
        return added_id

    def test_add_course(self):
        added_id = self.add_course(deepcopy(MyTest.test_user))
        added_course = Course.query.filter_by(id=added_id).first()
        assert added_course is not None

    def test_change_attributes(self):
        course_copy = deepcopy(MyTest.test_user)
        added_id = self.add_course(course_copy)
        data_to_update = {'title': 'updated_title'}
        self.client.post(f"/courses/change_attributes/{added_id}", json=data_to_update)
        course_after_update = Course.query.filter_by(id=added_id).first()
        course_copy.update(dict(**data_to_update, **{'id': added_id}))
        assert row_to_dict(course_after_update) == course_copy

    def test_get_courses_list(self):
        course_copy = deepcopy(MyTest.test_user)
        added_id = self.add_course(course_copy)
        course_copy['id'] = added_id
        all_records = list(map(row_to_dict, Course.query.all()))
        assert all_records == [course_copy]

    def test_get_course(self):
        course1 = {
            "title": "course1",
            "start_date": "10-05-2021",
            "end_date": "15-05-2021",
            "lectures_count": 22
        }
        course2 = {
            "title": "course2",
            "start_date": "14-05-2021",
            "end_date": "18-05-2021",
            "lectures_count": 22
        }
        course3 = {
            "title": "course3",
            "start_date": "20-05-2021",
            "end_date": "25-05-2021",
            "lectures_count": 22
        }
        added_id1 = self.add_course(course1)
        added_id2 = self.add_course(course2)
        added_id3 = self.add_course(course3)
        course1['id'] = added_id1
        course2['id'] = added_id2
        course3['id'] = added_id3

        res1 = self.client.get(f"/courses/get_courses_by_attribute", query_string={'id': course1['id']})
        res2 = self.client.get(f"/courses/get_courses_by_attribute", query_string={'title': course2['title']})
        res3 = self.client.get(f"/courses/get_courses_by_attribute", query_string={'start_date': '14-05-2021', 'end_date': '17-05-2021'})
        res4 = self.client.get(f"/courses/get_courses_by_attribute", query_string={'start_date': '14-05-2021', 'end_date': '17-05-2021', 'title': course2['title']})
        res5 = self.client.get(f"/courses/get_courses_by_attribute", query_string={'start_date': '14-05-2021', 'end_date': '17-05-2021', 'id': course3['id']})

        assert res1.json == [course1]
        assert res2.json == [course2]
        assert res3.json == [course1, course2]
        assert res4.json == [course2]
        assert res5.json == []

    def test_delete_course(self):
        course_copy = deepcopy(MyTest.test_user)
        added_id = self.add_course(course_copy)
        res = self.client.delete(f"/courses/delete_course/{added_id}")
        db_course = Course.query.filter_by(id=added_id).first()
        assert db_course is None
        assert res.json.get('SUCCESS') is True


if __name__ == '__main__':
    unittest.main()
