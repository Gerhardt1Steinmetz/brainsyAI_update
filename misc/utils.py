import json
from openai_api.openai_api import OpenaiAPI
from openai_api.openai_api import get_json
from fastapi import UploadFile, File, Form
from typing import Union

openai_api = OpenaiAPI()

def content_process(content):
    
    response_data = openai_api.get_completion(prompt=content)
    print(response_data)
    
    result_dict = dict()
    if "json" in response_data:
        result = get_json(response_data)
        
        result_dict = json.loads(result)
        print(result_dict)
        
    else :
        result_dict = response_data
    
    return result_dict

def verify_input(input):
    if input and len(input):
        return True
    return False


def process_personalised_plan_response(response):
    response = response.strip().split('\n')
    result = {}
    current_key = ''
    for res in response:
        if not res:
            continue

        if res == 'Objective:':
            current_key = 'Objective'
            continue
        if res == 'Study Topics:':
            current_key = 'Study Topics'
            continue

        if res == 'Explore Suggestions:':
            current_key = 'Explore Suggestions'
            continue

        if res == 'Practice Questions:':
            current_key = 'Practice Questions'
            continue

        if current_key not in result:
            result[current_key] = []

        result[current_key].append(res)

    return result

def fetch_personalized_learning_plans(name, grade, learning_style, preferences, short_term, long_term, subject, time_availability, type_of_assessment):
        
    json_format = """{
        "Overview" : "",
        "Objective" : "",
        "Long-term Goals" : {
            "1" : "",
            "2" : "",
            ... ...
            },
        "Short-term Goals" : {
            "1" : "",
            "2" : "",
            ... ...
        }
        "Key Concepts" : {
            "1" : "",
            "2" : "",
            ... ...
        }
        "Assessment" : {
            "Type" : "",
            "Frequency" : ""
        }
        "Additional Links to Resources" : {
            "1" : "",
            "2" : "",
            ... ...
        }
        "Links to Free Resources" : {
            "1" : "",
            "2" : "",
            ... ...
        }
        "Monthly Plan" : {
            "Week 1":"",
                "Day 1" : {
                    "1":"",
                    "2":"",
                    ... ...
                }
                "Day 2" : {
                    "1":""
                    "2":""
                    ... ...
                }
                ... ...
            "Week 2":"",
                "Day 1" : {
                    "1":"",
                    "2":"",
                    ... ...
                }
                "Day 2" : {
                    "1":""
                    "2":""
                    ... ...
                }
                ... ...
            ... ...
        }
        "Monitoring and Feedback" : {
            "Weekly Check-ins":{
                "1" : "",
                "2" : "",
                ... ...
            }
            "Monthly Assessments":{
                "1" : "",
                "2" : "",
                ... ...
            }
        }
        }"""
        
    prompt = f"""
    I need a detailed personalized learning plan of {subject} for {name} in {grade} grade. He likes {learning_style} method for studying and prefers {preferences}. Now his short term goal is to {short_term} and long term goal is to {long_term}. His time availability for studying is {time_availability}. He likes {type_of_assessment} for assessments. The plan has to include detail overview and objective of the plan, detailed short term and long term goals, key concepts of the plan, recommendation of additional valuable resources and free resources, effective monthly and daily schedule and monitoring and feedback for {name}'s study, notes for parents and teachers in detail. The output result has to be json format like below. \n\n{json_format}\n\n Please give me a detailed and useful and helpful learning plan for {name}.    
    """
        
    return prompt

