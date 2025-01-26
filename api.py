import enum
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"


class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        self._temperature = {
            Zone.LIVING_ROOM: 22,
            Zone.BEDROOM: 20,
            Zone.KITCHEN: 24,
            Zone.BATHROOM: 23,
            Zone.OFFICE: 21,
        }

    @llm.ai_callable(
        description="Данная функция нужна для работы с таск-менеджером YouGile. Любые действия с задачами выполняются с её помощью."
    )
    def task_manager(
        self,
        user_task: Annotated[
            str,
            llm.TypeInfo(
                description="Действие, которое необходимо выполнить с задачами"
            ),
        ],
    ):
        logger.info("user_task: %s", user_task)
        answer = "Задача 1234 выполнена."  # TODO вызов работы с бразуером
        return f"Отчёт по задаче: {answer}"
