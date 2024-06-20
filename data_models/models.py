"""
/api/curriculum-adaption
/api/essay-grading
/api/book-list-suggestions
/api/assignment-grading
/api/homework-creator
/api/reportcard-generator
/api/professional-correspondence
/api/course-design
/api/teacher-chatbot
/api/creative-stories
/api/personal-tutor-chat
/api/study-notes
/api/practice-test
/api/essay-help
"""

from typing import Annotated, Union
from pydantic import BaseModel, Field
from enum import Enum
from fastapi import UploadFile, File, Form

class RoleType(Enum):
    """
    Enum representing the type of role
    """
    TEACHER = "teacher"
    STUDENT = "student"

class PersonalizedLearningPlan(BaseModel):
    name: str = Field(default=None)
    grade: str = Field(default=None)
    learning_style: str = Field(default=None)
    preferences:str = Field()
    short_term: str = Field(default=None)
    long_term: str = Field(default=None)
    subject: str = Field(default=None)
    time_availability: str = Field(default=None)
    type_of_assessment: str = Field(default=None)
    
class GradingAssignmentsGenerator(BaseModel):
    topic : str = Field(default = None, description="Enter the main subject or theme of the assignment.")
    sub_topic : str = Field(default=None, description="Enter any sub-topics related to the main topic.")
    level : str = Field(default=None, description="Select the educational level (e.g., elementary, middle school, high school).")
    grade : str = Field(default=None, description="Select the grade level of the students.")
    subject : str = Field(default=None, description="Select the subject area (e.g., Math, Science, English).")
    due_date : str = Field(default=None, description="Set a time limit for completing the assignment (if applicable).")
    assignments_instructions : str = Field(default=None, description="Provide detailed instructions for the assignment.")
    attachments : Union[str, None] = Field(default=None, description="URL or path to attachment file (optional).")
    learning_objectives : str = Field(default=None, description="Specify the learning objectives the assignment aims to achieve.")
    assessment_type : str = Field(default=None, description="Choose the type of assessment (e.g., quiz, essay, project).")
    time_limit : str = Field(default=None, description="Set a time limit for completing the assignment (if applicable).")
#grading_criteria: Union[str, None] = Field(default=None, description="This field will allow the teacher to input the specific grading criteria they want to use for the assignment.")

class GradingAssignments_in_app(BaseModel):
    contents_problem : str = Field(default = None, description="Enter the problem to grade.")
    contents_answer : str = Field(default=None, description="Enter the answer to grade.")
    tone : Union[str, None] = Field(default=None, description="Specify the tone of feedback (optional) (e.g., funny, serious, helpful).")
    rubric_criteria : str = Field(default=None, description="This field will allow the teacher to input desired criteria")
    max_point : int = Field(default=None, description="Enter the maximum points in this test.")
    
class GradingAssignments_external(BaseModel):
    contents_problem : str = Field(default = None, description="Enter the problem to grade.")
    contents_answer : str = Field(default=None, description="Enter the answer to grade.")
    tone : Union[str, None] = Field(default=None, description="Specify the tone of feedback (optional) (e.g., funny, serious, helpful).")
    rubric_criteria : str = Field(default=None, description="This field will allow the teacher to input desired criteria")
    max_point : int = Field(default=None, description="Enter the maximum points in this test.")

class EducationalMaterial_worksheet(BaseModel):
    grade_level: str = Field(default=None, description="")
    standarads: Union[str, None] = Field(default=None, description="")
    language: str = Field(default="english", description="")
    topic_text: str = Field(default=None, description="")
  #  attachments : Union[UploadFile, None] = Field(default=None, description="")
  
class EducationalMaterial_multiplechoice(BaseModel):
    grade_level: str = Field(default=None, description="")
    topic_text: str = Field(default=None, description="")
    criteria: str = Field(default=None, description="")
    standarads: str = Field(default=None, description="")
    learning_diabilities: str = Field(default=None, description="")
    material_type: str = Field(default=None, description="")
    language: str = Field(default="english", description="")
    grade: str = Field(default=None, description="")
    output_quantity: str = Field(default=None, description="")
    