def fetch_grading_assignments_generator(topic, sub_topic, level, grade, subject, due_date, assignment_instructions, attachments, learning_objectives, assessment_type, time_limit):
    json_format = """{
        "Title" : "",
            "grade_level":"",
            "Topic":"",
            "Submission Deadline":"",
            "Time Limit":"",
            "Type":"",
            "Aim":""
        "Assignments Instructions":"",
            "Instructions":{
                "1":"",
                "2":"",
                ... ...
            }
        "Problems":{
            "Problem1":"",
            "Problem2":"",
            ... ... 
        } 
        "Answers":{
            "Problem1":"",
            "Problem2":"",
            ... ...
        }
        "Advice":""    
    }"""
    
    prompt = f"""
    I need assignments to evaluate the {level} student's studying progress about {sub_topic} in the topic {topic} of {subject}. The student's grade is {grade} grade. For assignments, please give {assignment_instructions} as assignment instructions. The aim of assignments is to achieve goals of {learning_objectives}. The type of assignments is {assessment_type}. Combine several types of problems for assignments. If you need attachments, please refer to {attachments} as attachments. Problems are not so easy and have to include 25% of difficult problems. For this, you can add some image files. Also, adjust correctly the difficulty of problems according to the level of students. The assignment has to be submitted in until {due_date}. The time limit of assignment has to be {time_limit}. Put the correct answers. At the end, put friendly instructions for students to solve the assignments. Output result has to be following json format. \n\n{json_format}\n\n Please give me helpful assignments for students' study considering above all.
    """
    return prompt

def fetch_grading_assignments_in_app(contents_problem, contents_answer, tone, rubric_criteria, max_point):
    json_format = """{
        "grade" : "",
        "feedback" : "",
        "field" : ""        
    }"""
    
    contents_problem = contents_problem.replace('"', r'\"')
    
    prompt = f"""
    Now you are a strict teacher to grade student's answer to assignments. The problem is this: \n {contents_problem} \n The answer of student is this: \n {contents_answer} \n You have to grade this with the following criteria. \n {rubric_criteria} \n The maximum points of this test is {max_point}. Grade correctly and provide {tone} feedback for students. Also, you have to provide the detail studying field of the problem for further reference to focus. Output Result has to be json format like below. \n\n {json_format} \n\n 
    """
    print(prompt)
    return prompt

def fetch_external_grading_assignments(file_content):
    json_format = """{
        question1: {
            type: "...", // one of [fill_blank, multiple_choice, true_false, short_answer]
            question: "...",
            options: "...", // only for the multiple_choice question
            answer: "..."
        },
        question2: {
            ...
        },
        ...
    }"""
    
    
    prompt = f"""
        Below content contains some questions:
        {file_content}
        
        Please reshape the content and make JSON like below.
        ```json
            {json_format}
        ```
    """
    
    return prompt

def fetch_educational_material_builder_worksheets(grade_level, content, file_content):
    json_object = """{
        "Word Bank" : ""
        "Multiple Choice Questions" : "",
            "1. xxx" : {
                "A" : "",
                "B" : "",
                ... ...
            }
            "2. xxx" : {
                "A" : "",
                "B" : "",
                ... ...
            }
            ... ...
        "Open Ended Questions" : "",
            "1" : "",
            "2" : "",
            ... ...
        "Answer Key" : ""
    }
    """
    prompt = f"""
        I need useful and helpful worksheets to get perfect educational material.
        The level of educational material is {grade_level} grade level.
        The contents is related with below. \n\n{content} {file_content}\n\n
        Put answer keys to the generated questions. The output result has to be json format like below.
        ```json
            {json_object}
        ```
    """
    return prompt

def fetch_educational_material_builder_MultipleChoiceAssessments(grade_level, number_of_questions, content, file_content):
    json_format = """
        {
            questions: {
                "1. xxxx": {
                    "A": "...",
                    "B": "...",
                }
                ...
            }
            answerKeys: {}
        }
    """
    
    prompt = f"""
        Please generate {number_of_questions} multi-choice questions for {grade_level} grade students.
        The questions should be based on below content: \n {content} {file_content} \n\n
        Output should be in JSON format given below:
        ```json
            {json_format}
        ```
    """

    return prompt

def fetch_educational_material_builder_TextSummarizer(content, file_content, length_of_summary):
    json_format = """{
        summarized: "..."
    }"""
        
    prompt = f"""
        Please summarize the below content and make it {length_of_summary}.
        {content} {file_content}\n\n
        The output should be in JSON format.
        ```json
            {json_format}
        ```
    """
    return prompt

