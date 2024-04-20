<!DOCTYPE HTML>
<html>

<head>
    <meta name="author" content="Ed Brown">
    <title>Quiz from 2005</title>
</head>

<body>
    <h1>Magic Online Quiz</h1>
 <div>
    <p>Question no {number} out of {length}</p>
    <p>Your Score: {score} out of {length}</p>
    <p><bold>{question}</bold>
    <form action="/answer" method="POST">
        <p>
        <button type="submit" name="but" value="0" id="0" {hidden[0]}>{answers[0]}</button>
        <button type="submit" name="but" value="1" id="1" {hidden[1]}>{answers[1]}</button>
        <button type="submit" name="but" value="2" id="2" {hidden[2]}>{answers[2]}</button>
        <button type="submit" name="but" value="3" id="3" {hidden[3]}>{answers[3]}</button>
        <button type="submit" name="but" value="4" id="4" {hidden[4]}>{answers[4]}</button>
        <button type="submit" name="but" value="5" id="5" {hidden[5]}>{answers[5]}</button>
        <button type="submit" name="but" value="6" id="6" {hidden[6]}>{answers[6]}</button>
        <button type="submit" name="but" value="7" id="7" {hidden[7]}>{answers[7]}</button>
        <button type="submit" name="but" value="8" id="8" {hidden[8]}>{answers[8]}</button>
        <button type="submit" name="but" value="9" id="9" {hidden[9]}>{answers[9]}</button>
        </p>
    </form>
 </div>
</body>
</html>