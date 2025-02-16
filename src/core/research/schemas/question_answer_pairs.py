from pydantic import BaseModel
from .question_answer import Answer
from .question_request import QuestionRequestWithId


class QuestionAndAnswer(BaseModel):
    question: QuestionRequestWithId
    answer: Answer


class QuestionAnswerPairs(BaseModel):
    question_answer_pairs: list[QuestionAndAnswer]

    def pretty_print(self) -> list[str]:
        return [
            f"  Question: {qa.question.query}\n"
            f"  Question ID: {qa.question.question_id}\n"
            f"  Domain: {qa.question.domain}\n"
            f"  Answer Summary: {qa.answer.summary}\n"
            f"  Reasoning: {qa.answer.reasoning}\n"
            f"  Citations: {', '.join(f' Author: {citation.author} Date: ({citation.source_date}) URL: {citation.url}' for citation in qa.answer.citations)}"
            for qa in self.question_answer_pairs
        ]