def fetch_educational_material_builder_MathWordProblems(grade_level, number_questions, mathsstandard_objective_topic, story_topic):
    json_format = """{
        "Title" : "Fun with xxx and xxx",
        "1. xxx" : {
            "Problem 1" : "",
            "Answer" : ""
            },
        "2. xxx" : {
            "Problem 2" : "",
            "Answer" : ""
            },
        ... ...
        }"""
        
    prompt = f"""
    I need Math story word problems for {grade_level} students. The number of questions to generate is {number_questions}. Maths standards or objective or topic of Maths story word problems are as follows: \n{mathsstandard_objective_topic}\n The story topic is {story_topic}. Title has to be reflect the maths topic and story topic. In front of every problem, put the description of every problem reflecting the idea of problems. Also put the correct answers. Output result has to be following json format: \n\n {json_format} \n\n 
    """
    return prompt

def fetch_educational_material_builder_SyllabusGeneration(grade_level, subject, course_description, course_objectives, required_materials, grading_policy, ClassPolicies_expectations, CourseOutline_whatiscovered, addtional_customization):
    json_format = """{
        "Cousre Syllabus" : "",
        "Course Description" : "",
        "Course Objectives" : {
            "1" : ""
            "2" : "",
            ... ...
            },
        "Required Materials" : "",
        "Grading Policy" : "",
        "Course Class Policies and Expectations" : "",
        "Course Content" : {
            "1" : "",
            "2" : "",
            ... ...
            },
        "Assessment Rubric" : {
            "" : {
                "Level1(developing)" : "",
                "Level2(Proficient)" : ""
                ... ...
            }
            "" : {
                "Level1(developing)" : "",
                "Level2(Proficient)" : ""
                ... ...
            }
            ... ...
        }
        }"""
        
    prompt = f"""
    I need smart syllabus for {grade_level} student about {subject}. The topic of syllabus is {course_description}. The syllabus contains {course_objectives}. The required materials are {required_materials}. The grading policy for this syllabus is {grading_policy}. Class policies or expectations are {ClassPolicies_expectations}. Course Outline or what is covered is {CourseOutline_whatiscovered}. Addtional customization is {addtional_customization}. Output result has to be following json format: \n\n {json_format} \n\n Give me helpful, useful and smart syllabus for education. Please explain course objectives and course descriptions much more detail.
    """
    return prompt

def fetch_educational_material_builder_SongWriter(topic, details, artist_title):
    
    prompt = f"""
    Generate a song of {topic}. The song has to include following details: \n\n {details} \n\n The artist name and the song title are as follows: \n\n {artist_title} \n\n Give me a perfect and awesome song!
    """
    return prompt

def fetch_lesson_plan_builder(topic, objective, materials_needed, teaching_methodology, standards, learning_disabilities, assessment_methods, engagement_strategies):
    json_format = """{
        "Objective" : "",
        "Assessment" : "",
        "Key Points" : "",
        "Opening" : "",
        "Guided Practice" : "",
        "Independent Practice" : "",
        "Closing" : "",
        "Extension Activity" : "",
        "Homework" : "",
        "Standards Addressed" : "", 
        }"""

    prompt = f"""
    Generate detailed, useful, helpful and perfect lesson plan of {topic}. The learning objective that students have to master from the lesson is {objective}. Materials needed for the lecture are {materials_needed}. The teaching methodology used in the lecture is {teaching_methodology}. Lesson plan has to be satisfied with {standards}. Consider the student has {learning_disabilities} as learning disabilities. The assessment methods are {assessment_methods}. The engagement strategies in the lesson are {engagement_strategies}. The contents of lesson plan has to be included key points, how to open the lesson, guided practice, independent practice, how to close the lesson, extension activity, homework and standards addressed. All the sections of the lesson plan has to be detailed, rich, helpful and useful for teachers and students. Output result has to be following json format: \n\n {json_format} \n\n Please give me a detailed, rich, useful and helpful lesson plan.
    """
    
    return prompt


