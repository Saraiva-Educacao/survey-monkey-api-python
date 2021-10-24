import math
from src.data.api import SurveyMonkeyAPI


class DataSurveys(SurveyMonkeyAPI):
    def __init__(self):
        super().__init__()
        self.map_choices = {}
        self.map_rows = {}
        self.map_questions = {}
        self.all_surveys, self.all_surveys_ids = self.surveys()
        self.length_all_surveys_ids = len(self.all_surveys_ids)

    def update_sets_surveys(self, current_id, current_survey):
        """Extract more information to update table all_surveys by enpoint
        'https://api.surveymonkey.com/v3/surveys/{survey_id}/details'

        Args:
            current_id [int]: ID of survey of interest to extract information by endpoint of interest.
            current_survey [list[dict]]: list of all page objects, each containing a list of details
            objects of survey of interest.

        Returns:
            list[dict]: more information about current survey
        """

        for data in self.all_surveys:
            if str(current_id) in data['survey_id']:
                data['response_count'] = current_survey['response_count']
                data['date_created'] = current_survey['date_created']
                data['date_modified'] = current_survey['date_modified']

    def get_survey_questions(self, current_id, current_survey):
        """"Details about questions by enpoint
        'https://api.surveymonkey.com/v3/surveys/{survey_id}/details'

        Custom map function ({id: label}) to:
        (i) questions;
        (ii) choises (rank/option avaliabe to select);
        (iii) rows (item of interest to rank); and
        (iv) number of responses to realize pagination in responses endpoint.

        Args:
            current_id [int]: ID of survey of interest to extract information by endpoint of interest.
            current_survey [list[dict]]: list of all page objects, each containing a list of questions
            objects of survey of interest.

        Return:
            list[dict]: details about questions of current survey
        """

        survey_questions = []

        print(f'Survey ID: {current_id}')
        for page in current_survey['pages']:
            for question in page['questions']:
                survey_question = {
                    'survey_id': current_id,
                    'page_id': page['id'],
                    'question_id': question['id'],
                    'question_position': question['position'],
                    'question': question['headings'][0]['heading']
                }
                self.map_questions[str(survey_question['question_id'])] = survey_question['question']
                rows = question.get('answers', {}).get('rows')
                choices = question.get('answers', {}).get('choices')

                if rows:
                    survey_question['item'] = [{'id': row['id'], 'text': row['text']} for row in rows]
                    for row in rows:
                        self.map_rows[str(row['id'])] = row['text']

                    survey_question['item'] = str(survey_question['item'])

                if choices:
                    survey_question['choices'] = [{'id': str(choice['id']), 'text': choice['text']} for choice in
                                                  choices]
                    for choice in choices:
                        self.map_choices[choice['id']] = choice['text']

                    survey_question['choices'] = str(survey_question['choices'])

                survey_questions.append(survey_question)

        print(f'Table questions of {current_id} OK')

        return survey_questions

    def get_survey_responses(self, current_id, current_survey):
        """Extract responses by enpoint
        'https://api.surveymonkey.com/v3/surveys/{survey_id}/responses/bulk?page={number_page}&per_page={items_per_page}'

        Attention about pagination!

        Args:
            current_id [int]: ID of survey of interest to extract information by endpoint of interest.
            current_survey [list[dict]]: list of all page objects, each containing a list of set of responses
            objects of survey of interest.

        Extract data:
            list[dict]: set of responses of current survey
        """

        survey_responses = []

        number_pages = math.ceil(current_survey['response_count'] / self.per_page)
        for number_page in range(number_pages):
            number_page += 1
            all_responses_url = '{}/surveys/{}/responses/bulk?page={}&per_page={}'
            return_all_responses = self.session.get(all_responses_url.format(self.base_url, current_id,
                                                                             number_page, self.per_page))
            all_responses = return_all_responses.json()
            if return_all_responses.status_code == 200:
                print(f'Table responses of {current_id} - page {number_page}')
                for response in all_responses['data']:
                    for page in response['pages']:
                        for question in page['questions']:
                            for answer in question['answers']:
                                r = {
                                    'response_id': response['id'],
                                    'survey_id': current_id,
                                    'page_id': page['id'],
                                    'question_id': question['id'],
                                    'question_label': self.map_questions[question['id']],
                                    'item_id': 'Not apply',
                                    'item_label': 'Not apply',
                                    'answer': 'Not apply',
                                    'total_time': response['total_time'],
                                    'date_created': response['date_created'][:-6],
                                    'date_modified': response['date_modified'][:-6]
                                }
                                survey_responses.append(r)

                                if 'text' in answer.keys():
                                    question_response = answer['text']
                                    r['answer'] = question_response
                                    if 'Por favor, insira o número do seu CPF:' in r['question_label']:
                                        r['answer'] = 'Sensitive data'

                                elif 'choice_id' and 'row_id' in answer.keys():
                                    if answer['choice_id']:
                                        question_response = self.map_choices[answer['choice_id']]
                                        question_item = self.map_rows[answer['row_id']]
                                    else:
                                        question_response = self.map_choices[answer['choice_id']]
                                        question_item = ''
                                    r['item_id'] = answer['row_id']
                                    r['item_label'] = question_item
                                    r['answer'] = question_response

                                elif 'choice_id' in answer.keys():
                                    choices = answer['choice_id']
                                    for choice in choices:
                                        question_response = self.map_choices[choices]
                                        r['answer'] = question_response

                print(f'Table responses of {current_id} OK')

        return survey_responses

    def get_all_data(self, first_position, last_position):
        """Get all data about of each surveys:
            (i) main information;
            (ii) all questions;
            (iii) all responses.

        Args:
            first_position [int]: first position of interest of vector sets_surveys_ids.
                                The deafult value is 0.
            last_position [int]: last position of interest of vector sets_surveys_ids.
                                The deafult value is len(all_surveys_ids).

        Extract data:
            list[dict]: set of information about survey selected
            list[dict]: set of all questions of survey selected
            list[dict]: set of all responses of survey selected
        """

        all_questions = []
        all_responses = []
        if not first_position:
            first_position = 0
        if not last_position:
            last_position = len(self.all_surveys_ids)
        for survey_id in self.all_surveys_ids[first_position:last_position]:
            details_questions_url = '{}/surveys/{}/details'
            return_details_questions = self.session.get(details_questions_url.format(self.base_url, survey_id))
            details_questions_survey = return_details_questions.json()
            if return_details_questions.status_code == 200:
                self.update_sets_surveys(current_id=survey_id, current_survey=details_questions_survey)
                all_questions.extend(self.get_survey_questions(current_id=survey_id,
                                                               current_survey=details_questions_survey))
                all_responses.extend(self.get_survey_responses(current_id=survey_id,
                                                               current_survey=details_questions_survey))

        return self.all_surveys, all_questions, all_responses
