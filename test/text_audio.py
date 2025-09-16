import requests

API_KEY = "oOOXB8arFDVrnGBGogRiRdfn"
SECRET_KEY = "O38Y2dXvcbUdvyy7vYlgtxrPj8LDTgOI"

def main():
        
    url = "https://tsn.baidu.com/text2audio"
    
    payload='tex=%E4%BD%A0%E5%A5%BD%E5%95%8A%EF%BC%8C%E6%88%91%E6%98%AF%E8%83%96%E8%83%96%EF%BC%8C%E6%88%91%E7%BB%88%E4%BA%8E%E4%BC%9A%E8%AF%B4%E8%AF%9D%E4%BA%86%EF%BC%8C%E6%88%91%E6%83%B3%E8%AF%B4%EF%BC%8C%E6%88%91%E7%88%B1%E6%88%91%E7%9A%84%E5%A6%88%E5%A6%88%EF%BC%8C%E5%93%88%E5%93%88%E5%93%88&tok='+ get_access_token() +'&cuid=Y5x69bLsS919EaG5mgUoyW6CKqLZnSdo&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=1&aue=3'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    with open('test-makerobo.mp3', 'wb') as f:
        f.write(response.text)
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
