Для решения задач на слежение и передачу вам необходимо написать три программы:
- кодировщик (преобразует входные данные в передаваемые по неустойчивому каналу)
- декодировщик (принимает данные из канала и формирует выходной файл)
- трекер (выполняет управление радаром  для слежения за спутником)

Каждую из трёх программ можно писать на одном из четырёх языков — C, C++, Java, Python 3.6. Заметим, что языки программы могут не совпадать между собой (например, допускается загружать трекер на Python, а кодировщик — на Java).

При написании программы можно использовать любые модули, входящие в стандартную библиотеку языка (установка дополнительных модулей не предусмотрена).

Принцип написания и взаимодействия программ со стендом един на всех языках (вплоть до одинаковых и не содержит радикальных отличий, поэтому далее будет обобщённое описание работы с каждой из программ. Конкретные детали и сигнатуры функций есть в предоставленных примерах программ.

== Кодировщик ==

Необходимо реализовать процедуру вида converter(FILE filein, FILE fileout), преобразующую содержимое входного файла и записывающую передаваемые данные в выходной.

Параметры:
- filein — входной файл, открытый на чтение в бинарном режиме ("rb")
- fileout — выходной файл, открытый на запись в бинарном режиме ("wb")

== Декодировщик == 

Необходимо реализовать процедуру вида converter(FILE filein, FILE fileout, FILE tracklog), преобразующую содержимое входного файла и записывающую передаваемые данные в выходной.

Параметры:
- filein — входной файл, открытый на чтение в бинарном режиме ("rb")
- fileout — выходной файл, открытый на запись в бинарном режиме ("wb")
- tracklog — файл журнала трекера, открытый на чтение в бинарном режиме ("rb")

== Трекер == 

Необходимо реализовать процедуру вида tracker(FILE tracklog), выполняющую управление радаром на протяжении всего процесса передачи данных. 

Параметры:
- tracklog — файл журнала трекера, открытый на запись в бинарном режиме ("wb")

Для взаимодействия с радаром используется модуль client2server, предоставляющий одноимённый класс client2server. У класса есть несколько функций:

- Status moveStop() - остановить повороты радара, возвращает Status;
- Status moveLeft(int n) - поворачивать радар влево со скоростью n (в условных единицах), возвращает Status;
- Status moveRight(int n) - поворачивать радар вправо со скоростью n (в условных единицах), возвращает Status;
- Status getStatus() - получить статус состояния радара, возвращает Status

Status — 128-разрядное беззнаковое целое со следующей структурой:
  0-11 биты - DX (знаковое) - смещение спутника на камере радара
  12-15 биты - состояние радара:
    0 - неопределённое
    1 - отключен
    2 - включен
    3 - перемещается
  16-19 биты - положение радара:
    0 - неопределённое
    1 - поворачивается влево
    2 - поворачивается вправо
    3 - в крайнем левом положении
    4 - в крайнем правом положении
  20-36 биты - точное время на радаре в милисекундах с начала работы (беззнаковое)

Движение радара после команды выполняется непрерывно, т.е. для его остановки необходимо явно послать соответствующую команду.

== Важные детали ==

Ни один из перечисленных ниже файлов не нужно открывать и закрывать самостоятельно (это делается автоматически вне пользовательского кода).

Все файлы открыты в двоичном формате, то есть чтение и запись осуществляется не текстом, а набором байт. Особенно важно это учитывать при реализации на Python.

Программы работают изолированно друг от друга, поэтому не имеет смысла создавать и взаимодействовать с файлами, кроме тех, которые передаются в параметрах функций. 

Стандартные потоки вывода и ошибок (stdout и stderr) недоступны для прямого чтения (т.к. выполняются в изолированной среде). Если вы хотите журналировать ошибки — делайте это через имеющиеся файлы.

При загрузке программы компилируются, но в случае с Python лишь производится синтаксическая проверка. Ошибки времени выполнения не регистрируются напрямую, но их можно заметить по поведению системы во время передачи. Если она завершилась досрочно — проблема в кодировщике или декодировщике. Если радар не двигается — возможно, в трекере ошибка времени выполнения.