class EducationalMaterial_textsummarizer(BaseModel):
    grade_level: str = Field(default=None, description="")
    topic_text: str = Field(default=None, description="")
    criteria: str = Field(default=None, description="")
    standarads: str = Field(default=None, description="")
    learning_diabilities: str = Field(default=None, description="")
    material_type: str = Field(default=None, description="")
    language: str = Field(default="english", description="")
    grade: str = Field(default=None, description="")
    output_quantity: str = Field(default=None, description="")

class EducationalMaterial_mathwordproblems(BaseModel):
    grade_level: str = Field(default=None, description="")
    number_questions : int = Field(default=None, description="")
    mathstandard_objective_topic: str = Field(default=None, description="")
    story_topic: str = Field(default=None, description="")
    
class EducationalMaterial_SyllabusGeneration(BaseModel):
    grade_level: str = Field(default=None, description="")
    subject: str = Field(default=None, description="")
    course_description: str = Field(default=None, description="")
    course_objectives: str = Field(default=None, description="")
    required_materials: str = Field(default=None, description="")
    grading_policy: str = Field(default=None, description="")
    ClassPolicies_expectations: str = Field(default="english", description="")
    CourseOutline_whatiscovered: str = Field(default=None, description="")
    addtional_customization: Union[str, None] = Field(default=None, description="")

class EducationalMaterial_SongWriter(BaseModel):
    topic: str = Field(default=None, description="")
    details: str = Field(default=None, description="")
    artist_title: str = Field(default=None, description="")

class PersonalTutorChat(BaseModel):
    subject_or_topic: str = Field(default=None, description="")
    grade: str = Field(default=None, description="")
    preference: str = Field(default=None)
    objective: str = Field(default=None)
    questions:  str = Field(default= None)

class CurriculumAdaption(BaseModel):
    curriculum_name: str = Field(default=None, description="This field will allow the user to input the name of the curriculum they want to use for generating assignments.")
    grade_level: str = Field(default=None, description="This field will allow the user to input the grade level for which they want to generate assignments.")
    subject_area: str = Field(default=None, description="This field will allow the user to input the grade level for which they want to generate assignments.")
    learning_objectives: str = Field(default=None, description="This field will allow the user to input the learning objectives they want to focus on for the generated assignments.")
    previous_assignment: Union[str, None] = Field(default=None, description="This field will allow the user to input any previous assignments or assessments that have been given in the curriculum.")
    assignment_type: str = Field(default=None, description="This field will allow the user to choose the type of assignment they want to generate (e.g. quiz, essay, project, etc.).")

#parameters Added
class EssayGrading(BaseModel):
    essay: str = Field(default=None, description="This field will allow the teacher to input the essay that needs to be graded.")
    rubric : str = Field(default=None, description="This field will allow the teacher to input the rubric they want to use to grade the essay.")
    grade_scale : Union[str, None] = Field(default=None, description="This field will allow the teacher to input the specific grading criteria they want to use for the essay.")
    level: str = Field(default=None)
    type: str = Field(default=None)
    essay_name: str = Field(default=None)
    file: UploadFile


class BookListSuggestions(BaseModel): 
    reading_history: str = Field(default=None, description="This field will allow the user to input a list of books they have already read.")
    grade: str = Field(default=None)
    preference: str = Field(default=None, description="This field will allow the user to input their preferred genres, authors, and other reading preferences.")
    favourite_book: str = Field(default=None, description="This field will allow the user to input their reading level or the reading level of the books they are interested in.")
    number_of_suggestions: str = Field(default=None, description="This field will allow the user to input the reason for their reading (e.g. educational, entertainment, personal development, etc.).")
    Include_log_reading: str = Field(default=None)



class HomeworkCreator(BaseModel):
    subject: str = Field(default=None, description="The field allow the teacher to input the subject for which they want to generate homework.")
    learning_objectives: str = Field(default=None, description="This field will allow the teacher to input the learning objectives they want to assess through the assignment.")
    assignment_type: str = Field(default=None, description="This field will allow the teacher to choose the type of assignment they want to create (e.g. quiz, essay, project, etc.).")
    question_format: str = Field(default=None, description="This field will allow the teacher to choose the format of the questions (e.g. multiple-choice, short answer, essay, etc.).")
    difficulty_level: str = Field(default=None, description="This field will allow the teacher to choose the difficulty level of the questions.")
    time_limit: str = Field(default=None, description="This field will allow the teacher to set a time limit for completing the assignment.")
    grade_level :str = Field(default=None)
    no_of_questions:str = Field(default= None)
    standards: str = Field(default=None)
    language_preferences: str = Field(default="English")
    grading_criteria:str = Field(default= None)
    accessibility_features : str = Field(default= None)

