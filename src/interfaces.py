import abc

class JSONInterFace(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_json_file') and callable(subclass.load_json_file) and hasattr(subclass, 'extract_json_data') and callable(subclass.extract_json_data))


class ReadJSON:

    def load_json_file_(self, path: str, file_name: str) -> str:
        pass




