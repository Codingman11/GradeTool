from dataclasses import dataclass, field


@dataclass
class ErrorInfo:
    _id: str = ""
    text: str = ""
    values: dict = field(default_factory=dict)
    amount: int = field(default=0)
    feedback: str = field(default_factory=str)
    alternative: list = field(default_factory=list, init=False)
    exclude: list = field(default_factory=list, init=False)

    def __str__(self) -> str:
        return(f"{self._id}, {self.text}, {self.feedback}, {self.values}, {self.amount}")


@dataclass
class StudentInfo:
    name: str = ""
    student_number: str = field(default_factory=str)
    group: str = field(default_factory=str)
    error_list: dict = field(default_factory=dict)
    grade: int = field(default_factory=int)
    errorpoints: float = field(default=0)
    moodle_comment: list = field(default_factory=list)
    def __str__(self) -> str:
        return(f"Student name: {self.name}, group: {self.group}")
    
@dataclass
class Students:
    studentList: list[StudentInfo] = field(default_factory=list)
@dataclass
class Category:
    name: str = ""
    category_sum: int = field(default=0)
    errors: list[ErrorInfo] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.errors}"
    
    def getName(self):
        return self.name
    
    def findError(self, error_id) -> ErrorInfo:
        return (x for x in self.errors if (x._id == error_id))
    
@dataclass
class ExamInfo(StudentInfo): 
    exam_level: str = ""
    exam_group: str = ""

