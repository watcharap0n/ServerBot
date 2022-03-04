from linebot.models import ImagemapArea, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction


def mango_products():
    template_image = ImagemapSendMessage(
        base_url='https://sv1.picz.in.th/images/2020/12/02/j3VUfR.png',
        alt_text='products',
        base_size=BaseSize(height=1600, width=1040),
        actions=[MessageImagemapAction(
            text=i.get('data'),
            area=ImagemapArea(
                x=i['area']['x'],
                y=i['area']['y'],
                width=i['area']['w'],
                height=i['area']['h'])
        ) if i['type'] == 'message' else
                 URIImagemapAction(
                     link_uri=i['data'],
                     area=ImagemapArea(
                         x=i['area']['x'],
                         y=i['area']['y'],
                         width=i['area']['w'],
                         height=i['area']['h']))
                 for i in data]
    )
    return template_image


data = [
    {'type': 'message', 'area': {'x': 12, 'y': 54, 'w': 210, 'h': 123}, 'data': 'ok'},
    {'type': 'message', 'area': {'x': 12, 'y': 54, 'w': 210, 'h': 123}, 'data': 'ok'},
    {'type': 'uri', 'area': {'x': 12, 'y': 54, 'w': 210, 'h': 123}, 'data': 'ja'}
]
