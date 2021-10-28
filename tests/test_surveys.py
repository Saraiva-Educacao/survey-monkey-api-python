import unittest
from json import load
from os import environ as env
import requests
from src.data.surveys import DataSurveys
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

    if args[0] == f"{api_url}/surveys/111111111/details":
        with open('src/tests/mocks/mock_questions_survey_111111111.json', 'r') as file:
            questions_survey = load(file)

        return MockResponse(200, questions_survey)

    if args[0] == f"{api_url}/surveys/111111111/responses/bulk?page=1&per_page=100":
        with open('src/tests/mocks/mock_responses_survey_111111111.json', 'r') as file:
            responses_survey = load(file)

        return MockResponse(200, responses_survey)

    return MockResponse(404)


class TestDataSurveys(unittest.TestCase):

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def setUp(self, mock_raw_all_surveys):
        self.survey_monkey_surveys = DataSurveys()

    def tearDown(self):
        self.survey_monkey_surveys.session.close()

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test_get_all_data(self, mock_raw_all_surveys):
        update_all_surveys, questions_survey_111111111, \
        responses_survey_111111111 = self.survey_monkey_surveys.get_all_data(first_position=0, last_position=1)
        with open('src/tests/expected_values/expected_update_all_surveys.json', 'r') as file:
            expected_update_all_surveys = load(file)
        with open('src/tests/expected_values/expected_questions_survey_308971488.json', 'r') as file:
            expected_questions_survey_111111111 = load(file)
        with open('src/tests/expected_values/expected_responses_survey_308971488.json', 'r') as file:
            expected_responses_survey_111111111 = load(file)
        assert update_all_surveys == expected_update_all_surveys
        assert questions_survey_111111111 == expected_questions_survey_111111111
        assert responses_survey_111111111 == expected_responses_survey_111111111

    @mock.patch.object(requests.Session, 'get', side_effect=mock_requests)
    def test_expected_name_columns_get_all_data(self, mock_raw_all_surveys):
        update_all_surveys, questions_survey_111111111, \
        responses_survey_111111111 = self.survey_monkey_surveys.get_all_data(first_position=0, last_position=1)
        self.assertIsInstance(update_all_surveys, list)
        self.assertEqual(len(update_all_surveys), 2)
        expected_keys_update = [
            'survey_id',
            'title_survey',
            'nick_survey',
            'link_survey',
            'response_count',
            'date_created',
            'date_modified'
        ]
        self.assertIsInstance(questions_survey_111111111, list)
        self.assertEqual(len(questions_survey_111111111), 2)
        expected_keys_questions =[
            'survey_id',
            'page_id',
            'question_id',
            'question_position',
            'question',
            'item',
            'choices'
        ]
        self.assertIsInstance(responses_survey_111111111, list)
        self.assertEqual(len(responses_survey_111111111), 4)
        expected_keys_responses = [
            'response_id',
            'survey_id',
            'page_id',
            'question_id',
            'question_label',
            'item_id',
            'item_label',
            'answer',
            'total_time',
            'date_created',
            'date_modified'
        ]
        assert list(update_all_surveys[0]) == expected_keys_update
        assert list(questions_survey_111111111[0]) == expected_keys_questions
        assert list(responses_survey_111111111[0]) == expected_keys_responses
