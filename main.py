"""
API Paths:
/api/personalized_learning_plans
/api/grading_assignments/generator
/api/grading_assignments/grading_in_app
/api/grading_assignments/exteranl_grading
/api/educational_material_builder/worksheet
/api/educational_material_builder/MultipleChoiceAssessments
/api/educational_material_builder/TextSummarizer
/api/educational_material_builder/MathWordProblems
/api/educational_material_builder/SyllabusGeneration
/api/educational_material_builder/SongWriter
/api/personal_tutor
/api/lesson_plan_builder
/api/essay_help
/api/book_reading_list
/api/creative_stories

, dependencies=[Depends(api_key_auth)]
"""
import os
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from typing import Union
from PIL import Image
from pydantic import BaseModel, Field
from tempfile import NamedTemporaryFile
# from misc.openai_utils import format_result
from misc.utils import fetch_personalized_learning_plans
from misc.utils import fetch_grading_assignments_generator
from misc.utils import fetch_grading_assignments_in_app
from misc.utils import fetch_external_grading_assignments
from misc.utils import fetch_educational_material_builder_worksheets
from misc.utils import fetch_educational_material_builder_MultipleChoiceAssessments
from misc.utils import fetch_educational_material_builder_TextSummarizer
from misc.utils import fetch_educational_material_builder_MathWordProblems
from misc.utils import fetch_educational_material_builder_SyllabusGeneration
from misc.utils import fetch_educational_material_builder_SongWriter
from misc.utils import fetch_personal_tutor_chat_prompt
from misc.utils import fetch_lesson_plan_builder
from misc.utils import fetch_essay_help
from misc.utils import fetch_book_reading_list
from misc.utils import fetch_creative_stories

from openai_api.openai_api import OpenaiAPI
from data_models.models import *
from misc.utils import content_process

from misc.utils import fetch_course_design_prompt
from misc.utils import fetch_research_help_prompt
from misc.utils import fetch_iep_generator
from misc.utils import fetch_essay_grading_prompt
from misc.utils import fetch_practice_test_prompt
from misc.utils import fetch_compose_email_prompt
from misc.utils import fetch_reply_email_prompt
from misc.utils import fetch_quiz_exam
from misc.utils import fetch_study_note_propmt
from misc.utils import fetch_script_for_lecture_prompt
from misc.utils import fetch_rubric_generator

from misc.utils import fetch_long_form_prompt
from docx import Document
from pypdf import PdfReader
from io import BytesIO

app = FastAPI()
openai_api = OpenaiAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json

import re
def get_json(text):
    json_match = re.search(r"```json\n(.*)\n```", text, re.DOTALL)
    return json_match.group(1) if json_match else None


def format_result(answer, json_format):
    prompt = f"""Your task is to convert the String into a valid JSON format and the format for the JSON would be given. Make sure if the given String is already in the JSON format give me back the same else convert it in valid JSON Format and also never mention any other details for example like this "Below is your string converted into a JSON format", etc or similar in the response I would require just the JSON Object in response. \n\nJSON FORMAT:{json_format}\n\n\n String: {answer} \n\n Make sure that the output/resposne should have the content of the string only not to change while changing ihe response. OUTPUT JSON OBJECT:"""
    result = openai_api.get_completion(prompt=prompt)
    if "json" in result:
        result = get_json(result)
    else: 
        result
    return result

def jsonify_text(text):
    # Remove newline characters and unnecessary backslashes
    cleaned_text = text.replace('\n', '').replace('\"', '""')
    cleaned_text = cleaned_text.replace('""','').replace("  "," ")
    # # Parse the string as JSON
    # try:
    #     json_data = json.loads(cleaned_text)
    #     return json_data
    # except json.JSONDecodeError as e:
    #     return f"Error parsing JSON: {e}"

    return cleaned_text

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

def get_docx_content(file):
    document = Document(file)

    return '\n'.join([p.text for p in document.paragraphs])