class ReportCardGenerator(BaseModel):
    student_name : str = Field(default=None)
    grade_level : str = Field(default=None)
    semester: str = Field(default=None)
    subjects: str = Field(default=None)
    teacher_comments: str = Field(default=None)
    attendance_record: str = Field(default=None)
    extra_curricular_activities: str = Field(default=None)
    behavior: str = Field(default=None)
    additional_notes: str = Field(default=None)

class TranscriptGenerator(BaseModel):
    student_name : str = Field(default=None)
    student_id : str = Field(default=None)
    graduation_year: str = Field(default=None)
    course_name: str = Field(default=None)
    gpa_calculation: str = Field(default=None)
    teacher_comments: str = Field(default=None)
    extra_curricular_activities: str = Field(default=None)
    additional_notes: str = Field(default=None)


class ProfessionalCorrespondence(BaseModel):
    recipient_information: str = Field(default=None, description="This field will allow the teacher to input the recipient's name, email address, and other relevant information.")
    purpose_of_communication: str = Field(default=None, description="This field will allow the teacher to choose the purpose of their communication (e.g. meeting request, progress update, etc.).")
    communication_template: str = Field(default=None, description="This field will allow the teacher to choose a communication template that is aligned with their purpose and professional standards.")
    message_content: str = Field(default=None, description="This field will allow the teacher to write the content of their message.")


class HomeworkHelp(BaseModel):
    homework: str = Field(default=None)
    additonal_prompt: str = Field(default=None)
    format_data: str = Field(default=None)
    depth_of_detail: str = Field(default=None)
    reference_materials: str = Field(default=None)

class CourseDesign(BaseModel):
    description: str = Field(default= None)
    learning_objective: str = Field(default=None)
    problem_to_solve: str = Field(default=None)
    target_student: str = Field(default=None)
    dream_outcome: str = Field(default=None)
    number_of_modules: int = Field(default=None)
    number_of_lessons: int = Field(default=None, description="number of lessons per module")
    topic_ideas: str = Field(default=None)
    language: str = Field(default = None)
    include_assessment: bool = Field(default=None)
    additional_criteria: str = Field(default=None)



class TeacherChatbot(BaseModel):
    task_assistance: str = Field(default=None, description="This field will allow the user to input the task that they need assistance with, such as lesson planning, homework creation, grading, or professional correspondence.")
    topic: str = Field(default=None, description="This field will allow the user to input the topic that they need help with.")
    level: str = Field(default=None, description="This field will allow the user to specify the academic level of their students.")
    concerns: str = Field(default=None, description="This field will allow the user to input any concerns or questions they have related to the task.")


class CreativeStories(BaseModel):
    topic: str = Field(default=None)
    genre: str =Field(default=None)
    setting: str = Field(default=None)
    plot_points: str = Field(default=None)
    conflict_challenge: str = Field(default=None)
    tone_mood: str = Field(default=None)
    themes : str = Field(default=None)
    narrative_style: str = Field(default=None)
    length: str = Field(default=None, description="This field will allow the user to specify the desired length of the story.")
    specific_details: str = Field(default=None)
    language : str 


class StudyNotes(BaseModel):
    subject: str = Field(default=None, description="")
    grade: str = Field(default=None, description="")
    keywords: str = Field(default=None)
    focus_areas : str = Field(default=None)
    reference_material: str = Field(default=None)


class PracticeTest(BaseModel):
    subject: str = Field(default=None, description="")
    grade: str = Field(default=None, description="")
    difficulty_level: str = Field(default=None, description="")
    question_type: str = Field(description="e.g. multiple choice, true/false, short answer")
    number_of_questions: str = Field(default=None, description="")
    time_limit: str = Field(default=None, description="")
    reference_material : str = Field(default=None)
    sub_section : str = Field(default=None)

class EssayHelp(BaseModel):
    essay_topic: str = Field(default=None, description="")
    essay_text : str = Field(default=None, description="")
    essay_length: str = Field(default=None, description="")
    feedback: str = Field(default=None, description="")
    focus_areas: str = Field(default=None, description="")
    

    