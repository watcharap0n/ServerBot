from typing import Optional
from linebot.models import ImagemapArea, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction


def mapping_image(base_url_image: Optional[str] = None,
                  mapping: Optional[dict] = None):
    if mapping.get('size') and mapping.get('areas'):
        height = mapping['size']['height']
        width = mapping['size']['width']
        template_image = ImagemapSendMessage(
            base_url=base_url_image if base_url_image else
            'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
            alt_text='products',
            base_size=BaseSize(height=height, width=width),
            actions=[MessageImagemapAction(
                text=i['action']['text'],
                area=ImagemapArea(
                    x=i['bounds']['x'],
                    y=i['bounds']['y'],
                    width=i['bounds']['width'],
                    height=i['bounds']['height'])
            ) if i['action']['type'] == 'message' else
                     URIImagemapAction(
                         link_uri=i['action']['uri'],
                         area=ImagemapArea(
                             x=i['bounds']['x'],
                             y=i['bounds']['y'],
                             width=i['bounds']['width'],
                             height=i['bounds']['height']))
                     for i in mapping['areas']]
        )
        return template_image
    return False
