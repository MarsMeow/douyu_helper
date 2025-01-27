# encoding:utf-8
from common.dy_glows import *
from common.login_check import *
from common.config import conf
from common.dy_badge import *
from common.logger import logger
from common.dy_glows import glow_donate
import math
from common.send_message import send_message


def run():
    logger.info("------登录检查开始------")
    login_res = is_login()
    logger.info("------登录检查结束------")
    mode = int(conf.get_conf("Modechoose")['givemode'])
    if login_res:
        get_glow()
        try:
            glow_nums = get_own()
            assert glow_nums != 0
            if mode == 1:
                logger.info("当前选择模式为:自选模式")
                nums = conf.get_conf_list('selfMode', 'giftCount')
                room_list = conf.get_conf_list('selfMode', 'roomId')
                logger.info("------开始捐赠荧光棒------")
                print_sentence = {}
                for i in range(len(nums)):
                    print_sentence[room_list[i]] = glow_donate(nums[i], room_list[i])
                logger.info("------荧光棒捐赠结束------")
                get_need_exp(print_sentence)
            elif mode == 0:
                logger.info("当前选择模式为:平均分配模式")
                room_list = get_room_list()
                every_give = math.ceil(glow_nums / len(room_list))
                left = int(glow_nums) - int(every_give) * (len(room_list) - 1)
                logger.info("------开始捐赠荧光棒------")
                print_sentence = {}
                for room in room_list:
                    if room == room_list[-1]:
                        print_sentence[room] = glow_donate(left, room)
                    else:
                        print_sentence[room] = glow_donate(every_give, room)
                logger.info("------荧光棒捐赠结束------")
                get_need_exp(print_sentence)
            else:
                logger.warning("配置错误,没有这种选项,请修改配置并重新执行")
                send_message(False, "配置错误,没有这种选项,请修改配置并重新执行")
        except Exception as e:
            logger.warning("背包中没有荧光棒,无法执行赠送,任务即将结束")
            send_message(False, "背包中没有荧光棒,无法执行赠送,任务即将结束")
            logger.debug(e)
    else:
        logger.warning("未登录状态无法进行后续操作,任务已结束")
        send_message(False, "未登录状态无法进行后续操作,任务已结束")



if __name__ == '__main__':
    run()
