# -*- coding: utf-8 -*-
import logging
import yt_dlp
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_youtube_url(query):
    """Busca o vídeo no YouTube e retorna a URL direta do áudio."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            video = info['entries'][0]
        else:
            video = info
        return video['url'], video.get('title', 'Música')

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Bem-vindo ao Meu DJ. O que você quer ouvir hoje?"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class PlayVideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PlayVideoIntent")(handler_input)

    def handle(self, handler_input):
        query = handler_input.request_envelope.request.intent.slots["videoQuery"].value
        
        try:
            audio_url, title = get_youtube_url(query)
            
            speak_output = f"Tocando agora: {title}"
            
            # Cria a diretiva para tocar o áudio
            handler_input.response_builder.add_directive(
                PlayDirective(
                    play_behavior=PlayBehavior.REPLACE_ALL,
                    audio_item=AudioItem(
                        stream=Stream(
                            url=audio_url,
                            token=audio_url[-100:], # Token único simplificado
                            offset_in_milliseconds=0,
                            expected_previous_token=None
                        )
                    )
                )
            ).speak(speak_output)
            
        except Exception as e:
            logger.error(e)
            speak_output = "Desculpe, tive um problema ao buscar esse vídeo no YouTube."
            handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response

class PauseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.PauseIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.add_directive(
            PlayDirective(play_behavior=PlayBehavior.CLEAR_ALL)
        )
        return handler_input.response_builder.response

class ResumeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.ResumeIntent")(handler_input)

    def handle(self, handler_input):
        # Para um resume real, precisaríamos salvar o estado. 
        # Aqui ele apenas confirma que não pode retomar do ponto exato sem banco de dados.
        return handler_input.response_builder.speak("Para retomar, peça para tocar a música novamente.").response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Ocorreu um erro. Tente novamente mais tarde."
        return handler_input.response_builder.speak(speak_output).response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PlayVideoIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()