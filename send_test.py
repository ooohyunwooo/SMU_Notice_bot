import requests  # 텔레그램 서버에 요청을 보내기 위해 사용

# ✅ 아래 두 값은 본인의 실제 값으로 바꿔주세요!
TOKEN = '8092242266:AAHBfN4PmCPFM6JQRIoUVYEryZGVIuMh8PY'
CHAT_ID = '7369110143'

def send_telegram_message(msg):
    """
    텔레그램 봇을 이용해서 특정 메시지를 보내는 함수
    :param msg: 보낼 메시지 문자열
    """
    url = f'https://api.telegram.org/bot8092242266:AAHBfN4PmCPFM6JQRIoUVYEryZGVIuMh8PY/sendMessage'  # 텔레그램 메시지 전송 API 주소
    payload = {
        'chat_id': CHAT_ID,  # 메시지를 받을 사람의 chat_id
        'text': msg          # 보낼 메시지 내용
    }

    response = requests.post(url, data=payload)  # 서버에 메시지 전송 요청
    if response.status_code == 200:
        print("✅ 메시지 전송 성공!")
    else:
        print(f"❌ 전송 실패: {response.text}")

# 테스트용 메시지를 보냅니다
if __name__ == '__main__':
    send_telegram_message("📢 테스트 메시지입니다! 텔레그램 알림 작동 확인 중입니다.")
