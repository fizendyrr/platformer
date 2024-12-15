import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 500
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.5


# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ну очень крутой платформер')
bg = pygame.image.load('fon.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

platform_image = pygame.image.load('ostrov.png')
platform_image = pygame.transform.scale(platform_image, (150, 40))

player_image = pygame.image.load('pers.png')
player_image = pygame.transform.scale(player_image, (90, 130))

# Загрузка изображения мишени
target_image = pygame.image.load('target.jpg')  # Замените 'target.png' на путь к вашему изображению
target_image = pygame.transform.scale(target_image, (70, 70))  # Измените размер по необходимости



pulya_image = pygame.image.load('pulya.png')
pulya_image = pygame.transform.scale(pulya_image, (10, 5))

portal_image = pygame.image.load('portaal.png')  # Убедитесь, что файл портала существует
portal_image = pygame.transform.scale(portal_image, (120, 170)) 
# Класс игрока
class Player:
    def __init__(self):
        self.start_position = (5, HEIGHT - 150)  # Начальная позиция
        self.rect = pygame.Rect(5, HEIGHT - 150, 90, 130)  # Начальная позиция
        self.image = player_image
        self.velocity = 5
        self.jump_height = 10
        self.is_jumping = False
        self.y_velocity = 0  # Скорость по оси Y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.velocity

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -self.jump_height  # Начальная скорость прыжка

        self.y_velocity += GRAVITY  # Применяем гравитацию
        self.rect.y += self.y_velocity

        # Проверка на приземление
        if self.rect.y >= HEIGHT - 160:  # 70 — высота платформы
            self.rect.y = HEIGHT - 160
            self.is_jumping = False
            self.y_velocity = 0

    def piupau(self):
        pass  # Пустой метод, если нужно
    def reset(self):
        self.rect.topleft = self.start_position

# Класс снаряда
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 5)  # размеры снаряда
        self.speed = -10  # скорость движения снаряда

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (145, 0, 255), self.rect)

# Класс платформы
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = platform_image  # Изображение платформы

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))




class Target:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 70)  # Размеры мишени
        self.active = True  # Флаг активности мишени

    def draw(self):
        if self.active:  # Рисуем только активные мишени
            screen.blit(target_image, (self.rect.x, self.rect.y))  # Используем изображение мишени

    def hit(self):
        self.active = False  # Делаем мишень неактивной

class Portal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 100)  # Размер портала

    def draw(self):
        screen.blit(portal_image, self.rect.topleft)

# Главная функция
def main():
    global death_count 
    global kill_count # Объявляем переменную как глобальную
    death_count = 0  # Счетчик смертей
    kill_count = 0
    clock = pygame.time.Clock()
    player = Player()
    platform = Platform(70, HEIGHT - 100, 150, 40)  # Платформа чуть выше
    platform2 = Platform(280, HEIGHT - 210, 150, 40)
    platform3 = Platform(70, HEIGHT - 320, 150, 40)
    platform4 = Platform(510, HEIGHT - 320, 150, 40)
    bullets = []
    target = Target(400, 30)
    target2 = Target(700, 220)
    portal = Portal(710, 10)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # При нажатии r
                    bullets.append(Bullet(player.rect.x + 50, player.rect.y + 87))

        for bullet in bullets[:]:  # Итерируем по копии списка
            bullet.update()  # Обновление позиции снаряда
            bullet.draw(screen)  # Отрисовка снаряда

            # Проверка на столкновение с первой мишенью
            if target.active and bullet.rect.colliderect(target.rect):
                target.hit()  # Мишень была поражена
                bullets.remove(bullet)  # Удаляем снаряд при попадании
                kill_count += 1
                continue  # Переходим к следующему снаряду


            # Проверка на столкновение со второй мишенью
            if target2.active and bullet.rect.colliderect(target2.rect):
                target2.hit()  # Вторая мишень была поражена
                bullets.remove(bullet)  # Удаляем снаряд при попадании
                kill_count += 1
                continue  # Переходим к следующему снаряду
        # Проверка на столкновение персонажа с мишенями
        if target.active and player.rect.colliderect(target.rect):
            player.reset()  # Телепортируем игрока на начальную позицию
            death_count += 1  # Увеличиваем счетчик смертей

        if target2.active and player.rect.colliderect(target2.rect):
            player.reset()  # Телепортируем игрока на начальную позицию
            death_count += 1  # Увеличиваем счетчик смертей    
        if player.rect.colliderect(portal.rect):
            print("Game Over! Win!")  # Завершаем игру
            pygame.quit()
            sys.exit()


        screen.blit(bg, (0, 0))
        player.move()
        player.draw()
        platform.draw()
        platform2.draw()
        platform3.draw()
        platform4.draw()
        target.draw()
        target2.draw()
        portal.draw()


        font = pygame.font.Font(None, 26)
        text = font.render(f'Deaths: {death_count}', True, (255, 255, 255))
        text_kill = font.render(f'Kills: {kill_count}/2', True, (255, 255, 255))
        screen.blit(text, (10, 10))
        screen.blit(text_kill, (10, 40))
        if player.rect.colliderect(platform.rect):
            if player.rect.bottom <= platform.rect.bottom:
                player.rect.bottom = platform.rect.top 
                player.is_jumping = False
                player.y_velocity = 0  # Обнуляем скорость при приземлении

        #platform 2       
        if player.rect.colliderect(platform2.rect):
            if player.rect.bottom <= platform2.rect.bottom:
                player.rect.bottom = platform2.rect.top 
                player.is_jumping = False
                player.y_velocity = 0

        if player.rect.colliderect(platform3.rect):
            if player.rect.bottom <= platform3.rect.bottom:
                player.rect.bottom = platform3.rect.top 
                player.is_jumping = False
                player.y_velocity = 0
        
        if player.rect.colliderect(platform4.rect):
            if player.rect.bottom <= platform4.rect.bottom:
                player.rect.bottom = platform4.rect.top 
                player.is_jumping = False
                player.y_velocity = 0

        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)



