from linebot.models import TextSendMessage,AudioSendMessage

def push_message(link,lineid,tag,file_name,dur,lineapi):
    if not lineid or not lineapi: return
    # 完了通知
    if tag == "/mp3":
        lineapi.push_message(
            lineid,
            messages=(
                TextSendMessage(text=('%s\n%s' % (file_name,link))),
                AudioSendMessage(original_content_url=link,duration=dur)
            )
        )
    else:
        lineapi.push_message(
            lineid,
            messages=(
                TextSendMessage(text=file_name + "\n" + link)
            )
        )