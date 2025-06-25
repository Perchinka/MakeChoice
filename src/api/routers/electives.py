from typing import Any, Dict, List
from uuid import UUID
import csv
import io

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from src.api.models import (
    ElectiveCreateRequest,
    ElectiveResponse,
    ImportElectiveReport,
    SkippedElective,
)
from src.api.routers.auth import get_current_user, require_admin
from src.domain.unit_of_work import AbstractUnitOfWork
from src.services.elective_service import ElectiveService
from src.api.dependencies import get_uow

router = APIRouter(prefix="/electives", tags=["electives"])


@router.get("/", response_model=List[ElectiveResponse])
async def list_electives(
    request: Request,
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return elective_service.list_electives(uow=uow)


@router.get("/{elective_id}", response_model=ElectiveResponse)
async def get_elective(
    elective_id: UUID,
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    elective = elective_service.get_elective(elective_id, uow)
    if not elective:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "elective not found")
    return elective


@router.put(
    "/{elective_id}",
    response_model=ElectiveResponse,
    dependencies=[require_admin],
)
async def update_elective(
    elective_id: UUID,
    payload: ElectiveCreateRequest,
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    updated = elective_service.update_elective(
        elective_id, **payload.model_dump(), uow=uow
    )
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "elective not found")
    return updated


@router.delete(
    "/{elective_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[require_admin],
)
async def delete_elective(
    elective_id: UUID,
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    if not elective_service.delete_elective(elective_id, uow):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "elective not found")


@router.delete(
    "/",
    dependencies=[require_admin],
    response_model=Dict[str, int],
)
async def delete_all_electives(
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    count = elective_service.delete_all_electives(uow)
    return {"deleted": count}


@router.post(
    "/from_file",
    response_model=ImportElectiveReport,
    dependencies=[require_admin],
)
async def import_electives_from_file(
    file: UploadFile = File(...),
    elective_service: ElectiveService = Depends(),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be UTF-8 encoded")

    reader = csv.DictReader(io.StringIO(text))
    electives_data: List[Dict[str, Any]] = []
    for row in reader:
        try:
            row["max_seats"] = int(row["max_seats"])
        except Exception as e:
            raise HTTPException(422, f"Invalid data in CSV row: {e}")
        electives_data.append(row)

    if not electives_data:
        raise HTTPException(400, "No elective records found in file")

    # perform the import inside a unit of work
    imported, skipped = elective_service.import_electives(electives_data, uow=uow)

    imported_out = [ElectiveResponse(**c.model_dump()) for c in imported]
    skipped_out = [
        SkippedElective(
            input=ElectiveCreateRequest(**inp),
            existing=ElectiveResponse(**existing.model_dump()),
        )
        for inp, existing in skipped
    ]

    return ImportElectiveReport(imported=imported_out, skipped=skipped_out)
