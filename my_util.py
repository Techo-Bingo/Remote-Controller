# -*- coding: UTF-8 -*-
"""
Viewmodel和Model板块公共模块
"""
from time import sleep
import my_global as Global
from my_logger import Logger
from my_viewmodel import ViewModel
from PIL import Image, ImageTk
from my_common import Common, JSONParser
from my_base import EnvError, FileError
from my_bond import Caller


class Utils:
    """ ViewModel/Model公共封装函数 """
    _infowin_cache = []

    @classmethod
    def _background_tell(cls, args=None):
        while 1:
            sleep(0.2)
            if not ViewModel.cache('GET_INFOWIN_EVT_FLAG'):
                continue
            """ infowin准备就绪后，消费掉info信息就退出线程 """
            for info_tuple in cls._infowin_cache:
                cls._tell(info_tuple)
            del cls._infowin_cache
            return

    @classmethod
    def _tell(cls, msg):
        Caller.call(Global.EVT_INSERT_INFOWIN_TEXT, msg)

    @classmethod
    def tell_info(cls, info, level='INFO'):
        """ 打印信息，如果infowin界面未就绪，开启线程等待 """
        if not ViewModel.cache('GET_INFOWIN_EVT_FLAG'):
            if not cls._infowin_cache:
                Common.create_thread(func=cls._background_tell)
            cls._infowin_cache.append((info, level))
            return
        cls._tell((info, level))

    @classmethod
    def windows_info(cls, info):
        Caller.call(Global.EVT_CALL_WIN_INFO, info)

    @classmethod
    def windows_warn(cls, info):
        Caller.call(Global.EVT_CALL_WIN_WARN, info)

    @classmethod
    def windows_error(cls, info):
        Caller.call(Global.EVT_CALL_WIN_ERROR, info)

    @classmethod
    def windows_ask(cls, info):
        return Caller.call(Global.EVT_CALL_WIN_ASK, info)

    @classmethod
    def top_progress_update(cls, info):
        Caller.call(Global.EVT_TOP_PROG_UPDATE, info)

    @classmethod
    def top_progress_stop(cls):
        Caller.call(Global.EVT_TOP_PROG_DESTROY)

    @classmethod
    def _top_progress(cls, info):
        Caller.call(Global.EVT_TOP_PROG_START)
        cls.top_progress_update(info)

    @classmethod
    def top_progress_start(cls, info):
        Common.create_thread(func=cls._top_progress, args=(info,))


class Init:
    """ 初始化处理类 """

    @classmethod
    def check_file(cls):
        # 创建日志目录
        if not Common.is_exists(Global.G_LOG_DIR):
            Common.mkdir(Global.G_LOG_DIR)
        # 日志大于阈值，清空
        if Common.file_size(Global.G_LOG_PATH) > Global.G_LOG_SIZE:
            Common.write_to_file(Global.G_LOG_PATH, 'Rollback init')
        try:
            if not Common.is_exists(Global.G_CONF_DIR):
                raise EnvError("%s is not exist" % Global.G_CONF_DIR)

            if not Common.is_file(Global.G_DEPEND_FILE):
                raise EnvError("%s is not exist" % Global.G_DEPEND_FILE)

            if not Common.is_file(Global.G_SETTING_FILE):
                raise EnvError("%s is not exist" % Global.G_SETTING_FILE)

            package = "%s\\%s" % (Global.G_CMDS_DIR, Global.G_PACKAGE_NAME)

            if not Common.is_file(package):
                raise EnvError("%s is not exist" % package)
        except EnvError as e:
            Logger.error(e)
            Utils.windows_error(e)
            return False
        return True

    @classmethod
    def conf_parser(cls):
        try:
            """ dependance.json解析 """
            _json_data = JSONParser.parser(Global.G_DEPEND_FILE)
            _images = _json_data['Images']
            _page_data = _json_data['Pages']
            _model_map = _json_data['ModelMap']
            _state_struct = _json_data['StatePageStruct']
            _otherlog_list = _json_data['OtherLogList']
            _photo = {}
            # 转换成photoImage格式
            for name, path in _images.items():
                if not Common.is_file(path):
                    raise FileError("%s is not exist !" % path)
                if name == 'ICO':
                    _photo[name] = path
                else:
                    _photo[name] = ImageTk.PhotoImage(
                        image=Image.open(path))
            """ settings.json解析 """
            _json_data = JSONParser.parser(Global.G_SETTING_FILE)
            _setting_map = _json_data['Setting']

            if not ViewModel.init(_model_map, _setting_map):
                raise FileError("Settings init failed !")
        except Exception as e:
            Logger.error(e)
            Utils.windows_error(e)
            return False

        # 存入images数据
        ViewModel.cache('CONF_IMAGE_DICT', type='ADD', data=_photo)
        # 设置page各类名全局变量
        Global.G_PAGES_NAME_DATA = _page_data
        # 设置state page显示的结构的全局变量
        Global.G_STATE_PAGE_STRUCT = _state_struct
        # 其他日志的名称列表
        Global.G_OTHER_LOG_STRUCT = _otherlog_list

        del _json_data
        del _images
        del _page_data
        del _model_map
        del _state_struct
        del _photo
        del _setting_map
        del _otherlog_list
        return True

    @classmethod
    def init(cls):
        return all([cls.check_file(),
                    cls.conf_parser()])



