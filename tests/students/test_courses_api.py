import pytest as pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# получение списка курсов

@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)


# получение одного курса

@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(name='course')
    url = reverse('courses-detail', args=(courses.id,))

    response = client.get(url)
    data = response.json()
    course = Course.objects.filter(id=data['id'])

    assert response.status_code == 200
    assert data['id'] == course[0].id


# создание курса

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'course_1'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


# фильтрация по идентификатору

@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'id': courses[0].id})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id


# фильтрация по названию

@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, data={'name': courses[2].name})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses[2].name


# изменение курса

@pytest.mark.django_db
def test_update_courses(client, course_factory):
    courses = course_factory(_quantity=1)
    url = reverse('courses-detail', args=(courses[0].id,))
    data = {'name': 'updated_course'}
    resp = client.patch(url, data=data)

    assert resp.status_code == 200
    assert resp.data['name'] == 'updated_course'


# удаление курса

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=3)
    url = reverse('courses-detail', args=(courses[0].id,))
    client.delete(url)
    response = client.get(url)
    data = response.json()

    assert response.status_code == 404
    assert courses[0].id not in data
