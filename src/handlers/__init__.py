from src.handlers.registry import registry
from src.handlers.generate_report import GenerateReportHandler
from src.handlers.send_email import SendEmailHandler
from src.handlers.process_csv import ProcessCsvHandler

registry.register(GenerateReportHandler())
registry.register(SendEmailHandler())
registry.register(ProcessCsvHandler())
