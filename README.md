# ai-talking-robot
Ai powered robot with speech recognition and synth, used for raspberry 

Explicación del funcionamiento de los servos:

    Fundamentalmente, el archivo que se conecta con los servos y los controla es:

        src.ia_talking_robot.controllers.AdafruitServoController.py

    Para probar el funcionamiento de este componente, se utiliza el test:

        src.test.TestAdafruitController.py

    Ejecutar este archivo mostrará una interfaz de texto, con la que se puede cambiar
    el ángulo de todos los servos, presionando las flechas del teclado. Con la tecla
    espacio, su valor se puede cambiar a "None", lo que en teoría, debe de detener
    la alimentación de voltaje de ese servo.

    Se puede usar ese archivo para encontrar el mínimo y máximo ángulo de rotación de
    cada servo. Una vez encontrados se deben anotar y escribir en el archivo:

        src.ia_talking_robot.sequencer.ComponentNameDefinition.py
    
    dentro en la clase ServoChannelNames. Sus miembros se escriben de la siguiente forma: 
        NOMBRE_DEL_SERVO = numero_del_canal, (valor_minimo, valor_maximo)
    
    Posteriormente, existe el siguiente archivo: 

        src.ia_talking_robot.sequencer.DefaultMoveSequencer.py

    Este archivo se encarga de reproducir "Animaciones", es decir, un conjunto de
    ángulos de diferentes servos que se van aplicando uno tras otro. A este conjunto,
    se le llama "secuencia" o "sequence". Un ejemplo de este, está en:

        src.ia_talking_robot.sequencer.TestSquence
        (Está mal escrito, lo sé.)

    Es básicamente, un arreglo de objetos, cada uno de estos objetos (a los que se
    les llamarán "pasos"), tienen unos"parámetros" y una lista de "componentes". 
        La lista de los componentes, es una lista de los componentes (servos normalmente, pero también pueden ser leds) que se activarán y moveran, así como de sus valores finales (en el caso de los servos pues el valor del ángulo en que se desea que termine). 
        En los parámetros, lo único importante es el tiempo en segundos que debe tardar mover todos los servos (o leds) desde su ángulo inicial a su ángulo final. Es recomendable no poner tiempos demasiado cortos (menos de 1 segundo), pues los servos pueden no moverse tan rápido como para lograr moverse hasta la posición final.
    
    Algo importante a destacar, es que en estas secuencias no se especifica el valor
    inicial de los componentes en cada paso, pues este se tomará del que tengan en ese
    momento antes de ejecutar cada paso.

    Para probar el funcionamiento del DefaultMoveSequencer, se ocupa el archivo:

        src.test.TestDefaultMoveSequencer

    Este ejecutará la secuencia TestSquence, pero sin usar los servos realmente.
    Para probar conjuntamente el DefaultMoveSequencer moviendo los servos con el
    AdafruitServoController, entonces se ocupa:

        src.test.TestServoSequencer

    Este puede ejecutar cualquier secuencia de la siguiente carpeta:

        src.resources.sequences.*

    Ahora, para crear secuencias, se pueden escribir manualmente, o utilizar el
    siguiente programa

        src.test.AnimationCreator

    Muy parecido a TestAdafruitController, una interfaz que se mueve con las flechas.
    Las instrucciones de uso están en el propio archivo al principio. Básicamente,
    para cada paso de la secuencia está la lista de los componentes y sus valores finales.
    Los pasos se ven en la parte de arriba con números [#] empezando desde el 0. Para agregar un nuevo paso, hay que utilizar la función de copiar (C) e ingresar un número.
    El valor de todos los componentes se copiará en el número de paso indicado, si no existe ese paso, entonces se creará. (Ojo, agregar más pasos, no te seleccionará automáticamente el paso nuevo creado, sino que seguirás en el mismo. No vayas a modificar cosas de tu paso original creeyendo que estás en el nuevo). 
    Los componentes marcados con OFF no se moverán ni se incluirán en ese paso. 
    Por ahora, la función de abrir no funciona correctamente. 
    La función de guardar (G) guardará la secuencia de la misma forma de TestSequence.
    El archivo guardado se guarda en la carpeta raíz, y puede moverse a la carpeta
    src.resources.sequences para que pueda utilizarse en el TestServoSequencer, pero
    debe modificarse el archivo __init__.py de esa carpeta para agregar las nuevas
    secuencias. Este programa respeta los mínimos y máximos del ComponentNameDefinition.
    Con (R), se puede reproducir la secuencia que se lleva hasta ahora. Con (Q) sales del programa o también presionando ctrl+C.

    Lo ideal sería crear varias animaciones que se puedan usar, y que combinen con la 
    temática.




