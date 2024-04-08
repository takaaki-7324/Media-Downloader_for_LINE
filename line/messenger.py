from linebot.v3.messaging import PushMessageRequest


def push_message(link, lineid, tag, file_name, dur, lineapi):
    if not lineid or not lineapi:
        return

    # 完了通知
    if tag == "/mp3":
        message_dict = {
            "to": lineid,
            "messages": [
                {"type": "text", "text": file_name},
                {"type": "text", "text": link},
                {"type": "audio", "originalContentUrl": link, "duration": dur},
            ],
        }
        push_message_request = PushMessageRequest.from_dict(message_dict)
        lineapi.push_message(push_message_request)
    else:
        message_dict = {
            "to": lineid,
            "messages": [
                {"type": "text", "text": file_name},
                {"type": "text", "text": link},
            ],
        }
        push_message_request = PushMessageRequest.from_dict(message_dict)
        lineapi.push_message(message_dict)
