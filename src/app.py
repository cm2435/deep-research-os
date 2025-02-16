from fastapi import FastAPI
from core.clients import INNGEST_CLIENT

from core.research import batch_answer_questions, answer_single_question
from core.search_planner import generate_search_plan
from core.evaluation import generate_critic_response
from core.main import initialize_research
from core.report_generator import fill_report_template, generate_report

import inngest
import inngest.fast_api

app = FastAPI()


def serve_inngest(app):
    inngest.fast_api.serve(
        app,
        INNGEST_CLIENT,
        [
            batch_answer_questions,
            generate_search_plan,
            generate_critic_response,
            answer_single_question,
            initialize_research,
            fill_report_template,
            generate_report,
        ],
    )


serve_inngest(app)


@app.get("/health")
def health_check():
    return "Ok"
