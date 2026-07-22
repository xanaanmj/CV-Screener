# Fair Hire - CV Screening System

An AI-powered CV screening tool built during a 5-day AI bootcamp at Scrumconnect,
using a multi-agent CrewAI pipeline (running on a local Ollama model) with a
Flask + HTML front end.

## What it does
Given a CV and a job description, a team of six CrewAI agents work together to:
1. Analyse the job description (Skills / Experience / Education)
2. Remove bias from the CV (names, schools, postcodes, gender, etc.)
3. Score the candidate's skills, experience, and education against the job description
4. Produce a final summary and an overall score out of 10

## My contribution
I built the CV screening pipeline (`crew_backend.py`) and the web interface
(`app.py` + `templates/index.html`).

## Team project note
This bootcamp also produced a related NHS patient-prioritisation tool that used
a similar bias-removal approach, built by my teammates at Scrumconnect during those 5 days.

## Presentation
See `Enineering_Ethical_AI_PowerPoint.pptx` for the slide deck presented to Scrumconnect leadership.