def fetch_essay_help(subject, title, additional_info, essay, upload_content):
    json_format = """{
        paragraph_1: {
            content: "...",
            feedback: {
                grammar: "..",  // optional if paragraph has no grammar issue
                content_organization: "..", // optional
                use_of_evidence: "..", // optional
                clarity: "..", // optional
                ...
            }
        }
        ...
    }"""
            
    prompt = f"""
        I have written an essay on {subject}. The title is {title}.
        Here are some additional info: {additional_info}
        And below is the essay:
        {essay}
        {upload_content}
        
        ---
        Please give me some feedback on this essay, like what is mistake and how I can improve
        For each paragraph, give me feedback in terms of grammar, clarity, content organization, use of evidence etc.
        If there's no issue in these criteria, simply skip that one.
        Output should be in the following JSON format.
        ```json
            {json_format}
        ```
    """
    return prompt

def fetch_personal_tutor_chat_prompt(grade, preference, subject_or_topic, objective, questions):
    json_format = """
        answer: "..."
    """
    
    prompt = f"""
        Help {grade} grade student to solve his questions about {subject_or_topic}.
        His preference is {preference} and his objective is {objective}.
        And he wants to know about {questions}.
        Note: please don't give him direct answer, but give him some steps to solve the answer.
        The answer should be in JSON format given below.
        ```json
            {json_format}
        ```
    """
    
    return prompt

def fetch_book_reading_list(reading_history, grade, preference, favourite_book, suggest_number, Included_log_reading):
    json_format = """{
        "Book 1":{
            "title":"",
            "summary":"",
            "URL":"",  
            ... ...          
        },
        "Book 2":{
            "title":"",
            "summary":"",
            "URL":"",     
            ... ...       
        },
        ... ...
        }"""
        
    prompt = f"""
    Recommendate the {suggest_number} books for {grade} student. This student prefer {preference} for book reading and his favourite book is {favourite_book}.  If {Included_log_reading} is yes, consider student's reading history like below: \n\n{reading_history}\n\n Recommendation has to include detail info of books including title, summary, page counts, author and URL. Output result has to be following json format like below: \n\n {json_format} \n\n Please provide useful and helpful reading books!
    """
    return prompt

def fetch_creative_stories(topic, genre, setting, plot_points, conflict_challenge, tone_mood, themes, narrative_style, length, specific_details, language):
    json_format = """{
        "Title" : "",
        "Setting" : "",
        "Plot Points" : {
            "1" : "",
            "2" : "",
            ... ...
        },
        "Conflict or Challenge" : "",
        "Tone or Mood" : "",
        "Themes" : {
            "1" : "",
            "2" : "",
            ... ...
        },
        "Narrative Style" : "",
        "Length" : "",
        "Story" : "",
        "Conclusion" : ""
        }"""
        
    prompt = f"""
    Generate a creative {genre} story on topic of {topic} in {language}. The setting of this story is {setting} and plot points which are occured in the story are as follows. \n\n {plot_points} \n\n The characters face following conflict or challenges. \n\n conflict or challenges: {conflict_challenge}. \n\n It is important to keep following tone and mood throughout the story. \n\n tone or mood: {tone_mood} \n\n The themes of the story is as follows. \n\n Themes:{themes} \n\n  The narrative style of the story is {narrative_style}. The story length is {length} level. I want to include {specific_details} in story. Output result has to be following json format: \n\n {json_format} \n\n The contents of story has to be detailed, rich and descriptive so that we publish immediately for audiences.Tell us a truly creative and rich story for your audience.
    """
    return prompt



def fetch_long_form_prompt(subject, topics, instructions):
    prompt = f'Write detailed content on {subject} subject on below topics in detail.'
    if instructions and len(instructions):
        prompt += f'\n{instructions}'
    prompt += f'\nTopics: {topics}'
    prompt += '\n\n###\n\n'

    return prompt


