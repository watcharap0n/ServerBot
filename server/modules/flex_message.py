from linebot.models import FlexSendMessage


def flex_dynamic(alt_text: str, contents: dict):
    flex_custom = FlexSendMessage(
        alt_text=alt_text,
        contents=contents
    )
    return flex_custom

