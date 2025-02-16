from pydantic import BaseModel, Field


class ResearchCycle(BaseModel):
    question_answering_round: int = Field(
        ...,
        description="Which cycle of research number this question answer was generated in.",
    )
    reasoning_for_subquestions_to_answer: str | None = Field(
        ...,
        description="Reasoning which was generated to determine which subquestions would further move the research closer to being ready to generate a final report for the user",
    )
    question_answer_pairs: list[str] = Field(
        ...,
        description="The stringified representation of a series of questions posed and their answers from the open web",
    )
    critic_reasoning_of_sufficiency: str | None = Field(
        ...,
        description="Reasoning which was generated to determine if the questions answered are sufficient to generate a final report for the user",
    )
    is_sufficient: bool | None = Field(
        ...,
        description="Weather we decided we had enough background information to move to report generation",
    )

    def pretty_print(self) -> str:
        parts = [f"Research Cycle {self.question_answering_round}:"]

        if self.reasoning_for_subquestions_to_answer is not None:
            parts.append(
                f"Reasoning for Subquestions: {self.reasoning_for_subquestions_to_answer}"
            )

        parts.extend(
            [
                f"Question-Answer Pair: {question_answer}"
                for question_answer in self.question_answer_pairs
            ]
        )

        if self.critic_reasoning_of_sufficiency is not None:
            parts.append(
                f"Critic Reasoning of Sufficiency: {self.critic_reasoning_of_sufficiency}"
            )

        if self.is_sufficient is not None:
            parts.append(f"Is Sufficient: {'Yes' if self.is_sufficient else 'No'}")

        return "\n".join(parts)
