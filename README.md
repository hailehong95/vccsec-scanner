
# VCCSEC Scanner

Công cụ rà soát Mã độc máy chủ, máy tính người dùng. Thu thập dữ liệu, chuẩn hóa đầu ra kết quả sau đó gửi về Hệ thống quản lý tập chung.


## 1. Các tính năng

- Quét dựa theo các modules: info, autoruns, process, network, eventlogs, browseraddon, lastactivity, filesystem,.v.v..
- Giao diện đơn giản, dễ sử dụng
- Hỗ trợ đa nền tảng: Windows, Linux, MacOSX
- Mã hóa các kết quả quét trước khi gửi chúng về Hệ thống quản lý tập chung
- and more..!


## 2. THOR Scanner và VCCSEC Scanner

**THOR Scanner** là sản phẩm thương mại/nguồn đóng hoạt động chủ yếu dựa vào các IOCs đã biết hoặc tự phát triển trong quá trình Malware Research, Threat Hunting,.v.v.. Quá trình hoạt động của THOR hầu như chúng ta không can thiệp vào được gì nhiều, chỉ chạy quét và đợi kết quả. Với mỗi kết quả được phát hiện bởi THOR, nó sẽ đánh điểm số và phân loại mức độ nghiêm trọng: Alerts, Warnings, Notice, Info, Errors. Tham khảo công cụ **[THOR-Launcher](https://github.com/hailehong95/THOR-Launcher)** tôi đã phát triển dựa trên THOR/THOR-Lite Scanner.

**VCCSEC Scanner** với ý tưởng khác với THOR/THOR-Lite Scanner, nó không "ăn sẵn" được như THOR Scanner, nó đòi hỏi cần phải có sự phân tích, kiểm chứng kết quả sau khi quét. Ưu điểm của nó là được thiết kế với độ tùy biến cao, dễ dàng mở rộng thêm các module,.v.v.. Và tất nhiên là mã nguồn mở.


## 3. Cài đặt môi trường ứng dụng
Download và cài đặt Python 3 tại: https://www.python.org/downloads. Yêu cầu phiên bản Python 3.6 trở lên. Sau khi cài đặt kiểm tra lại và chắc chắn rằng Python đã được thêm và biến môi trường đúng đắn. Mở CMD/Powershell và kiểm tra bằng cách sau:

```bash
$ python3 -V
Python 3.8.10

$ pip3 -V
pip 21.1.2 from <Your-Python-Installed-Location>\lib\site-packages\pip (python 3.8)
```

Tạo Virtual Python Environment: Nhằm mục đích chạy ứng dụng Python của chúng ta trong một môi trường an toàn, cô lập với hệ thống thật, tránh được các xung đột hay lỗi giữa các phiên bản phần mềm, thư viện.

```bash
$ pip3 install virtualenv

# Windows
$ mkdir my-project & cd my-project
$ virtualenv -p c:\path\to\python.exe venv

# Linux và MacOSX
$ mkdir my-project && cd my-project
$ virtualenv -p /path/to/python3 venv
```

Kích hoạt Virtual Python Environment:
```bash
# Windows:
$ venv\Scripts\activate

# Linux và MacOS:
$ source venv/bin/activate
```

Sao chép mã nguồn:
```bash
$ git clone https://github.com/hailehong95/VCCSEC-Scanner.git
```

Cài đặt các gói phụ thuộc:
```bash
(venv) $ cd vccsec-scanner
(venv) $ pip install -r requirements.txt
```

## 4. Đóng gói ứng dụng

### 4.1. Các chức năng của VCCSEC Utility

Là một Tiện ích hay có thể gọi là Builder/Maker dùng để đóng gói bộ **VCCSEC Scanner** thành tệp thực thi duy nhất, thuận tiện cho việc phân phối đến người dùng khi rà quét.
```bash
(venv) $ python vccsec-util.py
Usage: vccsec-util.py [OPTIONS] COMMAND [ARGS]...

  A CLI Utility for VCCSEC Scanner

Options:
  --help  Show this message and exit.

Commands:
  build    Build VCCSEC Scanner
  clean    Clean all temporary working files
  keygen   RSA keys Generator
  make     Create VCCSEC Scanner bundle
  version  Show Utility version
```

### 4.2. Đóng gói nhanh ứng dụng

Có một lưu ý là mỗi lần đóng gói ứng dụng, **VCCSEC Utility** sẽ kiểm tra và tự động sinh cặp khóa RSA nếu nó thấy trong thư mục của bộ công cụ chưa có cặp khóa này. Khóa mã hóa là khóa công khai, còn khóa giải mã là khóa riêng. Cần lưu trữ khóa riêng này cẩn thận.


Đóng gói **VCCSEC Scanner**:

```bash
(venv) $ python vccsec-util.py build
```

Quá trình đóng gói diễn ra:

![image info](./assets/build.png)


Kết quả:

![image info](./assets/result.png)


## 5. Todo
- Thêm Form nhập thông tin người dùng
- Mã hóa kết quả quét trước khi gửi về Hệ thống quản lý tập chung
- Gửi kết quả về một hệ thống object storage. eg: Amazon S3, MinIO, Ceph,...


## 6. Các hệ thống đã chạy thử nghiệm

- Microsoft Windows: 7, 8/8.1, 10, 2012, 2016, 2019
