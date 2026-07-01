from crewai import Agent, Task, Crew, Process, LLM
from pathlib import Path

CV = Path("James Wilson CV.txt").read_text()
JD = Path("JOB DESCRIPT SE.txt").read_text()

VERBOSE = True     
TRACING = False

# Model Initialisation (leave this as-is)
llm = LLM(
    model="ollama/granite4.1:3b",
    base_url="http://localhost:11434",
    temperature=0.3,
)


agent_one = Agent(
    role="Bias Cleanser",        
    goal="Get rid of any bias from the CV. Free from bias — irrelevant signals (a name, a school, a club, a postcode, gender) should not push a candidate up or down.",
    backstory="You are a fairness expert who ensures all candidates are evaluated equally.",   
    llm=llm,
)

agent_two = Agent(
    role="Job Description Analyser",
    goal="Analyse the job description and identify key requirements and responsibilities. Split them into Skills, Experience, and Education.",        # TODO
    backstory="You are a recruitment expert who specialises in understanding job requirements.",   
    llm=llm,
)

agent_three = Agent(

    role = "Skills Analyser",

    goal = "Analyse the CV and identify the candidate's skills, and match them to skills in the job desciption, given by the Job Description Analyser. Then score the skills, based on the job description, giving it a score between 1-10.",

    backstory = "You are a CV expert who specialises in identifying skills and matching them to job requirements.",

    llm=llm,
)

agent_four = Agent(

    role = "Experience Analyser",

    goal = "Analyse the CV and identify the candidate's experience, and match them to experience in the job desciption, given by the Job Description Analyser. Then score the experience, based on the job description, giving it a score between 1-10.",

    backstory = "You are a CV expert who specialises in identifying experience and matching them to job requirements.",

    llm=llm,
)

agent_five = Agent(

    role = "Education Analyser",

    goal = "Analyse the CV and identify the candidate's education, and match them to education in the job desciption, given by the Job Description Analyser. Then score the education, based on the job description, giving it a score between 1-10.",

    backstory = "You are a CV expert who specialises in identifying education and matching them to job requirements.",

    llm=llm,
)

agent_six = Agent(

    role = "CV Summarizer and Scorer",

    goal = "Create a concise summary of the candidate's qualifications based on their CV. Then using the scores from the Skills Analyser, Experience Analyser, and Education Analyser, give the candidate a final score out of 10.",

    backstory = "You are a resume writing expert who specialises in creating compelling summaries.",

    llm=llm,
)


my_team = [
    agent_one,
    agent_two,
    agent_three,
    agent_four,
    agent_five,
    agent_six
]


def CV_input(CV, JD):
    jd_analyser = Task(
    description=f"Analyse the <JD>{JD}</JD> and identify key requirements and responsibilities. Split them into Skills, Experience, and Education.",
    expected_output="A clear summary of the job description, split into Skills, Experience, and Education.",
    agent=agent_two,
)

    bias_cleanser = Task(
        description=f"Get rid of any bias from the <CV>{CV}</CV>. Free from bias — irrelevant signals (a name, a school, a club, a postcode, gender) should not push a candidate up or down.",
        expected_output="A clear summary of the CV, free from bias.",
        agent=agent_one,
    )

    skills_analyser = Task(
        description=f"Analyse the bias-free CV and identify the candidate's skills, and match them to skills in the job desciption, given by the Job Description Analyser.",
        expected_output="A clear summary of the candidate's skills, matched to the job description.",
        agent=agent_three,
        context = [bias_cleanser, jd_analyser]
    )

    experience_analyser = Task(
        description=f"Analyse the bias-free CV and identify the candidate's experience, and match them to experience in the job desciption, given by the Job Description Analyser.",
        expected_output="A clear summary of the candidate's experience, matched to the job description.",
        agent=agent_four,
        context = [bias_cleanser, jd_analyser]
    )

    education_analyser = Task(
        description=f"Analyse the bias-free CV and identify the candidate's education, and match them to education in the job desciption, given by the Job Description Analyser.",
        expected_output="A clear summary of the candidate's education, matched to the job description.",
        agent=agent_five,
        context = [bias_cleanser, jd_analyser]
    )

    cv_summarizer_and_scorer = Task(
        description=f"Create a concise summary of the candidate's qualifications based on their <CV>{CV}</CV>. Then using the scores from the Skills Analyser, Experience Analyser, and Education Analyser, give the candidate a final score out of 10.",
        expected_output="A clear summary of the candidate's qualifications and a final score out of 10.",
        agent=agent_six,
    )

    CV_crew = Crew(
        agents=my_team,
        tasks=[jd_analyser, bias_cleanser, skills_analyser, experience_analyser, education_analyser, cv_summarizer_and_scorer],
        process=Process.sequential,
        verbose=VERBOSE,
        tracing=TRACING,
        )
    result = CV_crew.kickoff()
    return result


if __name__ == "__main__":
    # TODO: change these lines to describe YOUR team and give example prompts
    print("My Agent Team is ready! Insert a Job Description and CV:")
    print("(type 'quit' to exit)\n")

    result = CV_input(CV, JD)
    print("\nFinal answer:\n" + str(result) + "\n")
