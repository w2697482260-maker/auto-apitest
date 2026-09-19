"""
HTTP请求封装
"""
import time
import json
import ssl
import requests
import allure
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.util.ssl_ import create_urllib3_context
from .logger import logger


class SSLContextAdapter(HTTPAdapter):
    """自定义SSL上下文的HTTPAdapter - 禁用SNI"""

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 允许不安全的SSL选项
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        # 禁用SNI (Server Name Indication)
        kwargs['assert_hostname'] = False
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        proxy_kwargs['ssl_context'] = context
        proxy_kwargs['assert_hostname'] = False
        return super().proxy_manager_for(proxy, **proxy_kwargs)


class HttpClient:
    """HTTP客户端封装"""

    def __init__(self, base_url: str = '', timeout: int = 30):
        """
        初始化HTTP客户端
        :param base_url: 基础URL
        :param timeout: 超时时间
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.token = None

        # 禁用SSL验证
        self.session.verify = False

        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=1
        )
        # 使用自定义SSL上下文的适配器
        adapter = SSLContextAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # 禁用SSL警告
        requests.packages.urllib3.disable_warnings()

    def set_token(self, token: str):
        """设置认证token"""
        self.token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def set_headers(self, headers: Dict[str, str]):
        """设置请求头"""
        self.session.headers.update(headers)

    def _build_url(self, path: str) -> str:
        """构建完整URL"""
        if path.startswith('http'):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        logger.info(f"{'='*50} REQUEST {'='*50}")
        logger.info(f"Method: {method}")
        logger.info(f"URL: {url}")

        if kwargs.get('headers'):
            logger.info(f"Headers: {json.dumps(dict(kwargs['headers']), indent=2, ensure_ascii=False)}")

        if kwargs.get('params'):
            logger.info(f"Params: {json.dumps(kwargs['params'], indent=2, ensure_ascii=False)}")

        if kwargs.get('json'):
            logger.info(f"Body: {json.dumps(kwargs['json'], indent=2, ensure_ascii=False)}")
        elif kwargs.get('data'):
            logger.info(f"Data: {kwargs['data']}")

    def _log_response(self, response: requests.Response, elapsed: float):
        """记录响应日志"""
        logger.info(f"{'='*50} RESPONSE {'='*50}")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Elapsed: {elapsed:.3f}s")

        try:
            resp_json = response.json()
            logger.info(f"Response Body: {json.dumps(resp_json, indent=2, ensure_ascii=False)}")
        except:
            logger.info(f"Response Body: {response.text[:500]}")

        logger.info(f"{'='*100}\n")

    def _allure_attach(self, method: str, url: str, response: requests.Response, **kwargs):
        """附加到Allure报告"""
        # 请求信息
        request_info = f"""
Method: {method}
URL: {url}
Headers: {json.dumps(dict(self.session.headers), indent=2, ensure_ascii=False)}
"""
        if kwargs.get('params'):
            request_info += f"Params: {json.dumps(kwargs['params'], indent=2, ensure_ascii=False)}\n"

        if kwargs.get('json'):
            request_info += f"Body: {json.dumps(kwargs['json'], indent=2, ensure_ascii=False)}\n"

        allure.attach(request_info, name="请求信息", attachment_type=allure.attachment_type.TEXT)

        # 响应信息
        try:
            resp_json = response.json()
            response_info = json.dumps(resp_json, indent=2, ensure_ascii=False)
        except:
            response_info = response.text

        allure.attach(
            f"Status: {response.status_code}\n{response_info}",
            name="响应信息",
            attachment_type=allure.attachment_type.JSON if response.headers.get('content-type', '').find('json') != -1 else allure.attachment_type.TEXT
        )

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        :param method: 请求方法
        :param path: 请求路径
        :param kwargs: 其他参数
        :return: Response对象
        """
        url = self._build_url(path)
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('verify', False)

        # 记录请求日志
        self._log_request(method, url, **kwargs)

        # 发送请求
        start_time = time.time()
        try:
            response = self.session.request(method, url, **kwargs)
            elapsed = time.time() - start_time

            # 记录响应日志
            self._log_response(response, elapsed)

            # 附加到Allure报告
            self._allure_attach(method, url, response, **kwargs)

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            raise

    def get(self, path: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request('GET', path, params=params, **kwargs)

    def post(self, path: str, json: Optional[Dict] = None, data: Optional[Any] = None, **kwargs) -> requests.Response:
        """POST请求"""
        return self.request('POST', path, json=json, data=data, **kwargs)

    def put(self, path: str, json: Optional[Dict] = None, data: Optional[Any] = None, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request('PUT', path, json=json, data=data, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request('DELETE', path, **kwargs)

    def patch(self, path: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """PATCH请求"""
        return self.request('PATCH', path, json=json, **kwargs)
