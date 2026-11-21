import sqlite3
from typing import List
from fastapi import HTTPException, status

from app.models.customer import CustomerModel
from app.views import CustomerCreate, CustomerResponse, CustomerUpdate


class CustomerController:

    @staticmethod
    def list_customers(db: sqlite3.Connection) -> List[CustomerResponse]:
        rows = CustomerModel.get_all(db)
        return [CustomerResponse.model_validate(dict(row)) for row in rows]

    @staticmethod
    def get_customer(db: sqlite3.Connection, customer_id: int) -> CustomerResponse:
        row = CustomerModel.get_by_id(db, customer_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado",
            )
        return CustomerResponse.model_validate(dict(row))

    @staticmethod
    def create_customer(db: sqlite3.Connection, customer: CustomerCreate) -> CustomerResponse:
        try:
            new_id = CustomerModel.create(
                conn=db,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                address=customer.address,
                registration_date=customer.registration_date,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al crear el cliente: {exc}",
            ) from exc

        row = CustomerModel.get_by_id(db, new_id)
        return CustomerResponse.model_validate(dict(row))

    @staticmethod
    def update_customer(
        db: sqlite3.Connection, customer_id: int, customer: CustomerUpdate
    ) -> CustomerResponse:
        try:
            updated = CustomerModel.update(
                conn=db,
                customer_id=customer_id,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                address=customer.address,
                registration_date=customer.registration_date,
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Error de integridad al actualizar el cliente: {exc}",
            ) from exc

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado",
            )
        row = CustomerModel.get_by_id(db, customer_id)
        return CustomerResponse.model_validate(dict(row))

    @staticmethod
    def delete_customer(db: sqlite3.Connection, customer_id: int) -> CustomerResponse:
        row = CustomerModel.get_by_id(db, customer_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado",
            )
        response_data = CustomerResponse.model_validate(dict(row))
        try:
            CustomerModel.delete(db, customer_id)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el cliente porque tiene registros asociados",
            ) from exc
        return response_data