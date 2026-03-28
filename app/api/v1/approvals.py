"""
ROUTER DE APROBACIONES (Approval Router).
Define los puntos de entrada para la gestion de autorizaciones humanas.
Permite listar solicitudes pendientes, consultar detalles y emitir 
decisiones tecnicas de aprobacion o rechazo sobre trabajos bloqueados.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.approval import ApprovalDecisionRequest, ApprovalResponse
from app.services.approval_service import ApprovalService

# Definicion del router para agrupar las rutas de aprobaciones
router = APIRouter()

# Instanciacion del servicio de logica de negocio para aprobaciones
approval_service = ApprovalService()


@router.get("", response_model=list[ApprovalResponse])
def list_approvals(
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Recupera una lista de solicitudes de aprobacion.
    Permite filtrar por estado (ej: 'pending') para facilitar el trabajo del supervisor.
    """
    return approval_service.list_approvals(db, limit=limit, offset=offset, status=status)


@router.get("/{approval_id}", response_model=ApprovalResponse)
def get_approval(approval_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene el detalle completo de una solicitud de aprobacion especifica.
    Util para revisar el motivo del bloqueo antes de tomar una decision.
    """
    approval = approval_service.get_approval_by_id(db, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval no encontrada")
    return approval


@router.post("/{approval_id}/approve", response_model=ApprovalResponse)
def approve_approval(approval_id: UUID, payload: ApprovalDecisionRequest, db: Session = Depends(get_db)):
    """
    Endpoint para autorizar la ejecucion de un Job.
    Tras esta accion, el Job cambiara a estado 'ready_to_execute'.
    """
    try:
        return approval_service.approve(
            db=db,
            approval_id=approval_id,
            resolved_by=payload.resolved_by,
            resolved_by_name=payload.resolved_by_name,
            resolution_comment=payload.resolution_comment
        )
    except ValueError as exc:
        # Maneja casos donde la aprobacion ya fue resuelta o no existe
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/{approval_id}/reject", response_model=ApprovalResponse)
def reject_approval(approval_id: UUID, payload: ApprovalDecisionRequest, db: Session = Depends(get_db)):
    """
    Endpoint para denegar la ejecucion de un Job.
    Tras esta accion, el Job y su comando asociado quedaran marcados como 'rejected'.
    """
    try:
        return approval_service.reject(
            db=db,
            approval_id=approval_id,
            resolved_by=payload.resolved_by,
            resolved_by_name=payload.resolved_by_name,
            resolution_comment=payload.resolution_comment
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))