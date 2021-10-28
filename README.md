# survey-monkey-api-python


Script to handle data from Survey Monkey (SM) data and save tables an schemas of tables in JSON files 
in local directory. <br>
For more information about the API endpoints of SM, please refer to
[documentation](https://developer.surveymonkey.com/api/v3/).


## Development Environment

To create the development environment it's recommended to use conda.<br>
<br>
Run the following commands to get the environment ready

```
conda create -n ENVIRONMENT_NAME python=3.8
conda activate ENVIRONMENT_NAME
pip install -r requirements.txt
```

You might need environment variable `SM_ACCESS_TOKEN` to be used in requests to Survey Monkey API.

```
export SM_ACCESS_TOKEN='YOUR TOKEN'
```

## Running
There is a function that collects data for all surveys in SM account of interest. <br>
The SM account of interest need to be a paid account to access endpoint with details of responses. <br>
The default in <i> api.py </i> is to collect and insert the data in JSON files for each table and for each schema, as 
following:<br>

### Table Surveys
<li> 'survey_id': unique ID of the interest survey <br> </li>
<li> 'title_survey': title of the interest survey <br> </li>
<li> 'nick_survey': tags of interest survey <br> </li>
<li> 'link_survey': link of interest survey <br> </li>
<li> 'response_count': number of responses survey has received <br> </li>
<li> 'date_created' date of creation of survey <br> </li>
<li> 'date_modified' last moment which the survey was modified <br> </li>

### Table questions:
<li> 'survey_id': unique ID of the interest survey <br> </li>
<li> 'page_id': unique ID of interest page <br> </li>
<li> 'question_id': unique ID per question of survey <br> </li>
<li> 'question_position': position of question in survey of interest <br> </li>
<li> 'question': label of question  <br> </li>
<li> 'item': items to evaluate in question, like 'Espaço Físico', 'Variedade de itens', etc <br> </li>
<li> 'choices': rank/option avaliabe to select, like 1 to 5 or 'insatisfeito' to 'muito satisfeito' <br> </li>

          
### Table responses:
<li> 'response_id': unique ID per set of answers of survey of one person <br> </li>
<li> 'survey_id': unique ID of the interest survey <br> </li>
<li> 'page_id': unique ID of interest page <br> </li>
<li> 'question_id': unique ID per question of survey <br> </li>
<li> 'question_label': label of question <br> </li>
<li> 'item_id': unique ID per item to evaluate/rating question of survey <br> </li>
<li> 'item_label': label of item to evaluate/rating question <br> </li>
<li> 'answer': answer of question of interest <br> </li>
<li> 'total_time': total time in seconds which the respondant spent on the survey <br> </li>
<li> 'date created': date of creation of set of answers <br> </li>
<li> 'date modified': last moment which the set of answers was modified <br> </li>

## PS:
<li> When 'item_id' and 'item_label' = Not apply is because this question doesn't have item to evaluate/rating <br> </li>
<li> When 'answer' = Sensitive data is because this answer is the CPF of person respondent <br> </li>

## Running
```
python main.py
```