def fetch_course_design_prompt(description,learning_objective,problem_to_solve,target_student,dream_outcome,number_of_modules,number_of_lessons,topic_ideas,language,include_assessment,additional_criteria):
    json_format = """{
        title: "",
        modules: [
            {
                module_name: "1. ...",
                introduction: "...",
                lessons: [
                    {
                        lesson_name: "...",
                        overview: "..",
                        key_concepts: "..",
                        interactive_elements: ".."
                    },
                    ...
                ]
            },
            ...
        ],
        assignments: [
            {
                assignment_name: "..",
                description: "..",
                instruction: "..",
                due_date: "week ..."    // i.e. "week 1" or "week 2" or basically any "week (number)"
            },
            {
                assignment_name: "..",
                description: "..",
                instruction: "..",
                due_date: "week ..."
            },
            ...
        ]
        additional_resources: "...",    //Some resources useful for this course
        course_schedule: "...", //weekly schedule for this course;
        assessments: "...", //possible assessments for this course;
        grading_criteria: "...",    //Weight for each assessments;
    }"""
    
    prompt = f"Please write a course design for {description}.\n The objective of this learning course is to {learning_objective}.\n\
        The problem to solve is {problem_to_solve}.\n This course is targeted for {target_student}.\n The dream outcome would be {dream_outcome}\n.\
        There are {number_of_modules} modules, and inside each module has {number_of_lessons} lessons. The brief description for each module is {topic_ideas}.\n\
        The course should be in {language}.\nThis course will {'' if include_assessment else 'NOT'} include assessments/quizzes.\
        And here are some more info about this course: {additional_criteria}\n\
        The output should be in the following JSON format: {json_format}"
    return prompt


def fetch_essay_grading_prompt(essay, rubric, grade_scale, level, type, essay_name, file_content):
    json_format = """
        {
            "EssayGradingOutput":{
                "OverallScore": ".../100",
                "Sections": {
                    "Content":{
                        "Score":".../30",
                        "Feedback":""
                    },
                    "Organization": {
                        "Score":".../25",
                        "Feedback":""
                    },
                    "Language":{
                        "Score":".../25",
                        "Feedback":"",
                    },
                    "Creativity":{
                        "Score":".../20",
                        "Feedback":""
                    },
                    "AdditionalComments": [
                        "",
                        "",
                        "",
                        ...
                    ],
                    "DetailedFeedback":"...",
                    "AdjustedGrade": {
                        "OriginalScore": "",
                        "AdditionalScore": "",
                        "Reason": ""
                    },
                    "FinalGrade": ".../100"
                }
            }
        }
    """
    prompt = f"Grade an essay based on the following information.\
        The title of the essay is {essay_name}. The type of this essay is {type}\
        level: {level}, rubric: {rubric}, grade_scale: {grade_scale}\
        And below is the actual essay:\
        {essay}\n{file_content}\n\n\
        Also make sure that the output is in JSON format whose structure is as follow:\
        ```json\
            {json_format}\
        ```\
        "
    return prompt


def fetch_quiz_exam(
    subject, grade_level, type_of_assessment, question_quantity, question_types, difficulty_level, time_limit, objectives, standards, disabilities, special_instructions, language, criteria
):
    json_format = """{
        "Problem 1" : {
            "Q1" : "",
            "Ans" : ""
            },
        "Problem 2" : {
            "Q2" : "",
            "Ans" : ""
            },
        ... ...
        }"""
    json_multi_choice = """{
        "Problem 1" : {
            "Q1": "",
                "options" : "",
            "Ans": ""
            },
        "Problem 2" : {
            "Q2": "",
                "options" : "",
            "Ans": ""
            },
        ... ...
        }
        }"""
    json_T_F = """{
        "Problem 1" :{
            "Q1": "",
                "Ans" : ""
        },
        "Problem 2" :{
            "Q2": "",
                "Ans" : ""
        },
        ... ...
    }
    """
    prompt = f"""
    Generate {type_of_assessment} of {subject} for {grade_level} students in {language}. The difficulty level of the {type_of_assessment} is {difficulty_level}. The number of questions is {question_quantity}. You have to provide exact {question_types} types of questions for all the problems. If the type is Multiple choice, the format of problems has to be following json format: \n\n {json_multi_choice} \n If the type is True/False or T/F, the format of problems has to be following json format: \n\n {json_T_F} \n\n If the question type is short answer, you have to provide problems that requires short answers. If the question type is essay, you have to provide problems that requires essay-format answers. What is covered the {type_of_assessment} is {objectives}. The contents are satisfied with {standards} and the limited time of {type_of_assessment} is {time_limit}. Consider this student has {disabilities}. The special instruction for this {type_of_assessment} is {special_instructions}. The criteria of this {type_of_assessment} is {criteria}. Put the correct answers for each problem after the questions. Output has to be following json format: \n\n {json_format} \n\n
    """

    return prompt

