from starlette.requests import Request
from pydantic import BaseModel


class Processor:
    @staticmethod
    def process_action(request: Request, model_name: str, 
                       model: BaseModel, method: str) -> dict:
        message = {
            'method': method,
            model_name: model.model_dump()
        }
        request.app.state.writer.write(message)
        return message
