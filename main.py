import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "Вы являетесь голосовым AI-ассистентом, интегрированным с системой управления задачами YouGile. Ваша цель - обеспечить пользователю максимально комфортное и эффективное взаимодействие с системой управления задачами. Ваша роль включает:"
            "1. Создание задач: Слушайте команды пользователя и запросы на создание новых задач, уточняйте название задачи, сроки и приоритет."
            "2. Управление задачами: Помогайте пользователю изменять статус задач, добавлять комментарии и обновлять информацию."
            "3. Просмотр и фильтрация: Позволяйте пользователю просматривать список задач, используя различные фильтры (по дате, приоритету, статусу и т.д.)."
            "4. Ведение диалога: Поддерживайте естественный и чёткий диалог, уточняйте детали, чтобы минимизировать недопонимание."
            "5. Обратная связь: Подтверждайте выполненные действия и предоставляйте обратную связь о текущем состоянии задач."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