def fetch_iep_generator(student_name, age, grade_level, learning_disabilities, goals, description_behavior_needs_strength):
    json_format = """
        {
            "Student IEP Draft" : "Review closely before implementation"
            "Present Levels for Performance: "",
            "Student Needs and Impact of Disability": "",
            "Goals and Objectives":{
                "Measurable Goal" : "",
                    "Objective" : "",
                "Measurable Goal" : "",
                    "Objective" : "",
                ... ...
                "Accomodations and Modifications" : {
                    "1" : "",
                    "2" : "",
                    ... ...
                }
    """
    
    prompt = f"I need perfect individual education plan generator for {age} year old {student_name}. His grade level is {grade_level} and he has {learning_disabilities} as learning\
        disabilities. His goal which is covered this plan is {goals}. The description of {student_name}'s behaviors, needs and strengths are as follows: \n\n {description_behavior_needs_strength}\n\n \
        The output should be in JSON format given below. Please provide me with the smart and detailed IEP for {student_name} in detail.\
        ```json\n{json_format}\n```\
    "
    return prompt

def fetch_script_for_lecture_prompt(Class,grade_level,topic,sub_topic,learning_goals,description,tone,language,additional_instructions):
    json_format = """
        {
            introduction: {
                greeting: "",
                overview: "",
                objectives: "",
                ...
            },
            background_information: {
                historical_context: "",
                definitions: "",
                ...
            },
            ...
        }
    """
    prompt = f"""Compose a detail and rich lecture script on {sub_topic} of {topic} for students in grade {grade_level}. The class is {Class} class.\
        The script should begin by presenting detailed learning objectives, which are {learning_goals},\
        detailing the specific skills and knowledge that the students are expected to acquire by the end of the lecture. The contents of the lecture has to include detail and rich theoretical knowledge, formula, application and practical knowledge with detail and rich explanation.\
        It's important to keep the tone {tone} throughout. Here is an description for this lecture script: {description} \
        The lecture should be conducted in {language}. Additionally, incorporate any specific details or methodologies outlined in {additional_instructions} to enhance the lecture's effectiveness and relevance to the audience.\
        This lecture script will be composed of many different sections including but not limited to detailed introduction, detailed background information, detailed and rich key concepts, detailed and rich analysis, detailed real-world applications and conclusion.\
        All the sections of this lecture script has to be much more detailed with detailed and rich explanation since this is the detailed and rich script for the lecture.\
        The amount of script is enough to say for 2 hour without break. The sections which have principal and theoretical contents has to be rich and detail. Please give me in JSON format given below.\
        \n\n{json_format}\n\n Please give me detailed and rich lecture script.
    """

    return prompt

