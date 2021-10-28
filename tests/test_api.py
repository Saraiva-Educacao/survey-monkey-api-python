import unittest
from json import load
from os import environ as env
import requests
from src.data.api import SurveyMonkeyAPI
from unittest import mock

env['SM_URL'] = 'https://api.surveymonkey.com/v3'
env['SM_ACCESS_TOKEN'] = 'SM_ACCESS_TOKEN'


def mock_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content=None):
            self.status_code = status_code
            self.content = content

        def content(self):
            return self.content

        def json(self):
            return self.content

    api_url = env['SM_URL']

    if args[0] == f"{api_url}/surveys?page=1&per_page=100":
        with open('src/tests/mocks/mock_raw_all_surveys_page_1.json', 'r') as file:
            all_surveys = load(file)

        return MockResponse(200, all_surveys)

    return MockResponse(404)


class TestSurveyMonkeyAPI(unittest.TestCase):

    def setUp(self):
        self.survey_monkey_api = SurveyMonkeyAPI()

    def tearDown(self):
        self.survey_monkey_api.session.close()

    def test_if__get_raw_contacts_raises_401_error_when_using_wrong_token(self):
       with self.assertRaises(401):
            self.survey_monkey_api.surveys()

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test__get_raw_surveys(self, mock_raw_all_surveys):
        raw_surveys = self.survey_monkey_api._get_raw_surveys()
        with open('src/tests/expected_values/expected_raw_surveys.json', 'r') as file:
            expected_raw_surveys = load(file)
        assert raw_surveys == expected_raw_surveys

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test_expected_name_columns__get_raw_surveys(self, mock_raw_all_surveys):
        raw_surveys = self.survey_monkey_api._get_raw_surveys()
        self.assertIsInstance(raw_surveys, list)
        self.assertEqual(len(raw_surveys), 2)
        expected_keys = [
            'survey_id',
            'title_survey',
            'nick_survey',
            'link_survey'
        ]
        assert list(raw_surveys[0]) == expected_keys

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test_get_survey_sets(self, mock_raw_all_surveys):
        all_surveys, all_surveys_id = self.survey_monkey_api.surveys()
        with open('src/tests/expected_values/expected_all_surveys.json', 'r') as file:
            expected_all_surveys = load(file)
        assert all_surveys == expected_all_surveys

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test_expected_name_columns_get_survey_sets(self, mock_raw_all_surveys):
        all_surveys, all_surveys_id = self.survey_monkey_api.surveys()
        self.assertIsInstance(all_surveys, list)
        self.assertEqual(len(all_surveys), 13)
        expected_keys = [
            'survey_id',
            'title_survey',
            'nick_survey',
            'link_survey'
        ]
        assert list(all_surveys[0]) == expected_keys
