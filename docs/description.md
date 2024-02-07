# Описание проекта

Даный проект позволяет из текстового представления R-схемы получать искомый код на языке Python. Также реализуется сравнительный анализ с генерацией кода на языке Дракон.
На первой итерации система позволяет генерироать алгоритмы, состоящие из управляющий конструкций: IF, FOR, WHILE.

## Пример генерации кода Python из R-схемы

<style>
.box{
    display: flex;
    justify-content: center;"
}
.sub-box{
    margin-right: 20px;
}
</style>
<div class="box">
<div class="sub-box">

**R-схема:**

```
    x
o-------->o
|   a=5   |
|         |
|-------->|
    a=10
```

</div>
<div class="sub-box">
        <b>Диаграмма Дракон:</b><br>
        <img width="350px" src="img/drakon.png" alt="drakon language"/>
    </div>
<div class="sub-box">

**Код на Python:**

```python
if x:
    a = 5
else:
    a = 10
```

</div>
</div>

