
import os
from karishmatg.karishmatgbot import *
import time

if __name__ == "__main__":
    while True:
        karishmatgbot.logger.info("Cycle")
        activecalls = os.popen("asterisk -x 'core show channels verbose' | grep 'active calls'").read().strip()
        if activecalls != "0 active calls":
            karishmatgbot.logger.info("Skipping cycle since call in progress")
            time.sleep(180)
            continue
        try:
            call_list = os.listdir("/opt/karishma-ivr/calls")
            call_list.remove("calllog")
            for call in call_list:
                files = os.listdir(os.path.join(
                    "/opt/karishma-ivr/calls", call))
                if "telegramed" in files:
                    karishmatgbot.logger.info("Ignoring {}".format(call))
                    continue
                for fn in files:
                    if ".wav" in fn:
                        karishmatgbot.logger.info(
                            "Trying to upload {}".format(call))
                        karishmatgbot.updater.bot.send_audio(-456601244, open(
                            os.path.join("/opt/karishma-ivr/calls", call, fn), "rb"), caption=call, timeout=300)
                        with open(os.path.join(os.path.join("/opt/karishma-ivr/calls", call, "telegramed")), "w") as f:
                            f.write("Telegramed")
                        karishmatgbot.logger.info(
                            "Successfully uploaded {}".format(call))
        except Exception as e:
            karishmatgbot.logger.error("{} {}".format(str(e), repr(e)))
        time.sleep(180)
