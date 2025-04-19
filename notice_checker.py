import os
import requests
from bs4 import BeautifulSoup

# 텔레그램 정보: Render에서 환경변수로 등록함
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(msg):
    """
    텔레그램으로 메시지를 전송하는 함수
    """
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': msg}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"❌ 메시지 전송 실패: {response.text}")
    else:
        print("✅ 메시지 전송 성공!")

def get_latest_notice():
    """
    상명대학교 공지사항 페이지에서 최신 공지사항의 제목과 링크를 추출하는 함수
    """
    url = 'https://www.smu.ac.kr/kor/life/notice.do?srCampus=smu'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 공지사항 리스트에서 첫 번째 항목 추출
    notice_list = soup.select('div.board_list ul li')
    if not notice_list:
        print("❗ 공지사항 항목을 찾을 수 없습니다.")
        return None, None

    first_notice = notice_list[0]
    title = first_notice.select_one('a').get_text(strip=True)
    link = first_notice.select_one('a')['href']
    full_link = f'https://www.smu.ac.kr{link}'

    print("✅ 공지사항 추출 완료:", title)
    return title, full_link

def load_last_notice():
    """
    마지막 공지 제목을 저장한 파일에서 불러옴
    """
    if not os.path.exists('last_notice.txt'):
        return None
    with open('last_notice.txt', 'r', encoding='utf-8') as f:
        return f.read().strip()

def save_last_notice(title):
    """
    마지막으로 확인한 공지 제목을 저장
    """
    with open('last_notice.txt', 'w', encoding='utf-8') as f:
        f.write(title)

def main():
    """
    메인 로직: 새로운 공지가 있으면 텔레그램으로 알림
    """
    try:
        latest_title, latest_link = get_latest_notice()
        if not latest_title:
            print("❌ 공지사항을 가져오지 못했습니다.")
            return

        last_title = load_last_notice()

        if latest_title != last_title:
            message = f"📢 새로운 공지사항:\n{latest_title}\n{latest_link}"
            send_telegram_message(message)
            save_last_notice(latest_title)
        else:
            print("ℹ️ 새로운 공지사항 없음.")
    except Exception as e:
        send_telegram_message(f"❗ 오류 발생: {e}")

if __name__ == '__main__':
    main()
