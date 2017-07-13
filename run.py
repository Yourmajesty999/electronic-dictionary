# coding=utf8
import tornado.ioloop as ioloop
import tornado.web as web
import mimetypes
import sys
import os
import bs4
import urllib
import requests

from contextlib import contextmanager
__author__ = "hellflame"

PWD = os.path.dirname(__file__)
routes = []


class Spider(object):
    def __init__(self, lang='eng', timeout=3):
        self.__html_url = "http://dict.youdao.com/w/{}/".format(lang)
        self.__timeout = timeout

    @contextmanager
    def soup(self, target_word):
        url = self.__html_url + urllib.quote(target_word.replace('/', ''))
        try:
            req = requests.get(url, timeout=self.__timeout)
        except requests.Timeout:
            sys.stderr.write('链接 `{}` 请求超时'.format(url))
            exit(1)
        except requests.ConnectionError:
            sys.stderr.write('链接 `{}` 连接失败'.format(url))
            exit(1)
        except Exception:
            sys.stderr.write('链接 `{}` 连接时发生未知错误')
            exit(1)

        if not req.status_code == 200:
            sys.stderr.write('链接 `{}` 非法状态码: {}'.format(url, req.status_code))
            exit(1)

        yield bs4.BeautifulSoup(req.content, 'html.parser')

    def deploy(self, word):
        with self.soup(word) as soup:
            match = soup.find(class_='keyword')
            if match:
                # pronunciation
                wordbook = soup.find(class_='wordbook-js')
                _pronounce = wordbook.find_all(class_='pronounce')
                pronounces = []
                translate = []
                web_translate = []
                word_phrase = []
                if not _pronounce:
                    _pronounce = wordbook.find_all(class_='phonetic')
                for p in _pronounce:
                    temp = p.get_text().replace(' ', '').replace('\n', '')
                    if not temp:
                        continue
                    pronounces.append(p.get_text().replace(' ', '').replace('\n', ''))

                # translation
                _trans = soup.find(class_='trans-container')
                if _trans and _trans.find('ul'):
                    _normal_trans = _trans.find('ul').find_all('li')
                    if not _normal_trans:
                        _normal_trans = _trans.find('ul').find_all(class_='wordGroup')
                    for _nt in _normal_trans:
                        title = _nt.find(class_='contentTitle')
                        type_ = _nt.find('span')
                        if title and type_:
                            title = title.get_text()
                            type_ = type_.get_text()
                        else:
                            title = _nt.get_text()
                            type_ = ''
                        translate.append((type_ + title).replace('\n', ''))

                # web translation
                _web_trans = soup.find(id="tWebTrans")
                if _web_trans:
                    for i in _web_trans.find_all('span', class_=None):
                        temp = i.get_text().replace('\n', '').replace(' ', '')
                        if not temp:
                            continue
                        web_translate.append(temp)

                    # word phrase
                    _word_phrase = _web_trans.find(id='webPhrase')
                    if _word_phrase:
                        for i in _word_phrase.find_all(class_='wordGroup'):
                            title = i.find(class_='contentTitle')
                            if not title:
                                continue
                            title = title.get_text()
                            word_phrase.append({
                                'phrase': title,
                                'explain': i.get_text().replace('\n', '').replace(title, '').replace(' ', '')
                            })

                # print word_phrase
                # print translate
                # print web_translate
                # print pronounces
                return 0, {
                    'pronounces': pronounces,
                    'translate': translate,
                    'web_translate': web_translate
                }
            else:
                # sentence translate may go here, but I won't use youdao. Better use google translate
                similar = soup.find(class_='error-typo')
                if similar:
                    possibles = []
                    similar = similar.find_all(class_='typo-rel')
                    for s in similar:
                        title = s.find(class_='title')
                        content = s.get_text()
                        if title:
                            title = title.get_text().replace(' ', '').replace('\n', '')
                            content = content.replace(title, '').replace(' ', '').replace('\n', '')
                        else:
                            continue
                        possibles.append({
                            'possible': title,
                            'explain': content
                        })
                    return 1, {
                        'possibles': possibles
                    }
                return None, None


class NormalBase(web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.send_error(404)

    def post(self, *args, **kwargs):
        return self.send_error(404)


settings = {
        'debug': True,
        'autoreload': True,
        'serve_traceback': True,
        'cookie_secret': '\x0e\xf9\xd4.\xf5\x035\xb8\xd29\xda\xe8L1z0\x0e\x11\xf7\xf9Q\xe9\x06=Rs\xb0\xda\xdab',
        'template_path': PWD,
        'static': PWD + '/static',
        "public": PWD + '/public',
        'default_handler_class': NormalBase
    }


class SiteService(NormalBase):
    """Here, tornado can run along on the server serving www service"""
    def get(self, path, file_type):
        target = path + '.' + file_type
        if not file_type == 'html':
            if os.path.exists(target):
                handle = web.StaticFileHandler.get_content(target)
                for i in handle:
                    self.write(i)
                    
                self.set_header('Cache-Control', 'no-store')
                self.set_header("Content-Type", mimetypes.guess_type(target)[0] or
                                'application/octet-stream')
            else:
                return self.send_error(404)
        else:
            return self.render(target)

routes.append((r'/(.+?)\.(css|js|jpg|jpeg|png|html)', SiteService))


class Dictionary(NormalBase):
    def get(self, lang, target):
        status, result = Spider(lang).deploy(target)
        return self.write({
            'code': status,
            'result': result
        })

routes.append((r'/dictionary/(.+?)/(.+?)', Dictionary))


if __name__ == '__main__':
    port = 5000
    app = web.Application(handlers=routes, **settings)
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    app.listen(port, address='127.0.0.1')
    ioloop.IOLoop.current().start()

