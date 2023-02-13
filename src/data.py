from dataclasses import dataclass

@dataclass
class StudentInfo:
    def __init__(self, name: str, student_number: str, exam_level: str, group: str, feedback: list) -> None:
        self.name = name
        self.student_name = student_number
        self.exam_level = exam_level
        self.group = group
        self.feedback = feedback
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