def fetch_practice_test_prompt(
    subject,topic,grade,question_quantity,question_type,difficulty_level,file_content
):
    overall_json_format = """
        [
            Question1,
            Question2,
            ...
        ]
    """
    question_short_answer_format = """
        {
            description: "...",
            answer: "..."
        }
    """
    question_multiple_choice_format = """
        {
            description: "...",
            // choice doesn't need to be a single number. it also can be expression or sentence. please be creative.
            choices: [
                "1.xxx",
                "2.xxx",
                ...
            ]
            correct_choice_index: "..."
        }
    """
    prompt = f"give me {question_quantity} questions on {subject}. the topic is {topic}.\
        question type is {question_type}. These questions are for {grade}. The difficulty level of the questions are {difficulty_level}.\
        And below is some of the knowledgebase the students have studied: {file_content}\
        Please give me in JSON format given below.\
        ```json\n{overall_json_format}\n```\n\n\n\
        if the question type is [short answer] or [fill in the blank] or [true or false], then each question can be expressed like this: {question_short_answer_format}\
        if the question type is [multiple choice], then each question can be expressed like this: {question_multiple_choice_format}\
    "

    return prompt

def fetch_research_help_prompt(grade_level, content):
    json_format = """
        {
            books: [
                {
                    title: "",
                    author: "",
                    url: ""
                },
                ...
            ],
            websites: [
                {
                    title: "",
                    url: ""
                },
                ..
            ],
            videos: [
                {
                    title: "",
                    url: ""
                },
                ...
            ]
        }
    """
    prompt = f"Please do some research on {content}. The research result should be ideal for {grade_level} students.\
        The research result should be from across the web and can contain sections but not limited to Books, Websites and Videos.\
        Please give me in JSON format given below.\
        ```json\
            {json_format}\
        ```\
    "
    print(prompt)
    return prompt

def fetch_compose_email_prompt(author, content):
    prompt = f"{author} is writing an email about {content}. please help him complete the email professionally. Just give me the email as the output, no other explanations or sth."
    return prompt

def fetch_reply_email_prompt(author, content):
    prompt = f"""{author} has sent an email and here is the content: {content}.\n
        Please write reply email to this email.
        Just give me the email as the output, no other explanations or sth.
    """
    return prompt

def fetch_study_note_propmt(grade, subject, topic, keywords, additional_notes, file_content):
    json_format = """{
        "Introduction" : "",
        "Section 1" : ""
            "" : {
                "":"",
                "":"",
                ... ...
                },
        "Section 2" : ""
            "" : {
                "":"",
                "":"",
                ... ...
                },
        ... ...
        "Conclusion" : "",
        "Study Tips" :{
            "1":"",
            "2":"",
            ... ...
        },
        "Additional Resources":{
            "":"",
            "":"",
            ... ...
        }
        }
    """
    prompt = f"Please give me helpful study notes for {grade} grade students for {subject}.\
        What is coverd to the notes is {topic} and keywords of study notes are {keywords}.\
        Here are idea of additional notes: {additional_notes}\n\n\n\
        Here are additional attachment content to be considered: {file_content}\n\n\
        The output should be in following JSON format:\
        ```json\n{json_format}\n```\
        Please give me useful and helpful and rich study notes for students.\
    "
    return prompt

def fetch_rubric_generator(subject, topic, objective, standards, assignment_title, assignment_description, additional_customization, point_scale, file_content):
    json_format = """{
        "Title" : "",
            "Criteria 1" : ""
                ... ...
                "Exceeds Expectations(3)" : "",
                "Meets Expectations(2)" : "",
                "Needs Improvement(1)" : "",
            "Criteria 2" : ""
                ... ...
                "Exceeds Expectations(3)" : "",
                "Meets Expectations(2)" : "",
                "Needs Improvement(1)" : "",
            ... ...
    }"""

    prompt = f"""
        Generate detailed, clear and perfect rubric for {topic} of {subject}. rubric has to include {objective} and is satisfied with {standards}. The assignment title for grading is {assignment_title} and the description of assignment is as follows: \n\n {assignment_description} \n\n Additional customization for rubric is as follows: \n\n {additional_customization} \n\n Point scale for rubric is {point_scale}. You have to refer following file contents from the attached files like below. file contents: \n\n {file_content} \n\n Output result has to be following json format: \n\n {json_format} \n\n Please generate perfect rubric with clear criteria and clear grading level.
     """

    return prompt
