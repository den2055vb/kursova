# bot.py
# Константи PADDLE_SPEED та SCREEN_HEIGHT будуть потрібні,
# їх можна імпортувати або передавати як аргументи.

def control_bot_paddle(bot_paddle, ball): # screen_height не потрібен, бо є в Paddle.move_down
    """Керує рухом ракетки бота."""
    # Проста логіка: ракетка намагається вирівняти свій центр з центром м'яча по осі Y
    # Додамо невелику "мертву зону", щоб уникнути тремтіння.
    # Швидкість бота обмежена власною швидкістю ракетки.
    dead_zone = bot_paddle.speed * 0.3 # Мертва зона - 30% від швидкості ракетки

    if bot_paddle.rect.centery < ball.rect.centery - dead_zone:
        bot_paddle.move_down() # Використовуємо метод ракетки
    elif bot_paddle.rect.centery > ball.rect.centery + dead_zone:
        bot_paddle.move_up()   # Використовуємо метод ракетки