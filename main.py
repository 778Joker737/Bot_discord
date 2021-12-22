import discord #импортируем библиотеку дискорда\
from discord.ext import commands  #импортируем команды из библиотеки
import datetime
from discord import utils
import config 
from PIL import Image, ImageFont, ImageDraw
import requests
import json
import io
from Cybernator import Paginator


PREFIX='.'

bot = commands.Bot(command_prefix='.', intens=discord.Intents.all())# prefix - это запуск команды. То что в ковычках это будет опорный знак с помощью, которых будем вызывать определенные команды

bot.remove_command('help')

hello_words = ['привет', 'ку', 'салам', 'здарова', 'hi', 'hello', 'йоу']
answer_words = ['че по серверу', 'команды', 'инфо', 'помощь', 'что тут есть']
bb_words = ['bb', 'пока', 'удачи', 'до свидания', 'всего хорошего', 'poka', 'до связи']
bad_words = ['дурак', 'клоун', 'сука', 'флуд']

POST_ID = 922619798775562260

ROLES = {
    '🔥':829710118769131562 ,
    '👨‍🏫':898359210943848568,
    '🚶':921513206051135498
}
EXCROLES =()
MAX_ROLES_PER_USER = 3

class MyClient(discord.Client):
 async def on_raw_reaction_add(self, payload):
    if payload.message_id == config.POST_ID:
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])
            if (len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


async def on_raw_reaction_remove(self, payload):
    channel = self.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)
    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=config.ROLES[emoji])
        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))

@bot.event #нужно для того чтобы узнать о работоспособности команд

async def on_ready():# функция определяет
    print('BOT connected and ready')#говорит о том что бот запущен
    await bot.change_presence(status=discord.Status.online, activity= discord.Game('.help'))




@bot.event
async def on_command_error(ctx, error):
    pass



@bot.event
async def on_member_join( member ):
    await bot.process_commands(member)
    channel = bot.get_channel(919798808978796626)

    role = discord.utils.get(member.guild.roles, id = 921513206051135498 ) #добовляем айди канала в котором будет высвечиватся сообщение

    await member.add_roles( role )
    await channel.send(embed = discord.Embed(description=f'Новый пользователь``{member.name}``,присоеденилися к нам!', color = 0x0c0c0c))



@bot.event
async def on_message( message ): #Функция
    await bot.process_commands(message)
    msg = message.content.lower()
   # #msg =переменная
    if  msg in hello_words:
        await message.channel.send("Привет, чего изволите?")

    if msg in answer_words:
        await message.channel.send("В команде .help присутствует список возможных команд")

    if msg in bb_words:
        await message.channel.send('До свидания, надеюсь я вам помог ')

    if msg in bad_words:
        await message.delete()
        await message.author.send(f'{ message.author.name }, не пиши, а то в бан ')



@bot.command()
async def test(ctx):
    embed1 = discord.Embed(title="Страница 1", description='test 1')
    embed2 = discord.Embed(title="Страница 2", description='test 2')
    embed3 = discord.Embed(title="Страница 3", description='test 3')
    embed4 = discord.Embed(title="Страница 4", description='test 4')
    embeds = [embed1, embed2, embed3, embed4]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()


@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed


@bot.command()# используем префикс для вызова
@commands.has_permissions( administrator = True)#только админы могут выполнить команду

async def clear( ctx, amount : int):
    await ctx.channel.purge(limit = amount)


@bot.command()# используем префикс для вызова
@commands.has_permissions( administrator = True)#только админы могут выполнить команду

