import abc


class WebDriverBase(abc.ABC):

    def __init__(self):
        self.driver = None

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def get(self, url):
        pass

    @abc.abstractmethod
    def login(self):
        pass