import requests
import json

class MeshAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def _get_request(self, endpoint: str, params: dict = None):
        """
        内部方法：发送实际的 HTTP GET 请求。
        Args:
            endpoint (str): API 端点，例如 "/status" 或 "/version"。
            params (dict, optional): 查询参数。
        Returns:
            dict: API 响应的 JSON 数据。
        Raises:
            requests.exceptions.RequestException: 网络或 HTTP 错误。
            ValueError: 非 JSON 响应。
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            response.raise_for_status()

            if response.text:
                return response.json()
            return {}
        except requests.exceptions.HTTPError as e:
            error_message = (
                f"MimoMesh API 请求失败: GET {url} - "
                f"状态码: {e.response.status_code}, 响应: {e.response.text}"
            )
            raise requests.exceptions.RequestException(error_message) from e
        except requests.exceptions.ConnectionError as e:
            error_message = f"无法连接到 MimoMesh 设备: {self.base_url} - {e}"
            raise requests.exceptions.RequestException(error_message) from e
        except requests.exceptions.Timeout as e:
            error_message = f"MimoMesh API 请求超时: {url} - {e}"
            raise requests.exceptions.RequestException(error_message) from e
        except json.JSONDecodeError as e:
            error_message = f"MimoMesh API 响应不是有效的 JSON: {url} - {e}, 响应内容: {response.text}"
            raise ValueError(error_message) from e
        except Exception as e:
            error_message = f"MimoMesh API 请求发生未知错误: {e}"
            raise requests.exceptions.RequestException(error_message) from e

    def get_status(self):
        """获取设备状态。"""
        return self._get_request("status")

    def get_version(self):
        """获取设备版本信息。"""
        return self._get_request("version")

    def get_spectrum(self):
        """获取频谱数据。"""
        return self._get_request("spectrum")

    def get_config(self):
        """获取设备配置。"""
        return self._get_request("config")
    
    def set_config(self, config_data: dict):
        """
        设置设备配置。
        Args:
            config_data (dict): 要设置的配置数据。
        Returns:
            dict: API 响应的 JSON 数据。
        Raises:
            requests.exceptions.RequestException: 网络或 HTTP 错误。
            ValueError: 非 JSON 响应。
        """
        url = f"{self.base_url}/config"
        try:
            response = requests.post(url, headers=self.headers, json=config_data, timeout=5)
            response.raise_for_status()

            if response.text:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            raise e
    
if __name__ == "__main__":
    # 替换为你的 MimoMesh 设备的实际 IP 地址
    MIMOMESH_BASE_URL = "http://192.168.1.87" 
    
    # 实例化客户端
    client = MeshAPI(MIMOMESH_BASE_URL)

    print("--- 测试 MimoMesh API 客户端 ---")

    # 测试 /status
    try:
        status_data = client.get_status()
        print("\n--- /status 响应 ---")
        print(f"状态码: 200 (OK)") # 如果成功，raise_for_status 不会抛异常
        print("数据:", json.dumps(status_data, indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"请求 /status 失败: {e}")
    except ValueError as e:
        print(f"请求 /status 响应解析失败: {e}")
