from src.models import Job, JobStatus
from src.worker.executor import execute_job
import src.handlers  # noqa: F401


def test_job_completes_successfully(db):
    job = Job(
        handler_name="generate_report",
        payload={"report_type": "sales"},
        status=JobStatus.PENDING,
    )
    db.add(job)
    db.commit()

    execute_job(db, job)

    db.refresh(job)
    assert job.status == JobStatus.COMPLETED
    assert job.started_at is not None
    assert job.finished_at is not None


def test_job_fails_validation(db):
    job = Job(
        handler_name="send_email",
        payload={},  # missing required fields
        status=JobStatus.PENDING,
    )
    db.add(job)
    db.commit()

    execute_job(db, job)

    db.refresh(job)
    assert job.status == JobStatus.FAILED
    assert "validation failed" in job.error_message.lower()


def test_job_transitions_to_dead_after_max_retries(db):
    job = Job(
        handler_name="generate_report",
        payload={"report_type": "sales"},
        status=JobStatus.PENDING,
        retries=2,
        max_retries=3,
    )
    db.add(job)
    db.commit()

    # Monkey-patch the handler to raise an exception
    from src.handlers.registry import registry
    original_execute = registry.get("generate_report").execute
    registry.get("generate_report").execute = lambda p: (_ for _ in ()).throw(
        RuntimeError("simulated failure")
    )

    execute_job(db, job)

    # Restore
    registry.get("generate_report").execute = original_execute

    db.refresh(job)
    assert job.status == JobStatus.DEAD
    assert job.retries == 3
    assert "simulated failure" in job.error_message


def test_job_transitions_to_retrying(db):
    job = Job(
        handler_name="generate_report",
        payload={"report_type": "sales"},
        status=JobStatus.PENDING,
        retries=0,
        max_retries=3,
    )
    db.add(job)
    db.commit()

    from src.handlers.registry import registry
    original_execute = registry.get("generate_report").execute
    registry.get("generate_report").execute = lambda p: (_ for _ in ()).throw(
        RuntimeError("transient error")
    )

    execute_job(db, job)

    registry.get("generate_report").execute = original_execute

    db.refresh(job)
    assert job.status == JobStatus.RETRYING
    assert job.retries == 1
