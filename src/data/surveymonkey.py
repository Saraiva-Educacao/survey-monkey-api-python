# This file is responsible for orchestrating the functions that gathered data from the API

from src.data.surveys import DataSurveys


class SurveyMonkey(DataSurveys):
    def __init__(self, first_position=None, last_position=None):
        """
        Args:
            first_position [int]: first position of interest of vector all_surveys_ids.
            last_position [int]: last position of interest of vector all_surveys_ids.
        """
        super().__init__()
        self.all_surveys, self.all_questions, self.all_responses = DataSurveys().get_all_data(
            first_position=first_position,
            last_position=last_position
        )

    def get_records(self, table_name):
        """
        Get records for the specified table.

        Args:
            table_name (str): Desired table. Possible values are 'all_surveys', 'questions_surveys'
            and 'responses_surveys'.

        Returns:
            list[dict]: List of dicts with all records ready to load.

        Raises:
            KeyError: when table_name is not valid.
        """

        if table_name == 'all_surveys':
            print('Getting all surveys...')
            return self.all_surveys
        elif table_name == 'questions_surveys':
            print('Getting questions of all surveys...')
            return self.all_questions
        elif table_name == 'responses_surveys':
            print('Getting responses of all surveys...')
            return self.all_responses
        else:
            raise KeyError("The table name you provided is not valid.")

    def get_schema(self, table_name):
        """
        Get schema for the specified table.

        Args:
            table_name (str): Desired table. Possible values are 'all_surveys', 'questions_surveys'
            and 'responses_surveys'.

        Returns:
            list[dict]: List of dicts with all records ready to load.

        Raises:
            KeyError: when table_name is not valid.
        """

        if table_name == 'all_surveys':
            all_surveys_schema = [
                {'column_name': 'survey_id', 'column_type': 'INTEGER'},
                {'column_name': 'title_survey', 'column_type': 'STRING'},
                {'column_name': 'nick_survey', 'column_type': 'STRING'},
                {'column_name': 'link_survey', 'column_type': 'STRING'},
                {'column_name': 'response_count', 'column_type': 'INTEGER'},
                {'column_name': 'date_created', 'column_type': 'DATETIME'},
                {'column_name': 'date_modified', 'column_type': 'DATETIME'},
            ]

            return all_surveys_schema

        elif table_name == 'questions_surveys':
            questions_surveys_schema = [
                {'column_name': 'survey_id', 'column_type': 'INTEGER'},
                {'column_name': 'page_id', 'column_type': 'INTEGER'},
                {'column_name': 'question_id', 'column_type': 'INTEGER'},
                {'column_name': 'question_position', 'column_type': 'INTEGER'},
                {'column_name': 'question', 'column_type': 'STRING'},
                {'column_name': 'item', 'column_type': 'STRING'},
                {'column_name': 'choices', 'column_type': 'STRING'},
            ]

            return questions_surveys_schema

        elif table_name == 'responses_surveys':
            responses_surveys_schema = [
                {'column_name': 'response_id', 'column_type': 'INTEGER'},
                {'column_name': 'survey_id', 'column_type': 'INTEGER'},
                {'column_name': 'page_id', 'column_type': 'INTEGER'},
                {'column_name': 'question_id', 'column_type': 'INTEGER'},
                {'column_name': 'question_label', 'column_type': 'STRING'},
                {'column_name': 'item_id', 'column_type': 'STRING'},
                {'column_name': 'item_label', 'column_type': 'STRING'},
                {'column_name': 'answer', 'column_type': 'STRING'},
                {'column_name': 'total_time', 'column_type': 'INTEGER'},
                {'column_name': 'date_created', 'column_type': 'DATETIME'},
                {'column_name': 'date_modified', 'column_type': 'DATETIME'},
            ]

            return responses_surveys_schema

        else:
            raise KeyError(f"Table {table_name} not available.")
