from src.ia_talking_robot.log.ConsoleLogger import ConsoleLogger

#from ..ia_talking_robot.log.ConsoleLogger import ConsoleLogger
from src.ia_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory

from src.ia_talking_robot.speech.FakeYouVoiceSynthetizer import FakeYouVoiceSynthetizer

import threading


if __name__ == "__main__":
    
    audioFactory = SimpleAudioFactory()

    consoleLogger = ConsoleLogger()
    synthetizer = FakeYouVoiceSynthetizer(audioFactory)
    synthetizer.addNewLogger(consoleLogger)
    synthetizer.setNameOnLog("Sintetizador")
    #synthetizer.setModel("weight_yr079zvzh5gfrvzbjsmrc94a5")
    synthetizer.setModel("weight_eayyttcf6rt2v4ty3vd6z8hd6")
    synthetizer.setCookie(
        ('_ga_525G5MXFJG=GS2.1.s1755388160$o9$g1$t1755388238$j60$l0$h0; '
        '_ga=GA1.1.1302113631.1755211134; '
        'visitor=eyJhbGciOiJIUzI1NiJ9.eyJhdnRfdG9rZW4iOiJhdnRfdzZrNWhydHYyczUxMWY1YXlqaGVrZTNqbXQzbSIsImNvb2tpZV92ZXJzaW9uIjoiMSJ9.wLZXt-D-wqKJJfu9eOXZTAR2qo1z36rUfRnU3UjFCOA; '
        'session=eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX3Rva2VuIjoic2Vzc2lvbl9lam10bTUwODRwZTZqeTB4YXF2M3dyNDIiLCJ1c2VyX3Rva2VuIjoidXNlcl84eTRzOTFlZHBybmt2IiwidmVyc2lvbiI6IjMifQ.64kc-2SFsRUlERERL02xUlfVSih2H2bofUr6E1vFfPc;'
        '_ga_06ZXE5FTP6=GS2.1.s1755377220$o5$g0$t1755377220$j60$l0$h0')
    )


    def asyncTest():
    #Sintetizar de forma normal
        synthetizer.synthetize("Soy Dart Véider, senior oscuro de los sith. Habla, ¿Cuál es tu mayor fortaleza?").playAudio()
    
    hilo = threading.Thread(target=asyncTest, daemon=True)
    hilo.start()
    hilo.join()
    #Reproducir el audio nuevamente sin tener que sintetizar denuevo
    synthetizer.getAudio().playAudio()