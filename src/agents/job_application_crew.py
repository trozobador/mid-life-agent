import json
import logging
import os
import sys
from textwrap import dedent

from crewai import Agent, Crew, Process, Task

current_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)

from prompts.job_application_prompts import (
    get_applicant_prompt,
    get_editor_prompt,
    get_hr_prompt,
    get_interview_coach_prompt,
    get_strategist_prompt,
)
from tools.resume_tools import (
    generate_resume_tool,
    pgcount_tool,
    save_interview_prep_tool,
    save_resume_json,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class JobApplicationCrew:
    def __init__(
        self,
        role: str = None,
        job_profile_path: str = "data/job_desc.txt",
        output_dir: str = "outputs",
        provider: str = None,
        language: str = "pt-BR",
    ):
        self.role = role
        self.job_profile_path = job_profile_path
        self.output_dir = output_dir
        self.provider = provider
        self.language = language

        os.environ["RESUME_OUTPUT_DIR"] = output_dir

        with open(job_profile_path, "r") as f:
            self.job_description = f.read()

        original_resume_path = "data/resume.json"
        with open(original_resume_path, "r") as f:
            self.original_resume = json.load(f)

        generated_resume_path = os.path.join(output_dir, "json", "resume.json")
        if os.path.exists(generated_resume_path):
            with open(generated_resume_path, "r") as f:
                self.resume_generated = json.load(f)
        else:
            self.resume_generated = self.original_resume

        self.llm = self._get_llm()

    def _get_llm(self):
        try:
            from src.llm_factory import get_llm
            return get_llm(provider=self.provider)
        except ImportError:
            try:
                sys.path.insert(0, grandparent_dir)
                from src.llm_factory import get_llm
                return get_llm(provider=self.provider)
            except Exception:
                return None

    def run(self):
        llm_kwargs = {"llm": self.llm} if self.llm else {}

        career_strategist = Agent(
            name="Career Strategist",
            role="Senior Career Strategist specializing in professional repositioning",
            goal=(
                "Rewrite the candidate's resume narrative and strategically reframe their "
                "experiences to maximize fit for the target job, without fabricating anything."
            ),
            backstory=(
                "You have helped hundreds of mid-career professionals pivot into new roles by "
                "surfacing the hidden relevance of their existing experience. You know that "
                "the same career can tell many different stories — your job is to tell the "
                "right story for this specific role."
            ),
            verbose=True,
            allow_delegation=False,
            **llm_kwargs,
        )

        hiring_manager = Agent(
            name="Hiring Manager",
            role="Experienced hiring manager specializing in tech roles",
            goal="Evaluate candidate resumes and provide constructive, actionable feedback",
            backstory=(
                "You have years of experience hiring for top tech companies and know exactly "
                "what makes a strong candidate. You provide detailed feedback and accurate "
                "ratings based on job requirements."
            ),
            verbose=True,
            allow_delegation=False,
            **llm_kwargs,
        )

        resume_editor = Agent(
            name="Resume Editor",
            role="Expert resume editor with tech industry knowledge",
            goal="Optimize resumes based on feedback to fit on up to two pages and highlight key qualifications",
            backstory=(
                "You've helped countless tech professionals land their dream jobs by crafting "
                "perfect resumes of up to two pages. You balance depth with impact."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[generate_resume_tool, pgcount_tool, save_resume_json],
            **llm_kwargs,
        )

        job_applicant = Agent(
            name="Job Applicant",
            role="Motivated professional seeking to optimize their job application",
            goal="Secure a job offer by iterating on the resume until it achieves a rating ≥ 8.5",
            backstory=(
                "You are determined to present yourself in the best possible light. You "
                "coordinate between the hiring manager and editor until your resume is excellent."
            ),
            verbose=True,
            allow_delegation=False,
            **llm_kwargs,
        )

        interview_coach = Agent(
            name="Interview Coach",
            role="World-class Interview Coach for tech and business professionals",
            goal=(
                "Produce a comprehensive interview preparation guide tailored to the candidate's "
                "real experience and the specific job requirements."
            ),
            backstory=(
                "You have coached hundreds of candidates for interviews at top companies. "
                "You know what interviewers look for and how to help candidates tell compelling, "
                "authentic stories from their actual experience."
            ),
            verbose=True,
            allow_delegation=False,
            **llm_kwargs,
        )

        reposition_resume = Task(
            description=dedent(get_strategist_prompt(self.job_description, self.original_resume, self.language)),
            agent=career_strategist,
            expected_output=(
                "A repositioned resume as a valid JSON object with the same structure as the input, "
                "with the summary rewritten, experiences prioritized and reframed, and skills "
                "reordered for the target role. No fabricated information."
            ),
        )

        evaluate_resume = Task(
            description=dedent(get_hr_prompt(self.job_description, self.resume_generated)),
            agent=hiring_manager,
            expected_output=(
                "A comprehensive evaluation report including: numerical rating (1–10), "
                "strengths, areas for improvement, missing ATS keywords, and resume "
                "presentation feedback."
            ),
            context=[reposition_resume],
        )

        edit_resume = Task(
            description=dedent(
                get_editor_prompt(
                    self.job_description, self.resume_generated, self.original_resume, self.language
                )
            ),
            agent=resume_editor,
            expected_output=(
                "An optimized resume (up to two pages) saved as JSON and PDF, addressing the hiring "
                "manager's feedback and fitting up to two pages. Includes confirmation that "
                "the file was saved."
            ),
            context=[reposition_resume, evaluate_resume],
        )

        optimize_application = Task(
            description=dedent(get_applicant_prompt(self.job_description, self.original_resume, self.language)),
            agent=job_applicant,
            expected_output=(
                "A report with: final resume rating (≥ 8.5), summary of key improvements "
                "made across iterations, and any additional recommendations from the hiring manager."
            ),
            context=[reposition_resume, evaluate_resume, edit_resume],
        )

        prepare_interview = Task(
            description=dedent(
                get_interview_coach_prompt(self.job_description, self.resume_generated)
            ),
            agent=interview_coach,
            expected_output=(
                "A comprehensive interview preparation guide saved as 'interview_prep.md' in "
                "the output directory, including: role analysis, 15 likely questions with "
                "suggested answers, key talking points, red flags to address, questions to ask "
                "the interviewer, pre-interview checklist, and salary/negotiation tips."
            ),
            context=[reposition_resume, optimize_application],
        )

        crew = Crew(
            agents=[
                career_strategist,
                hiring_manager,
                resume_editor,
                job_applicant,
                interview_coach,
            ],
            tasks=[
                reposition_resume,
                evaluate_resume,
                edit_resume,
                optimize_application,
                prepare_interview,
            ],
            verbose=True,
            process=Process.sequential,
        )

        result = crew.kickoff()

        logger.info(crew.usage_metrics)
        logger.info(f"Token Usage: {result.token_usage}")

        interview_content = getattr(getattr(prepare_interview, "output", None), "raw", None)
        if interview_content:
            interview_path = os.path.join(self.output_dir, "interview_prep.md")
            with open(interview_path, "w", encoding="utf-8") as f:
                f.write(interview_content)
            logger.info(f"Interview prep saved to: {interview_path}")

        # Deterministic padding: ensure PDF reaches 2 pages
        try:
            from resume.pad_pages import pad_to_two_pages
            final_pages = pad_to_two_pages(self.output_dir)
            logger.info(f"Final PDF page count after padding: {final_pages}")
        except Exception as e:
            logger.warning(f"pad_to_two_pages skipped: {e}")

        role_label = f" [{self.role}]" if self.role else ""
        logger.info(f"Outputs{role_label} saved to: {self.output_dir}/")

        return result


def main():
    job_application_crew = JobApplicationCrew()
    final_result = job_application_crew.run()
    logger.info(final_result)
