from starlette.requests import Request
from pydantic import BaseModel


class Processor:
    @staticmethod
    def process_action(
        request: Request, 
        model_name: str, 
        model: BaseModel, 
        method: str, 
        current_user: str
) -> dict:
        message = {
            'method': method,
            'model': model_name,
            'data': model.model_dump(),
            'current_user': current_user
        }
        request.app.state.writer.write(message)
        return message
