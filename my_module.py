# -*- coding: UTF-8 -*-
"""
View板块的单个子模块
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import my_global as Global
from my_common import Common
from my_bond import Bonder, Define
from my_viewutil import ToolTips, ViewUtil
# from my_logger import Logger


class SubLogin(object):
    """ 登录子板块，不可为单例 """

    def __init__(self, master, index):
        self.master = master
        self.index = index
        self.bonder = None
        self.tiglab = None
        self.ip_en = None
        self.user_en = None
        self.userpwd_en = None
        self.rootpwd_en = None
        self.delbtn = None
        self.var_user = tk.StringVar()
        self.var_upwd = tk.StringVar()
        self.var_rpwd = tk.StringVar()
        self.init_event()
        self.init_frame()
        self.pack_frame()
        self.set_defaults()
        self.see_passwd_off()

    def init_event(self):
        _index = self.index
        _name = Global.G_EVT_NAME_SUBLOGIN % _index
        self.bonder = Bonder(_name)
        self.bonder.bond(Global.EVT_SEE_PSWD_ON, self.see_passwd_on)
        self.bonder.bond(Global.EVT_SEE_PSWD_OFF, self.see_passwd_off)

        Define.define(Global.EVT_GET_LOGIN_INPUT % _index,
                      self.get_inputs)
        Define.define(Global.EVT_CHG_LOGIN_TIG_COLOR % _index,
                      self.status_tig)
        Define.define(Global.EVT_SUBLOGIN_ENTRY_TIG % _index,
                      self.widget_tips)

    def init_frame(self):
        entry_style = {'master': self.master,
                       'background': Global.G_DEFAULT_COLOR,
                       'font': (Global.G_FONT, 12)
                       }
        self.tiglab = tk.Label(self.master,
                               text='●',
                               font=(Global.G_FONT, 16),
                               fg=Global.G_TIG_FG_COLOR['DEFAULT']
                               )
        self.ip_en = tk.Entry(width=15,
                              **entry_style
                              )
        self.user_en = tk.Entry(width=13,
                                textvariable=self.var_user,
                                **entry_style
                                )
        self.userpwd_en = tk.Entry(width=14,
                                   textvariable=self.var_upwd,
                                   **entry_style
                                   )
        self.rootpwd_en = tk.Entry(width=13,
                                   textvariable=self.var_rpwd,
                                   **entry_style
                                   )
        self.delbtn = tk.Button(self.master,
                                text='×',
                                font=(Global.G_FONT, 13, 'bold'),
                                bd=0,
                                command=self.destroy
                                )

    def pack_frame(self):
        grid_style = {'row': self.index + 1,
                      'padx': 4,
                      'pady': 6,
                      'ipady': 3
                      }
        self.tiglab.grid(row=self.index + 1,
                         column=0
                         )
        self.ip_en.grid(column=1,
                        **grid_style
                        )
        self.user_en.grid(column=2,
                          **grid_style
                          )
        self.userpwd_en.grid(column=3,
                             **grid_style
                             )
        self.rootpwd_en.grid(column=4,
                             **grid_style
                             )
        if self.index == 1:
            return
        self.delbtn.grid(row=self.index + 1,
                         column=5
                         )

    def set_defaults(self):
        """ 设置默认用户和密码 """
        default_info = ViewUtil.get_default_passwd()
        self.var_user.set(default_info[0])
        self.var_upwd.set(default_info[1])
        self.var_rpwd.set(default_info[2])

    def get_inputs(self, msg=None):
        return (self.ip_en.get(),
                self.user_en.get(),
                self.userpwd_en.get(),
                self.rootpwd_en.get()
                )

    def see_passwd_on(self, msg=None):
        self.userpwd_en['show'] = ''
        self.rootpwd_en['show'] = ''

    def see_passwd_off(self, msg=None):
        self.userpwd_en['show'] = '*'
        self.rootpwd_en['show'] = '*'

    def status_tig(self, status):
        """ 登录状态颜色提示 """
        try:
            self.tiglab['fg'] = Global.G_TIG_FG_COLOR[status]
        except:
            pass

    def widget_tips(self, which):
        """ 用于提示具体的entry填入的值有误 """
        try:
            ToolTips.widget_tips(eval('self.{}_en'.format(which)))
        except:
            pass

    def destroy(self):
        _index = self.index
        self.tiglab.grid_remove()
        self.ip_en.grid_remove()
        self.user_en.grid_remove()
        self.userpwd_en.grid_remove()
        self.rootpwd_en.grid_remove()
        self.delbtn.grid_remove()
        self.bonder.unbond(Global.EVT_SEE_PSWD_ON)
        self.bonder.unbond(Global.EVT_SEE_PSWD_OFF)
        Define.undefine(Global.EVT_GET_LOGIN_INPUT % _index)
        Define.undefine(Global.EVT_CHG_LOGIN_TIG_COLOR % _index)
        Define.undefine(Global.EVT_SUBLOGIN_ENTRY_TIG % _index)
        ViewUtil.del_sublogin(_index)
        del self


class TtkProgress(object):
    """ Ttk 实现的进度条 """

    def __init__(self,
                 master,
                 name,
                 width=200,
                 size=2,
                 row=1,
                 column=0):
        self.prog = ttk.Progressbar(master,
                                    length=width,
                                    mode="determinate",
                                    orient=tk.HORIZONTAL
                                    )
        self.prog["maximum"] = 100
        self.prog["value"] = 0
        _lab = tk.Label(master,
                        text=name,
                        font=(Global.G_FONT, 9+size)
                        ).grid(row=row, column=column)
        self.val_lab = tk.Label(master,
                                text='0%',
                                font=(Global.G_FONT, 9+size)
                                )
        self.prog.grid(row=row, column=column+1, ipady=size)
        self.val_lab.grid(row=row, column=column+2)

    def update(self, value):
        """ 0~1 """
        _value = value * 100
        self.prog['value'] = _value
        self.val_lab['text'] = '%s%%' % _value

    def destroy(self):
        self.prog.destroy()
        self.val_lab.destroy()


class ProgressBar(object):
    """ 进度条/比例条 """

    def __init__(self,
                 master,
                 name,
                 bg=Global.G_DEFAULT_BG,
                 size=11,
                 width=32,
                 row=1,
                 column=0):
        self.width = width
        self.value = 0
        _lab_style = {'master': master,
                      # 'relief': 'solid',
                      'font': (Global.G_FONT, size-2),
                      # 'bd': 1
                      }
        _grid_style = {'row': row,
                       'column': column + 1,
                       'sticky': tk.W
                       }

        self.namelab = tk.Label(master,
                                text=name,
                                font=(Global.G_FONT, size),
                                bg=bg
                                )
        self.namelab.grid(row=row,
                          column=column,
                          padx=5,
                          pady=5
                          )
        self.bglab = tk.Label(width=width,
                              bg='snow',
                              anchor=tk.E,
                              **_lab_style
                              )
        self.fglab = tk.Label(**_lab_style)
        self.bglab.grid(**_grid_style)
        self.fglab.grid(**_grid_style)

    def update(self, value, color=False):
        if self.value == value:
            return
        self.value = value
        sub = int(self.width * value / 100)
        percent = '%s%%' % value
        fg_color = 'PaleTurquoise'
        if value > 50:
            self.bglab['text'] = ''
            self.fglab['text'] = percent
        else:
            self.bglab['text'] = ''.join([str(percent), ' ' * 6])
            self.fglab['text'] = ''
        if isinstance(color, str):
            fg_color = color
        elif color:
            if 0 <= value < 30:
                fg_color = 'PaleTurquoise'
            elif 30 <= value < 50:
                fg_color = 'Turquoise'
            elif 50 <= value < 70:
                fg_color = 'Gold'
            elif 70 <= value < 85:
                fg_color = 'Coral'
            elif 85 <= value < 95:
                fg_color = 'OrangeRed'
            elif 95 <= value <= 100:
                fg_color = 'Red3'

        self.fglab['width'] = sub
        self.fglab['bg'] = fg_color

    def destroy(self):
        self.namelab.destroy()
        self.bglab.destroy()
        self.fglab.destroy()


class InfoWindow(object):
    """ 消息提示栏 """

    def __init__(self, master):
        self.master = master
        self.infotext = None
        self.index = 0
        self.init_event()
        self.init_frame()

    def init_event(self):
        Define.define(Global.EVT_INSERT_INFOWIN_TEXT, self.insert_text)

    def init_frame(self):
        self.infotext = scrolledtext.ScrolledText(self.master,
                                                  font=(Global.G_FONT, 10),
                                                  bd=2,
                                                  relief='ridge',
                                                  fg='Blue',
                                                  bg='AliceBlue',
                                                  height=9,
                                                  width=110
                                                  )
        self.infotext.insert(tk.END, Global.G_WELCOME_INFO)
        self.infotext['stat'] = 'disabled'
        self.infotext.pack()
        # 设置infowin可以接受事件的变量为True
        ViewUtil.set_infowin_flag()

    def insert_text(self, msg=None):
        info, level = msg
        try:
            """ 级别转换成对应的颜色 """
            color = Global.G_INFOWIN_LEVEL_COLOR[level.upper()]
        except KeyError as e:
            color = Global.G_INFOWIN_LEVEL_COLOR['INFO']
            # Logger.error(e)
        """ 信息中加入时间戳 """
        info = "\n{} [{}]: {}".format(Common.get_time(),
                                      level.upper(),
                                      str(info)
                                      )
        self.infotext['stat'] = 'normal'
        self.infotext.insert(tk.END, info)
        self.index += 1
        line = self.infotext.index(tk.END)
        line = int(line.split('.')[0]) - 1
        self.infotext.tag_add('BINGO{}'.format(self.index),
                              '{}.0'.format(line),
                              '{}.end'.format(line)
                              )
        self.infotext.tag_config('BINGO{}'.format(self.index),
                                 foreground=color
                                 )
        self.infotext.see(tk.END)
        self.infotext['stat'] = 'disabled'


class LabelButton(object):
    """ Radiobutton实现的侧边菜单栏 """

    def __init__(self, master, name, shell, intvar, text, command):
        self.name = name
        self.shell = shell
        self.command = command
        self.button = tk.Radiobutton(master,
                                     selectcolor='SkyBlue2',
                                     fg='Snow',
                                     bg='SkyBlue4',
                                     variable=intvar,
                                     width=20,
                                     bd=0,
                                     indicatoron=0,
                                     value=name,
                                     text=text,
                                     justify=tk.LEFT,
                                     font=('宋体', 14),
                                     command=self.click
                                     )
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.button['fg'] = 'Brown1'
        self.button['bg'] = 'SkyBlue3'

    def leave(self, event=None):
        self.button['fg'] = 'Snow'
        self.button['bg'] = 'SkyBlue4'

    def pack(self):
        self.button.pack(ipady=12)

    def click(self, event=None):
        self.command(self.name, self.shell)


class MyButton(object):
    """ 封装button，个性化外观 """

    def __init__(self, master, text, command, size=10, width=10):
        self.master = master
        self.button = tk.Button(master,
                                text=text,
                                activebackground=Global.G_DEFAULT_COLOR,
                                activeforeground='Red',
                                disabledforeground='Red',
                                fg='Gray23',  # 'DodgerBlue4',
                                bg=Global.G_DEFAULT_COLOR,
                                font=(Global.G_FONT, size, 'bold'),
                                width=width,
                                bd=0,
                                relief='groove',
                                command=command
                                )
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)
        self.button.pack(side=tk.LEFT)

    def enter(self, event=None):
        self.button['bg'] = 'Grey27'  # 'DodgerBlue4'
        self.button['fg'] = Global.G_DEFAULT_COLOR

    def leave(self, event=None):
        self.button['bg'] = Global.G_DEFAULT_COLOR
        self.button['fg'] = 'Gray23'  # 'DodgerBlue4'

    def config(self, key, value):
        self.button[key] = value


class TopProgress:
    """ 顶窗提示进度 """
    _toplevel = None
    _progress = None
    _infolab = None
    _top_size = (300, 80)

    @classmethod
    def start(cls, msg=None):
        try:
            width, height = msg
        except:
            width, height = cls._top_size
        cls._toplevel = tk.Toplevel()
        cls._toplevel.title('请稍候')
        cls._toplevel.resizable(False, False)
        # cls._toplevel.overrideredirect(True)
        cls._toplevel.wm_attributes('-topmost', 1)
        cls._toplevel.geometry('%sx%s' % (width, height))
        cls._toplevel.protocol("WM_DELETE_WINDOW", cls.close)
        ViewUtil.set_centered(cls._toplevel, width, height+100)
        cls._infolab = tk.Label(cls._toplevel, font=(Global.G_FONT, 11))
        cls._infolab.pack(pady=8)
        cls._progress = ttk.Progressbar(cls._toplevel,
                                        mode='indeterminate',
                                        length=250
                                        )
        cls._progress.pack(ipady=3)
        """ 开始滑块，并设置速度 """
        cls._progress.start(10)

    @classmethod
    def update(cls, info):
        cls._infolab['text'] = info

    @classmethod
    def destroy(cls, msg=None):
        try:
            cls._progress.destroy()
            cls._toplevel.destroy()
            cls._infolab.destroy()
        except:
            pass
        cls._toplevel = None
        cls._progress = None

    @classmethod
    def close(cls):
        pass


class TopAbout:
    """ 关于窗 """
    _top_size = (500, 330)
    _toplevel = None
    _showing = False

    @classmethod
    def show(cls, event=None):
        if cls._showing:
            return
        cls._showing = True
        width, height = cls._top_size
        cls._toplevel = tk.Toplevel()
        cls._toplevel.title('关于软件')
        cls._toplevel.resizable(False, False)
        cls._toplevel.wm_attributes('-topmost', 1)
        cls._toplevel.geometry('%sx%s' % (width, height))
        cls._toplevel.protocol("WM_DELETE_WINDOW", cls.close)
        ViewUtil.set_centered(cls._toplevel, width, height + 100)
        # 图标
        tk.Label(cls._toplevel, image=ViewUtil.get_image('ABOUT')).pack(ipady=10)
        # 中间部分说明
        _infolab = tk.Label(cls._toplevel,
                            bg='Snow',
                            justify='left',
                            text=Global.G_ABOUT_INFO,
                            font=(Global.G_FONT, 10)
                            )
        _infolab.pack(fill=tk.BOTH)
        # 底部版权说明
        tk.Label(cls._toplevel, text=Global.G_COPYRIGHT_INFO).pack(ipady=15)

    @classmethod
    def close(cls, event=None):
        cls._showing = False
        cls._toplevel.destroy()