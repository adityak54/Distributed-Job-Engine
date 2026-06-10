from src.handlers.generate_report import GenerateReportHandler

# A simple dictionary mapping string names to instantiated handler classes
HANDLER_REGISTRY = {
    "generate_report": GenerateReportHandler(),
    # "send_email": SendEmailHandler(),  <-- easy to add more later
}