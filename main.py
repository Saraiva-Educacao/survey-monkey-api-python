from src.data.surveymonkey import SurveyMonkey
import json


def main(request=None):
    tables = [
        'all_surveys',
        'questions_surveys',
        'responses_surveys'
    ]

    if request:
        request_args = parse_http_request(request)
        if 'first_position' in request_args.keys():
            first_position = request_args['first_position']
        else:
            first_position = None
        if 'last_position' in request_args.keys():
            last_position = request_args['last_position']
        else:
            last_position = None
        if 'table' in request_args.keys():
            tables = [request_args['table']]

    surveymonkey = SurveyMonkey(first_position, last_position)

    error_messages = []
    for table in tables:
        try:
            records = surveymonkey.get_records(table_name=table)
            print(f'Extracted {len(records)} {table}')

            schema = surveymonkey.get_schema(table)

            print('Loading records...')
            with open(f'{table}.json', 'w+', encoding='utf-8') as t:
                json.dump(table, t, ensure_ascii=False, indent=4)

            with open(f'{table}_schema.json', 'w+', encoding='utf-8') as s:
                json.dump(schema, s, ensure_ascii=False, indent=4)

        except Exception as error:
            print(f'Could not transform or load all records for table {table}, giving up.')
            error_messages.append(f'Error in table {table}: {str(error)}')
            print(error_messages)

    return 'OK'


if __name__ == '__main__':
    main()
