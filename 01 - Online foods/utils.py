import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_register(db: Session, model: models.Base, **kwargs):
    """
    Create a new record in the database for the specified model.

    Args:
        db (Session): SQLAlchemy session.
        model (models.Base): SQLAlchemy model class.
        **kwargs: Keyword arguments representing the attributes of the new record.

    Returns:
        Tuple[str, models.Base or str]: A tuple containing the status of the operation ("ok" or "error")
        and either the newly created model instance or an error message.

    """
    db_model = model(**kwargs)
    try:
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
    except SQLAlchemyError as e:
        db.rollback()
        return "error", e
    return "ok", db_model


def upload_normalized_values(
    model: (
        models.MatrialStatus
        | models.OccupationStatus
        | models.IncomeStatus
        | models.EducationStatus
    ),
    values: list[str],
    session: Session,
):
    """
    Upload normalized values to the specified model.

    Args:
        model (models.MatrialStatus | models.OccupationStatus | models.IncomeStatus | models.EducationStatus):
            The SQLAlchemy model class to upload values to.
        values (list[str]): A list of string values to upload.
        session (Session): SQLAlchemy session.

    Returns:
        dict: A dictionary containing the uploaded values and their corresponding IDs in the database.

    """
    u_result = {}
    for val in values:
        status, res = create_register(session, model, status=val)
        if status == "ok":
            u_result[res.status] = res.id
        elif "already exists" in res.args[0]:
            new_res = session.query(model).filter_by(status=val).first()
            u_result[new_res.status] = new_res.id
    return u_result
