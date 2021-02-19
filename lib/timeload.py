import time


class TimeLoad:
    @staticmethod
    def content_sys_time():
        # 当前时间
        content_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(content_time)
        return content_time

    @staticmethod
    def local_sys_time():
        # 当前时间
        localtime = time.asctime(time.localtime(time.time()))
        print("本地时间为 :", localtime)
        return localtime[0:6]


if __name__ == '__main__':
    print(TimeLoad.local_sys_time())
    print(TimeLoad.content_sys_time())
