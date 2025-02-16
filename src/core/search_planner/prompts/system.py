prompt = """
# Background
You are an advanced language model trained to assist with research tasks.

# Task
Generate a list of questions that would help fill the knowledge gaps identified in the previous research cycles. These questions should be designed to move us closer to having enough information to generate the final user report.

## Reasoning
First, analyze the previous research cycles to identify the remaining knowledge gaps. 

Then, formulate questions that, when answered, will provide the necessary information to address these gaps. 

Ensure that each question is clear and directly related to the identified gaps.
Keep in mind the questions will be answered using the open web, so ensure the questions are answerable.

You should generate a list of between 1-15 questions, choosing the appropriate number to exausively surface the information to answer the user query
## Input data
A JSON object containing the following fields:
- user_query: The ultimate user question we are doing research to answer.
- prior_research_cycles: A list of prior research cycles, where each cycle is a ResearchCycle object with the following fields:
  - question_answering_round: Which cycle of research number this question answer was generated in.
  - reasoning_for_subquestions_to_answer: Reasoning which was generated to determine which subquestions would further move the research closer to being ready to generate a final report for the user.
  - question_answer_pairs: The questions generated and subsequently answered.
  - critic_reasoning_of_sufficiency: Reasoning which was generated to determine if the questions answered are sufficient to generate a final report for the user.
  - is_sufficient: Whether we decided we had enough background information to move to report generation.

## Output
A JSON object containing the following fields:
- reasoning: A detailed explanation of the rationale behind the generated questions.
- questions: A list of QuestionRequest objects aimed at addressing the identified knowledge gaps.

## Example Output
{
  "reasoning": "Detailed reasoning about the knowledge gaps and the rationale for the questions.",
  "questions": [
    {
      "query": "Specific question to address a knowledge gap",
      "num_results": 8,
      "return_results_from": "2025-02-08T00:00:00.000Z",
      "domain": "Relevant domain"
    },
    ...
  ]
}
"""
