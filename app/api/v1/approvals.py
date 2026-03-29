"""
ROUTER DE APROBACIONES (Approval Router).
Define los endpoints para consultar, aprobar o rechazar solicitudes
de aprobacion usando usuario autenticado real.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.approval import ApprovalDecisionRequest, ApprovalResponse
from app.services.approval_service import ApprovalService

# Router de aprobaciones
router = APIRouter()

# Servicio de negocio de aprobaciones
approval_service = ApprovalService()


@router.get(
    "",
    response_model=list[ApprovalResponse],
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def list_approvals(
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista solicitudes de aprobacion.
    Puede filtrarse por estado.
    """
    return approval_service.list_approvals(db, limit=limit, offset=offset, status=status)


@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def get_approval(approval_id: UUID, db: Session = Depends(get_db)):
    """
    Devuelve el detalle de una aprobacion concreta.
    """
    approval = approval_service.get_approval_by_id(db, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval no encontrada")
    return approval


@router.post(
    "/{approval_id}/approve",
    response_model=ApprovalResponse,
    dependencies=[Depends(require_roles("admin"))]
)
def approve_approval(
    approval_id: UUID,
    payload: ApprovalDecisionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Aprueba una solicitud usando el usuario autenticado actual.
    """
    try:
        return approval_service.approve(
            db=db,
            approval_id=approval_id,
            current_user=current_user,
            resolution_comment=payload.resolution_comment
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post(
    "/{approval_id}/reject",
    response_model=ApprovalResponse,
    dependencies=[Depends(require_roles("admin"))]
)
def reject_approval(
    approval_id: UUID,
    payload: ApprovalDecisionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Rechaza una solicitud usando el usuario autenticado actual.
    """
    try:
        return approval_service.reject(
            db=db,
            approval_id=approval_id,
            current_user=current_user,
            resolution_comment=payload.resolution_comment
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))