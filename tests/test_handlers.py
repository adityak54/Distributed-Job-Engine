from src.handlers.registry import HandlerRegistry
from src.handlers.generate_report import GenerateReportHandler
from src.handlers.send_email import SendEmailHandler
from src.handlers.process_csv import ProcessCsvHandler


def test_register_and_get():
    reg = HandlerRegistry()
    handler = GenerateReportHandler()
    reg.register(handler)
    assert reg.get("generate_report") is handler


def test_get_unknown_raises():
    reg = HandlerRegistry()
    try:
        reg.get("nonexistent")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_list_handlers():
    reg = HandlerRegistry()
    reg.register(GenerateReportHandler())
    reg.register(SendEmailHandler())
    reg.register(ProcessCsvHandler())
    assert sorted(reg.list_handlers()) == ["generate_report", "process_csv", "send_email"]


def test_generate_report_validate():
    h = GenerateReportHandler()
    assert h.validate({"report_type": "sales"}) is True
    assert h.validate({}) is False


def test_send_email_validate():
    h = SendEmailHandler()
    assert h.validate({"to": "a@b.com", "subject": "hi", "body": "hello"}) is True
    assert h.validate({"to": "a@b.com"}) is False


def test_process_csv_validate():
    h = ProcessCsvHandler()
    assert h.validate({"file_path": "/data/test.csv"}) is True
    assert h.validate({}) is False
