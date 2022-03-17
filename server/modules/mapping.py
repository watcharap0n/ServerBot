from typing import Optional
from linebot.models import ImagemapArea, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction


def image_map(base_url_image: Optional[str] = None,
              size: Optional[dict] = None, areas: Optional[dict] = None):
    if size and areas:
        height = size['height']
        width = size['width']
        template_image = ImagemapSendMessage(
            base_url=base_url_image if base_url_image else
            'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
            alt_text='products',
            base_size=BaseSize(height=height, width=width),
            actions=[MessageImagemapAction(
                text=i['text'],
                area=ImagemapArea(
                    x=i['area']['x'],
                    y=i['area']['y'],
                    width=i['area']['width'],
                    height=i['area']['height'])
            ) if i['type'] == 'message' else
                     URIImagemapAction(
                         link_uri=i['linkUri'],
                         area=ImagemapArea(
                             x=i['area']['x'],
                             y=i['area']['y'],
                             width=i['area']['width'],
                             height=i['area']['height']))
                     for i in areas]
        )
        return template_image
    return False
