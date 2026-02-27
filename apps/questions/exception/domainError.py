class DomainError(Exception):
    pass


class QuestionNotFound(DomainError):
    pass


class InvalidContentType(DomainError):
    pass


class AnswerAlreadyExists(DomainError):
    pass

class InvalidUpdatePayload(DomainError):
    pass

class ContentNotFound(DomainError):
    pass
