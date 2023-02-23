from dataclasses import dataclass

@dataclass
class StudentInfo:
    def __init__(self, name: str, student_number: str, group: str, feedback: list) -> None:
        self.name = name
        self.student_number = student_number
        self.group = group
        self.feedback = feedback

    def print_id(self):
        print(f'The name is {self.name}, student_number is {self.student_number}')
@dataclass
class ErrorInfo:
    def __init__(self, error:tuple, text:str, errorpoints:float, amount:int, alternative:list, exclude:list) -> None:
        self.error = error
        self.text = text
        self.errorpoints = errorpoints
        self.amount = amount
        self.alternative = alternative
        self.exclude = exclude
@dataclass
class Category:
    def __init__(self, name:str, category_sum:int) -> None:
        self.name = name
        self.category_sum = category_sum
@dataclass
class ExamInfo(StudentInfo): 
    def __init__(self, exam_level:str):
        self.exam_level = exam_level