async def kick( ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed(title='kick', colour=discord.Color.red())
    await ctx.channel.purge(limit = 1)#удаляет сообщение

    await member.kick( reason = reason)#Дает возможность кикнуть юзера


    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Участника лобби выгнали', value='Грязнуля: {}'.format(member.mention))
    emb.set_footer(text="<Ответственный за кик, {}".format(ctx.author.name), icon_url=ctx.author.avatar_url)

    await ctx.send( embed= emb)



@bot.command()# используем префикс для вызова
@commands.has_permissions( administrator = True)#только админы могут выполнить команду

async def ban( ctx, member: discord.Member, *, reason = None):# банит участника группы
    emb = discord.Embed( title= 'Ban',colour = discord.Color.red() )
    await ctx.channel.purge(limit = 1)

    await member.ban(reason = reason)  #банит юзера

    emb.set_author(name = member.name, icon_url=member.avatar_url)
    emb.add_field(name = 'Участник лобби ЗАБЛОКИРОВАН', value = 'Виновный: {}'.format(member.mention))
    emb.set_footer( text = "<Ответственный за бан, {}".format(ctx.author.name), icon_url=ctx.author.avatar_url )

    await ctx.send( embed= emb)


@bot.command()# используем префикс для вызова

async def hello(ctx):# при команде hello будет выводить сообщение

    author = ctx.message.author  #Кто отправил запрос

    await ctx.send(f' {author.mention} Привет, я ваш личный бот.')# отвечает на комманду hello
                            #mention выделяет отправителя при отправки сообщения

@bot.command()# используем префикс для вызова



async def help(ctx):#Выводится таблица со всеми возможными командами
    emb = discord.Embed( title = 'Навигация по командам') #title - параметр (огловление)

    emb.add_field(name = '{}clear'.format( PREFIX ), value='Очистка чата')
    emb.add_field(name = '{}kick'.format( PREFIX ), value='Выгнать участника')
    emb.add_field(name = '{}ban'.format( PREFIX ), value='Заблокировать участника ')
    emb.add_field(name='{}time'.format(PREFIX), value='Возможность просмотреть время')
    emb.add_field(name='{}mute'.format(PREFIX), value='Возможность замутить игра')
    emb.add_field(name='{}say'.format(PREFIX), value='Бот напишит вам особое сообщение ')
    emb.add_field(name='{}карта'.format(PREFIX), value='Бот даст вам личную карточку ')
    emb.add_field(name='{}join/leave'.format(PREFIX), value='<бот присоединиться или выйдит из голосового чата> ')
    emb.add_field(name='{}Fox'.format(PREFIX), value='<бРандомные картинки лис> ')
    emb.add_field(name='{}карта'.format(PREFIX), value='<карточка участника> ')
    await ctx.send(embed = emb)


@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Вы должны быть подключены  к голосовому чату ")


@bot.command()
async def leave(ctx):
    if (ctx.voice_bot):
        await ctx.guild.voice_bot.disconnect()
        await ctx.send("я вышел из голосового чата")
    else:
        await ctx.send("я не в госовом чате")





@bot.command()# используем префикс для вызова



async def time(ctx):
    emb = discord.Embed(title = 'Источник',description="вы сможете узнать текущее время ", colour = discord.Colour.purple(), url = 'https://www.timeserver.ru/cities/ru/moscow')#Ссылка на источник
    emb.set_author( name = bot.user.name, icon_url = bot.user.avatar_url)#Добавление икконки и никнеййма бота
    emb.set_footer(text= 'Смотри за временем, а то убежит :)', icon_url = bot.user.avatar_url)#Добавление мал иконки бота с коментарием
    emb.set_image( url='https://darnado.com/wp-content/uploads/2014/08/235491122.jpg')        #большая картинка
    emb.set_thumbnail( url = 'https://w7.pngwing.com/pngs/686/423/png-transparent-blend-s-4chan-youtube-reddit-normie-hideri-purple-child-face.png') #Маленькая картинка

    now_date = datetime.datetime.now()#переменная времени
    emb.add_field( name= 'Time ', value = 'Time : {}'.format(now_date))#выводит вреемя

    await ctx.send(embed = emb)


@bot.command()
@commands.has_permissions( administrator = True)#только админы могут выполнить команду


async def mute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='Ты в муте чел')

    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention},нарушил общесвенный порядок')


@bot.command()
async def say(ctx):
    await ctx.author.send("В команде Say, вы   можете получать инофрмацию которую захочет донести админ, всем добра")# отправка сообщений в лс


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, Укажите аргумент')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, У вас недостаточно прав')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, ты не достоин этой привилегии')


@kick.error
async def kick_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, ты не достоин этой привилегии')




@bot.command(aliases = ['карта'])
async def card_user(ctx):
    await ctx.channel.purge(limit = 1)

    img = Image.new('RGBA', (400,200), '#242345')
    url = str(ctx.author.avatar_url)[:-10]

    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator

    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15), f'{name}#{tag}', font = headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

    img.save('user_card.png')

    await ctx.send(file = discord.File(fp = 'user_card.png'))


bot.run('token')