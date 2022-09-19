#Start screen Loop
done = False
start_time = pygame.time.get_ticks()
while not done and display_instructions:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('bgm.mp3')
        pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            instruction_page += 1
            if instruction_page == 2:
                display_instructions = False

    # Set the screen background
    win.fill(black)

    if instruction_page == 1:

        text = font.render("Instructions:", True, white)
        win.blit(text, [10, 20])

        text = font.render("1. Use WASD, or the Arrow Keys to move", True, white)
        win.blit(text, [10, 100])

        text = font.render("2. Left click to shoot", True, white)
        win.blit(text, [10, 150])

        text = font.render("3. Collect ammunition", True, white)
        win.blit(text, [10, 200])

        text = font.render("4. STAY ALIVE", True, white)
        win.blit(text, [10, 250])

        text = font.render("Kill or be killed", True, red)
        win.blit(text, [260, 420])

        text = font.render("How long can you survive?", True, red)
        win.blit(text, [150, 470])

        text = font.render("Click to start", True, white)
        win.blit(text, [270, 600])

    clock.tick(60)
    pygame.display.flip()

def gameOverScreen(end_time):
    seconds_survived = (end_time - start_time) // 1000
    ending = 1
    global run, gameover

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill(black)
    timer = pygame.time.get_ticks() - now2

    if ending == 1:
        win.blit(endscreen.image, endscreen.rect)
        time = font.render(str(seconds_survived/1000) ,1,red)
        win.blit(time, (410, 600))
        endtext = font.render("You survived for               seconds", True, red)
        win.blit(endtext, [100, 600])
        kill = font.render("Kill count: " +str(killcounter), 1, red)
        win.blit(kill, (280, 650))

    pygame.display.flip()
    clock.tick(100)
    # Programme loop
run = True
gameover = False

while run:

    actual_ticks = pygame.time.get_ticks()

    if gameover:
        now2 = now = actual_ticks 
        gameOverScreen(end_time)
        continue

    timer = actual_ticks - now2
    time_difference = actual_ticks - now

    if time_difference >= 1500:
        newenemy = Enemy(random.randrange(50,780), random.randrange(50,780), 1 ,wall_list)
        enemy_list.add(newenemy)
        all_sprite_list.add(newenemy)
        newenemy2 = Enemy(random.randrange(50,780), random.randrange(50,780), 1 ,wall_list)
        enemy_list.add(newenemy2)
        all_sprite_list.add(newenemy2)

        now = actual_ticks

        all_sprite_list.update()


    win.fill(white)
    win.blit(background.image, background.rect)


    for e in enemy_list:
        e.move(player)

    collide = pygame.sprite.spritecollide(player, enemy_list, False)
    if collide:
        gameover = True
        end_time = pygame.time.get_ticks()


    food_collide = pygame.sprite.spritecollide(player,food_list,False)
    for food in food_collide:
        score += 1
        bullets += 10
        food_list.remove(food)
        newfood = Food()
        food_list.add(newfood)
        all_sprite_list.add(newfood)
        all_sprite_list.remove(food)
        food_list.update()
        all_sprite_list.update()

        pygame.mixer.music.load('reload.mp3')
        pygame.mixer.music.play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.move(-2, 0)
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.move(2, 0)
            elif event.key == pygame.K_UP or event.key == ord('w'):
                player.move(0, -2)
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                player.move(0, 2)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.move(2, 0)
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.move(-2, 0)
            elif event.key == pygame.K_UP or event.key == ord('w'):
                player.move(0, 2)
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                player.move(0, -2)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            aim_pos = event.pos
            player_position = player.rect.center
            bullet_vec = pygame.math.Vector2(aim_pos[0] - player_position[0], aim_pos[1] - player_position[1]).normalize() * 10
            bullet = Bullet()
            bullet.rect.center = player.rect.center
            bullet.vec = bullet_vec

            if bullets > 0:
                all_sprite_list.add(bullet)
                bullets -= 1
                pygame.mixer.music.load('Gunshot.mp3')
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load('reload.mp3')
                pygame.mixer.music.play()


    hit = pygame.sprite.spritecollide(bullet, enemy_list, False)
    for enemy in hit:
        killcounter += 1
        enemy_list.remove(enemy)
        all_sprite_list.remove(enemy)
        enemy_list.update()
        all_sprite_list.update()

    enemy.move(player)
    all_sprite_list.update()

    all_sprite_list.draw(win)

    time = font.render(str(timer/1000) ,1,black)
    win.blit(time, (680, 5))

    scoretext = font.render("Bullets: " +str(bullets), 1, black)
    win.blit(scoretext, (5, 5))

    kill = font.render("Kill count: " +str(killcounter), 1, black)
    win.blit(kill, (250, 5))


    pygame.display.flip()

    clock.tick(100)


pygame.quit()