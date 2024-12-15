try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
    from app.database import crud
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

router = APIRouter()


"""
    Pensando na criticidade das três próximas funções, 
    devem ser utilizadas com cautela, apenas por um administrador.
"""
@router.post("/", response_model=UserSchema)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=List[UserSchema])
def get_all_users_route(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.get("/{user_id}", response_model=UserSchema)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)

"""
    As funções abaixo não retornam os dados do usuário,
    já que são operações com dados sensíveis e privados.
"""
@router.put("/{user_id}", response_model=UserSchema)
def update_user_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    """
        Rota para atualizar a senha de um usuário.

        Args:
            user_id: ID do usuário que deve ter a senha alterada.
            update_data: Dados do usuário para atualizar.
            db: Sessão do banco de dados.

        Returns:
            message: Retorna apenas uma mensagem avisando que a alteração foi realizada.
    """
    crud.update_user(db, user_id, update_data)
    return {"message": "Dados atualizados com sucesso."}

@router.put("/{user_id}/password")
def update_user_password_route(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    """
        Rota para atualizar a senha de um usuário.

        Args:
            user_id: ID do usuário que deve ter a senha alterada.
            update_data: Dados da senha para atualizar.
            db: Sessão do banco de dados.

        Returns:
            message: Retorna apenas uma mensagem avisando que a senha foi alterada.
    """

    crud.update_user_password(db, user_id, update_data)
    return {"message": "Senha alterada com sucesso."}

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
        Rota para excluir um usuário.

        Args:
            user_id: ID do usuário selecionado para ser excluído.
            db: Sessão do banco de dados.

        Returns:
            message: Retorna mensagem avisando que foi excluído
    """

    crud.delete_user(db, user_id)
    return {"message": "Usuário excluído com sucesso."}
