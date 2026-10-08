import warnings
from report_summarization_crew.crew_2 import ReportSummarizationCrew


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    '''This function runs the ReportSummarizationCrew'''
    # Define the inputs in the form of dict
    inputs = {"field": 'Education'}

    # Create the crew
    rsc = ReportSummarizationCrew().crew()

    # Pass the inputs to the crew and execute the crew
    result = rsc.kickoff(inputs = inputs)

    if "__name__" == "__main__":
        run()