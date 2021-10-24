from os import environ as env
import math
import requests


class SurveyMonkeyAPI:
    """
    Args:
        per_page (int): Set how many items (surveys or set of responses) will return per request of Survey Monkey
        (SM) API.
        Max of 100 items allowed per page. Default value in SM is 50 items.
    """

    def __init__(self, per_page=100):
        self.token = env.get('SM_ACCESS_TOKEN')
        self.all_surveys = []
        self.all_surveys_ids = []
        self.per_page = per_page
        self.base_url = 'https://api.surveymonkey.com/v3'
        self.session = self._create_session()

    def _create_session(self):
        session = requests.session()
        session.headers.update({
            "Authorization": "Bearer %s" % self.token,
            "Content-Type": "application/json"
        })
        return session

    def surveys(self):
        """Get all surveys in SM account of interest.
        Gather survey data from pages.
        The data is presented in pages with a max of 100 surveys (items) per page.

        Returns:
            list[dict]: Main information about every survey in SM account.
        """

        if self.all_surveys:
            return self.all_surveys

        all_surveys_url = '{}/surveys?page=1&per_page={}'
        return_all_surveys = self.session.get(all_surveys_url.format(self.base_url, self.per_page))
        every_surveys = return_all_surveys.json()
        if return_all_surveys.status_code == 200:
            number_pages = math.ceil(every_surveys['total'] / self.per_page)
            for page in range(number_pages):
                page += 1
                if page == 1:
                    for data in every_surveys['data']:
                        surveys = {
                            'survey_id': data['id'],
                            'title_survey': data['title'],
                            'nick_survey': data['nickname'],
                            'link_survey': data['href']
                        }
                        self.all_surveys.append(surveys)
                        self.all_surveys_ids.append(surveys['survey_id'])
                else:
                    all_surveys_url = 'https://api.surveymonkey.com/v3/surveys?page={}&per_page={}'
                    response_all_surveys = self.session.get(all_surveys_url.format(page, self.per_page))
                    every_surveys = response_all_surveys.json()
                    for data in every_surveys['data']:
                        surveys = {
                            'survey_id': data['id'],
                            'title_survey': data['title'],
                            'nick_survey': data['nickname'],
                            'link_survey': data['href']
                        }
                        self.all_surveys.append(surveys)
                        self.all_surveys_ids.append(surveys['survey_id'])

            return self.all_surveys, self.all_surveys_ids
