# Программа и методика испытаний. 

1. Тестирование парсера AST в сущности диаграмм деятельности.

   - Задача: Убедиться, что парсер правильно интерпретирует AST и преоб-
   разует его в соответствующие классы Python,
   - Методика:
     - Создать набор тестовых AST, полученных из разлчиных алгоритмов
     на псевдокоде.
     - Запустить парсер на каждом AST и проверить, что каждый узел соот-
     вествует своему Python классу.
     - Убедиться, что недочётов нет. При наличии исправить.
2. Тестирование системы с использованием языка DiaDel
    
    - Задача: Убедиться, что система успешно визуализирует псевдокод в диа-
грамму деятельности, используя языки PSAD и DiaDel.
    - Методика:
      - Создать набор тестовых алгоритмов на псевдокоде с различными сущ-
ностями. 
      - Запустить систему и проверить, что каждый псевдокод корректно отоб-
ражается в диаграмму. 
      - Добавить несколько новых сущностей из псевдокода. 
      - Протестировать на новом наборе алгоритмов. 
      - Убедиться, что недочётов нет. При наличии исправить.
3. Тестирование системы на реальных примерах использования

    - Задача: Проверить работоспособность системы на реальных практиче-
ских задачах, которые могут встретиться пользователям.
    - Методика:
      - Собрать набор реальных алгоритмов на псевдокоде из учебных посо-
бий, книг, онлайн-ресурсов и практических задач. 
      - Протестировать систему, удостоверившись, что получаются коррект-
ные диаграммы деятельности.