def get_pdf_content(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

async def get_file_content(file):
    content = await file.read()
    file_like = BytesIO(content)

    if file.filename.endswith("docx"):
        return get_docx_content(file_like)
    elif file.filename.endswith("pdf"):
        return get_pdf_content(file_like)
    elif file.filename.endswith("txt"):
        return content
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/api/personalized_learning_plans')
async def personalized_learning_plans(data:PersonalizedLearningPlan, max_retries: int = 3): 
    attempt_count = 0
    
    while attempt_count < max_retries:
        try:
            prompt = fetch_personalized_learning_plans(data.name, data.grade, data.learning_style, data.preferences, data.short_term, data.long_term, data.subject, data.time_availability, data.type_of_assessment)
            
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/api/grading_assignments/generator")                                      #gradeing assignments
async def grading_assignments_generator(data:GradingAssignmentsGenerator, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try:
            prompt =  fetch_grading_assignments_generator(data.topic, data.sub_topic, data.level, data.grade, data.subject, data.due_date, data.assignments_instructions, data.attachments, data.learning_objectives, data.assessment_type, data.time_limit)        
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)
            
@app.post("/api/grading_assignments/grading_in_app")                                      #gradeing assignments
async def grading_assignments_in_app(data: GradingAssignments_in_app, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try:
            prompt =  fetch_grading_assignments_in_app(data.contents_problem, data.contents_answer, data.tone, data.rubric_criteria, data.max_point)        
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/api/grading_assignments/external_grading")
async def upload_file(
    file: UploadFile
):
    max_retries = 3
    attempt_count = 0
    content = await get_file_content(file)
    
    while attempt_count < max_retries:
        try:
            prompt =  fetch_external_grading_assignments(content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)
    
    
    
    
# Run the FastAPI server using: uvicorn filename:app --reload


@app.post("/api/educational_material_builder/worksheet")
async def educational_material_builder_worksheets(
    grade_level: str,
    content: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    file_content = await get_file_content(file) if file else None
    
    while attempt_count < max_retries:
        try:         
            prompt = fetch_educational_material_builder_worksheets(grade_level, content, file_content)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)  
            
@app.post("/api/educational_material_builder/multiple_choice_assessments")
async def educational_material_builder_multiple_choice(
    grade_level: str,
    number_of_questions: int,
    content: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    
    file_content = await get_file_content(file) if file else None
    
    while attempt_count < max_retries:
        try: 
            prompt = fetch_educational_material_builder_MultipleChoiceAssessments(grade_level, number_of_questions, content, file_content)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)  
            
@app.post("/api/educational_material_builder/TextSummarizer")
async def educational_material_builder_multiple_choice(
    length_of_summary: str,  # i.e. 2 paragraphs, 5 pages, 200 words
    content: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    file_content = await get_file_content(file) if file else None
    
    while attempt_count < max_retries:
        try: 
            prompt = fetch_educational_material_builder_TextSummarizer(content, file_content, length_of_summary)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 
            
@app.post("/api/educational_material_builder/MathWordProblems")
async def educational_material_builder_multiple_choice(data: EducationalMaterial_mathwordproblems, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_educational_material_builder_MathWordProblems(data.grade_level, data.number_questions, data.mathstandard_objective_topic, data.story_topic)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 

@app.post("/api/educational_material_builder/SyllabusGeneration")
async def educational_material_builder_multiple_choice(data: EducationalMaterial_SyllabusGeneration, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_educational_material_builder_SyllabusGeneration(data.grade_level, data.subject, data.course_description, data.course_objectives, data.required_materials, data.grading_policy, data.ClassPolicies_expectations, data.CourseOutline_whatiscovered, data.addtional_customization)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 

@app.post("/api/educational_material_builder/SongWriter")
async def SongWriter(data: EducationalMaterial_SongWriter, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_educational_material_builder_SongWriter(data.topic, data.details, data.artist_title)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 

@app.post("/api/personal_tutor")
async def personal_tutor_chat(data: PersonalTutorChat):
    attempt_count = 0
    max_retries = 3
    
    while attempt_count < max_retries:
        try: 
            prompt = fetch_personal_tutor_chat_prompt(data.grade, data.preference, data.subject_or_topic, data.objective, data.questions)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 
    
@app.post("/api/lesson_plan_builder")
async def lesson_plan(
    topic:str,
    objective:str, 
    materials_needed:str,
    teaching_methodology:str,
    standards:str,
    learning_disabilities:str=None,
    assessment_methods:str=None,
    engagement_strategies:str=None
):
    max_retries = 3
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_lesson_plan_builder(topic, objective, materials_needed, teaching_methodology, standards, learning_disabilities, assessment_methods, engagement_strategies)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 

@app.post("/api/essay_help")
async def essay_help(
    subject: str,
    title: str,
    additional_info: str,
    essay: str = None,
    upload: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    upload_content = await get_file_content(upload) if upload else None
    
    while attempt_count < max_retries:
        try: 
            prompt = fetch_essay_help(subject, title, additional_info, essay, upload_content)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 
            
@app.post("/api/book_reading_list")
async def book_list_suggestion(data: BookListSuggestions, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_book_reading_list(data.reading_history, data.grade, data.preference, data.favourite_book, data.number_of_suggestions, data.Include_log_reading)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 
                
@app.post("/api/creative_stories")
async def creative_stories(data: CreativeStories, max_retries: int = 3):
    attempt_count = 0
    while attempt_count < max_retries:
        try: 
            prompt = fetch_creative_stories(data.topic, data.genre, data.setting, data.plot_points, data.conflict_challenge, data.tone_mood, data.themes, data.narrative_style, data.length, data.specific_details, data.language)
          
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400) 


@app.post("/api/long-form")
async def long_form(subject: str,
                    topics: str,
                    instructions: str = ""):
    attempt_count = 0
    max_retries = 3
    while attempt_count < max_retries:
        try:
            prompt = fetch_long_form_prompt(subject, topics, instructions)
            is_flagged, moderation = openai_api.get_moderation(
                f"{subject}, {topics}, {instructions}")
            
            # response = openai_api.get_completion(prompt=prompt     

            # formatted_final_output= format_result(response,json_format)
            if not is_flagged:
                result_dict = content_process(prompt)
                    
                return JSONResponse(content={"result": result_dict})
            else:
                return JSONResponse(content={"result": "sensitive input"}, status_code=400)

            
        except Exception as e:
                    attempt_count += 1
                    if attempt_count >= max_retries:
                        return JSONResponse(content={"error": str(e)}, status_code=400)
    # try:
    #     prompt = fetch_long_form_prompt(subject, topics, instructions)
    #     is_flagged, moderation = openai_api.get_moderation(
    #         f"{subject}, {topics}, {instructions}")

    #     if not is_flagged:
    #         return JSONResponse(content={"result": openai_api.get_completion(prompt=prompt)})
    #     else:
    #         return JSONResponse(content={"result": "sensitive input"}, status_code=400)

    # except Exception as e:
    #     return JSONResponse(content={"error": str(e)}, status_code=400)


@app.post("/api/course-design")
async def course_design(data: CourseDesign):
    attempt_count = 0
    max_retries = 3

    while attempt_count < max_retries:
        try:
            prompt = fetch_course_design_prompt(
                data.description,
                data.learning_objective,
                data.problem_to_solve,
                data.target_student,
                data.dream_outcome,
                data.number_of_modules,
                data.number_of_lessons,
                data.topic_ideas,
                data.language,
                data.include_assessment,
                data.additional_criteria
            )        
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)


@app.post("/api/grade-essay")
async def essay_grading(
    rubric: str,
    grade_scale: str,
    level: str,
    type: str,
    essay_name: str,
    essay: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    file_content = await get_file_content(file) if file else None
    
    while attempt_count < max_retries:
        try:
            prompt = fetch_essay_grading_prompt(essay, rubric, grade_scale, level, type, essay_name, file_content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)


@app.get("/api/quiz_exam")
async def quiz_exam(
    subject: str, 
    grade_level: str, 
    type_of_assessment: str, 
    question_quantity: str, 
    question_types: str, 
    difficulty_level: str, 
    time_limit: str, 
    objectives: str = None, 
    standards: str = None, 
    disabilities: str = None,
    special_instructions: str = None, 
    language: str = None, 
    criteria: str = None
):
    attempt_count = 0
    max_retries = 3

    while attempt_count < max_retries:
        try:
            prompt = fetch_quiz_exam(
                subject, grade_level, type_of_assessment, question_quantity, question_types, difficulty_level, time_limit, objectives, standards, disabilities, special_instructions, language, criteria
            )
            # is_flagged, moderation = openai_api.get_moderation(
            #     f"{subject}, {topics}, {class_grade}, {difficulty}")
            
            # response = openai_api.get_completion(prompt=prompt     
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})
            
        except Exception as e:
                    attempt_count += 1
                    if attempt_count >= max_retries:
                        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.get("/api/iep_generator")
async def iep_generator(
    student_name: str, 
    age: str=None, 
    grade_level: str = None,
    learning_disabilities: str = None,
    goals: str = None,
    description_behavior_needs_strength: str = None
    ):
    attempt_count = 0
    max_retries = 3

    while attempt_count < max_retries:
        try:
            prompt = fetch_iep_generator(
                student_name, age, grade_level, learning_disabilities, goals, description_behavior_needs_strength
            )
            print(prompt)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return None


@app.get("/api/lecture-scripts")
async def lecture_scripts(
    Class: str,
    grade_level: str,
    topic: str,
    sub_topic: str,
    learning_goals: str,
    description: str,
    tone: str,
    language: str,
    additional_instructions: str = None,
):
    attempt_count = 0
    max_retries = 3

    while attempt_count < max_retries:
        try:
            prompt = fetch_script_for_lecture_prompt(Class,grade_level,topic,sub_topic,learning_goals,description,tone,language,additional_instructions)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/api/practice-test")
async def practice_test(
    subject: str,
    topic: str,
    grade: str,
    question_quantity: int,
    question_type: str, # one of [multiple choice, true or false, short answer]
    difficulty_level: str, # one of [easy, medium, hard]
    file: UploadFile = None,
):
    attempt_count = 0
    max_retries = 3
    
    file_content = await get_file_content(file) if file else None

    while attempt_count < max_retries:
        try:
            prompt = fetch_practice_test_prompt(subject,topic,grade,question_quantity,question_type,difficulty_level,file_content)
            result_dict = content_process(prompt)
            return JSONResponse(content={"result": result_dict})
            
        except Exception as e:
                    attempt_count += 1
                    if attempt_count >= max_retries:
                        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.get("/api/research-help")     #homework help
async def research_help(
    grade_level: str,
    content: str,
):
    attempt_count = 0
    max_retries = 3

    while attempt_count < max_retries:
        try:
            prompt =  fetch_research_help_prompt(grade_level, content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/api/compose-email")
async def compose_email(
    author: str,
    content: str
):
    attempt_count = 0
    max_retries = 3
    
    while attempt_count < max_retries:
        try:
            prompt = fetch_compose_email_prompt(author, content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/api/reply-email")
async def compose_email(
    author: str,
    content: str
):
    attempt_count = 0
    max_retries = 3
    
    while attempt_count < max_retries:
        try:
            prompt = fetch_reply_email_prompt(author, content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/api/study-note")
async def study_note(
    grade: str = None,
    subject: str = None,
    topic: str = None,
    keywords: str = None,
    additional_notes: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    file_content = await get_file_content(file) if file else None
    
    while attempt_count < max_retries:
        try:
            prompt = fetch_study_note_propmt(grade, subject, topic, keywords, additional_notes, file_content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)


@app.post("/api/rubric_generator")
async def rubric_generator(
    subject: str,
    topic: str,
    objective: str,
    standards: str,
    assignment_title: str,
    point_scale: str,
    assignment_description: str = None,
    additional_customization: str = None,
    file: UploadFile = None
):
    attempt_count = 0
    max_retries = 3
    file_content = await get_file_content(file) if file else None

    while attempt_count < max_retries:
        try:
            prompt = fetch_rubric_generator(subject, topic, objective, standards, assignment_title,
                                            assignment_description, additional_customization, point_scale, file_content)
            result_dict = content_process(prompt)

            # formatted_final_output= format_result(response,json_format)
            return JSONResponse(content={"result": result_dict})

        except Exception as e:
            attempt_count += 1
            if attempt_count >= max_retries:
                return JSONResponse(content={"error": str(e)}, status_code=400)
