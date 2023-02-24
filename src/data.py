from dataclasses import dataclass, field

@dataclass
class StudentInfo:
    name: str
    student_number: str = field(default_factory=str, init=False)
    group: str
    feedback: list = field(default_factory=list) 
    grade: int = field(default_factory=int)



@dataclass
class ErrorInfo:
    error_id: str = ""
    text: str = ""
    values: dict = field(default_factory=dict)
    amount: int = 0
    feedback: str = field(default_factory=str)
    alternative: list = field(default_factory=list)
    exclude: list = field(default_factory=list)

    def __str__(self) -> str:
        return(f"{self.error_id}, {self.text}")

@dataclass(kw_only=True)
class Category(ErrorInfo):
    name: str = ""
    category_sum: int = field(default=0)
    errors: list[ErrorInfo] = field(default_factory=list)

    def __str__(self) -> str:
        return super().__str__() + f"{self.errors}"
    
@dataclass
class ExamInfo(StudentInfo): 
    exam_level: str = ""
    exam_group: str = ""

